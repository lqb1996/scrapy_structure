# _*_ coding:utf-8 _*_
#爬虫代理
import requests

header_info = {
    'Host': 'mil.huanqiu.com',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9'
    }

def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").content

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))
    
def getHtml(url):
    retry_count = 5
    proxy = get_proxy()
    while retry_count > 0:
        try:
            html = requests.get(url, proxies={"http": "http://{}".format(proxy.decode())}, timeout = 10)
            return html
        except Exception as e:
            print(e)
            retry_count -= 1
    delete_proxy(proxy)
    return None

def postHtml(url, headers = None, datas = None):
    retry_count = 3
    proxy = get_proxy()
    while retry_count > 0:
        try:
            html = requests.post(url, data=datas, headers=headers, proxies={"http": "http://{}".format(proxy)})
            return html
        except Exception:
            retry_count -= 1
    delete_proxy(proxy)
    return None

if __name__ == '__main__':
    html = getHtml('https://public-api.adsbexchange.com/VirtualRadar/AircraftList.json?refreshTrails=1')
    print(html.text)