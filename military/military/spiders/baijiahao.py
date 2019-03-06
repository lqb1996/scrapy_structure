# -*- coding: utf-8 -*-
import scrapy


class BaijiahaoSpider(scrapy.Spider):
    name = 'baijiahao'
    allowed_domains = ['baijiahao.baidu.com']
    # start_urls = ['https://baijiahao.baidu.com/s?id=1627130418408807094&wfr=spider&for=pc']
    start_urls = ['https://baijiahao.baidu.com/s?id=1627130418408807094&wfr=spider&for=pc']

    def parse(self, response):
        print(response.text)
