# -*- coding: utf-8 -*-
import scrapy


class BaijiahaoSpider(scrapy.Spider):
    name = 'baijiahao'
    allowed_domains = ['www.baidu.com']
    def __init__(self, parms=None, *args, **kwargs):
        super(BaijiahaoSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://www.baidu.com/s?ie=utf-8&cl=2&rtt=1&bsst=1&tn=news&word=%s&rsv_sug3=5&rsv_sug4=53&rsv_sug1=4&rsv_sug2=0&inputT=3659&x_bfe_rqs=03E80&x_bfe_tjscore=0.000923&tngroupname=organic_news&pn=0' % parms]

    # start_urls = ['https://baijiahao.baidu.com/s?id=1627130418408807094&wfr=spider&for=pc']

    def parse(self, response):
        # url_list = list(set([url for url in response.xpath('//a/@href').extract() if url.startswith('https://www.baidu.com')]))
        result_list = response.xpath("//div[@id='content_left']//div//div[@class='result']")
        url_list = list([url.xpath(".//h3[@class='c-title']//a/@href").extract() for url in result_list])
        name_list = list([name.xpath(".//h3[@class='c-title']//a/text()").extract() for name in result_list])
        print(name_list)
        # self.url_list = url_list
        # for url in self.url_list:
        #     print(url)
            # yield scrapy.http(url, callback=self.parse_item)
        # print(response.text)
