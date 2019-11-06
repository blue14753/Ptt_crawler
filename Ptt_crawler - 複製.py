from __future__ import unicode_literals
from bs4 import BeautifulSoup
import requests
import json
import codecs

def parse_article(url):
    req = requests.get(url).content.decode('utf-8')
    soup = BeautifulSoup(req,'html.parser')

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
    #print(json_data)
    
    fp = codecs.open("data.json", 'w', encoding="utf-8")
    json.dump(json_data, fp, indent=4, ensure_ascii=False)

    return json_data


def parse_content(url):
    req = requests.get(url).content.decode('utf-8')
    soup = BeautifulSoup(req,'html.parser')

    article_content = {'title':[],'attr':[]}
    comments = []
    try:
        with open("data.json",'r',encoding='utf-8') as fp:
            json_data = json.load(fp)
    except FileNotFoundError:
        json_data = {}

    title =  soup.find('span',class_='article-meta-value').text
    content = soup.find_all('div',class_='article-metaline')[2].text
    comment = soup.find_all('div',class_='push')
    for com in comment:
        push_tag = com.find('span',class_='push-tag').text
        push_userid = com.find('span',class_='push-userid').text
        push_content = com.find('span',class_='push-content').text
        push_ipdatetime = com.find('span',class_='push-ipdatetime').text
        comments.append( {'push_tag':push_tag,'push_userid':push_userid,'push_content':push_content,'push_ipdatetime':push_ipdatetime} )

    article_content['title'] = title
    article_content['attr'] = {'content':content,'comment':comments}

    json_tmp = json.dumps(article_content,ensure_ascii=False)
    json_data = merge_dict(json_tmp,)

    fp = codecs.open("content_data.json", 'w', encoding="utf-8")
    json.dump(json_data, fp, indent=4, ensure_ascii=False)

    return json_data

"""
def merge_dict(*dicts):
    merged_dict = {}
    for d in dicts:
        for key in d:
            try:
                merged_dict[key].append(d[key])
            except KeyError:
                merged_dict[key] = [d[key]]
    return merged_dict
"""

def merge_dict(*dicts):
    merged_dict = {}
    for d in dicts:
        for key in d:
            try:
                merged_dict[key].append(d[key])
            except KeyError:
                merged_dict[key] = [d[key]]
    return merged_dict



    



    


url = 'https://www.ptt.cc/bbs/joke/index.html'
url2 = 'https://www.ptt.cc/bbs/joke/M.1573012478.A.58E.html'

#parse_article(url)
#parse_content(url2)

a = { 'title':['123','456'],'attr':[{'author':'apple'},{'author':'banana'}] }
b = {'title':['123','456','789'],'attr':[{'author':'apple2'},{'author':'banana2'}]}

print(merge_dict(a,b))

