# encoding=utf-8
#环球网新闻事件抽取
import re
import jieba
import sys
# from proxy import *
from bs4 import BeautifulSoup
from mysql_dao import find_line, insert_field, update_field,\
    fetch_row
from proxy_py import *
# sys.path.append(r'\script\DAO')
# sys.path.append(r'/')

south_area_list = ['南海','西沙','台湾','南沙','菲律宾','越南','港','澳','台海','印尼','印度尼西亚','台北','台','菲','越']
east_area_list = ['东海','钓鱼岛','日本','韩国','冲绳','釜山','朝鲜','鹿儿岛','黄海','渤海','日美','美日','美韩','韩朝','朝韩','中日','中韩','中朝','朝中']
tibet_area_list = ['藏南','印度','印军']
# area_list = ['南海', '东海', '藏南']

def add_dict_freq():
    for j in south_area_list + east_area_list + tibet_area_list:
        jieba.suggest_freq((j, '称'), True)
        jieba.suggest_freq(j, True)
    return jieba

def isvaild(html):
    if html == None or html.status_code != 200:
        return True
    else:
        return False

def getText(url, encoding, pattern):
    html = getHtml(url)
    retry_count = 5
    while isvaild(html):
        html = getHtml(url)
        retry_count -= 1
        print("html_retry"+str(retry_count))
        if retry_count == 0:
            break
    html.encoding = encoding
    soup = BeautifulSoup(html.text, features="lxml")
    main_text = soup.select(pattern)
    retry_count = 5
    while main_text == []:
        html = getHtml(url)
        retry_count_1 = 5
        while isvaild(html):
            html = getHtml(url)
            retry_count_1 -= 1
            print("html_level2_retry"+str(retry_count_1))
            if retry_count_1 == 0:
                break
        html.encoding = encoding
        soup = BeautifulSoup(html.text, features="lxml")
        main_text = soup.select(pattern)
        retry_count -= 1
        print("main_text_retry"+str(retry_count))
        if retry_count == 0:
            return main_text
    return main_text

#http://mil.huanqiu.com/world/
def get_mil_url(url):
    main_text = getText(url, "utf-8", 'ul[class="listPicBox"]')
    solo_set = main_text[0].find_all(attrs={"class": "item"})
    for i in solo_set:
        header_solo = i.h3.a
        times = str(i.h6)
        dr = re.compile(r'<[^>]+>')
        times = dr.sub('', times)
        news_url = str(header_solo['href'])
        news_title = str(header_solo.string) 
        seg_list = add_dict_freq().cut_for_search(news_title)  # 搜索引擎模式
        for j in seg_list:
            if j in south_area_list:
                area = '南海'
            if j in east_area_list:
                area = '东海'
            if j in tibet_area_list:
                area = '藏南'
        if 'area' in vars():
            buffer = ['news_title','news_url','news_times','area']
            value = [news_title, news_url, times, area]
            try:
                insert_field("event_mil_news", buffer, value)
            except Exception as e:
                print(value)
                continue
            del area

def update_title_url(max_page):
    suffix = ".html"
    page_list = ['']
    for i in range(2, max_page+1):
        page_list.append(str(i) + suffix)
    for i in page_list:
        try:
            print("http://mil.huanqiu.com/world/"+i)
            get_mil_url("http://mil.huanqiu.com/world/"+i)
        except Exception as e:
            print(e)
            continue
        
def get_content():
    url_list = fetch_row("event_mil_news", "news_url")
    count = 0
    for i in url_list:
        try:
            count += 1
            main_text = str(getText(i, "utf-8", 'div[class="la_con"]'))
            print(count)
            dr = re.compile(r'AD_SURVEY_Add_AdPos\(.*?\);|<[^>]+>|&.*?;')
            main_text = dr.sub('', main_text)[2:-2]
            main_text = main_text.strip()
            main_text = "".join(main_text.split())
            update_field("event_mil_news", ["news_content"], [main_text], "news_url", i)
        except Exception as e:
            print(e)
            continue
    
if __name__ == '__main__':
    #update_title_url(30)
    get_content()


            