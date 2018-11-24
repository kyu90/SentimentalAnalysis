import requests
from bs4 import BeautifulSoup
import json
import time
import re
import pandas as pd
import numpy as np 
import os 

#종목코드 
url = "http://comp.fnguide.com/XML/Market/CompanyList.txt"
resp = requests.get(url)
json_data = resp.content

my_dic = json.loads(json_data, strict=False)
data = my_dic['Co']

codes = pd.DataFrame()
for i in range(0, len(data)):
    d = {'code' : [data[i]['cd'][1:len(data[i]['cd'])]],
         'name' : [data[i]['nm']]}
    temp = pd.DataFrame(d)
    codes = pd.concat([temp, codes], axis = 0)

def deep_crawl(url):
    try:
        resp = requests.get(str(url))
        html = resp.text

        soup = BeautifulSoup(html, "html5lib")
        temp = soup.select("#body")
        return temp[0].text
    except:
        return 0

def crawl(code, page):
    try :
        time.sleep(2)

        url = "https://finance.naver.com/item/board.nhn?code="+code+"&page="+page
        resp = requests.get(url)
        html = resp.text

        soup = BeautifulSoup(html, "html5lib")

        deep_url=[]
        for anchor in soup.findAll('a', href=re.compile("^(/item/board_read.nhn?)")):
            deep_url.append(anchor['href'])

        opinion = soup.select("#content > div.section.inner_sub > table.type2 > tbody > tr > td.tc > span")
        rec_count = soup.select("#content > div.section.inner_sub > table.type2 > tbody > tr > td > strong")
        sec_count = soup.select("#content > div.section.inner_sub > table.type2 > tbody > tr > td:nth-of-type(5) > span.tah")
        date = soup.select("#content > div.section.inner_sub > table.type2 > tbody > tr > td:nth-of-type(1) > span.tah")

        df = pd.DataFrame()
        for i in range(0, len(opinion)):
            temp = str(page) + "번째 페이지의 "+str(i)+"번째_게시글"
            d = {'rank' : [temp],
                 'date' : [date[0].text],
                 'opinion': [opinion[0].text],
                 'description' : [deep_crawl("https://finance.naver.com"+deep_url[i])],
                 'rec': [rec_count[0].text], 
                 'click_count': [sec_count[0].text]}

            temp = pd.DataFrame(d)
            df = pd.concat([temp, df],axis=0)
        df['code'] = str(code)
        return df
    except:
        return 0
        
df = pd.DataFrame()
for i in range(2000,2002):
    print("\n종목명 : %s"%codes['name'].iloc[i])
    for j in range(1,2):
        print("%d 번째 페이지 크롤링 중..."%j)
        temp = crawl(codes['code'].iloc[i],str(j))
        df = pd.concat([temp,df], axis= 0)
