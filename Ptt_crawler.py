from __future__ import unicode_literals
from bs4 import BeautifulSoup
import requests
import json


def get_url(url):
    req = requests.get(url).content.decode('utf-8')
    soup = BeautifulSoup(req,'html.parser')
    return soup


def parse(soup):
    article = soup.find_all('div',class_='r-ent')
    articles = {'title':[],'attr':[]}
    for art in article:
        title = art.find('div',class_='title').text
        point = art.find('div',class_='nrec').text
        author = art.find('div',class_='author').text
        date = art.find('div',class_='date').text
        try:
            content_url = art.find('a').get('href')
        except AttributeError:
            print("error " + str(title.find('a')) )
        articles['title'].append(title)
        articles['attr'].append({'point':point,'author':author,'date':date,'content_url':'https://www.ptt.cc/'+content_url})
        #articles.append({ 'title':title,'attr':{'point':point,'author':author,'date':date,'content_url':'https://www.ptt.cc/'+content_url} })
    json_data = json.dumps(articles,ensure_ascii=False)
    print(json_data)
    
    with open('./data.json','w',encoding='utf-8') as f:
        json.dump(json_data,f)
    


url = 'https://www.ptt.cc/bbs/joke/index.html'

soup = get_url(url)
parse(soup)