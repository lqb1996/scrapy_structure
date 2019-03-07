# -*- coding: utf-8 -*-
import scrapy


class BjhDetailSpider(scrapy.Spider):
    name = 'BJH_detail'
    allowed_domains = ['baijiahao.baidu.com']
    def __init__(self, parms=None, *args, **kwargs):
        super(BjhDetailSpider, self).__init__(*args, **kwargs)
        self.start_urls = parms


    def parse(self, response):
        pass
