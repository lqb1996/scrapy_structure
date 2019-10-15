# -*- coding: utf-8 -*-
import scrapy
from military.items import MilitaryItem


class BaijiahaoSpider(scrapy.Spider):
    name = 'baijiahao'
    allowed_domains = ['www.baidu.com', 'baijiahao.baidu.com']
    def __init__(self, parms=None, *args, **kwargs):
        super(BaijiahaoSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&word=%s' % parms]


    def parse(self, response):
        result_list = response.xpath("//div[@id='content_left']//div//div[@class='result']")
        search_object = response.url.split('word=')[1].split('&')[0]
        for re in result_list:
            mil_item = MilitaryItem()
            mil_item['object'] = search_object
            mil_item['url'] = re.xpath(".//h3[@class='c-title']//a/@href").extract()
            for url in mil_item['url']:
                request = scrapy.Request(url, callback=self.parse_detail)
                request.meta['item'] = mil_item
                yield request
        next_page = response.xpath("//div[@id='wrapper']//p[@id='page']//a[contains(text(),'下一页')]/@href").extract_first()
        if next_page:
            # next_page = next_page[0]
            yield scrapy.Request("https://www.baidu.com"+next_page, callback=self.parse)

    def parse_detail(self, response):
        mil_item = response.meta['item']
        mil_item['title'] = response.xpath("//div[@id='article']//div[@class='article-title']//h2/text()").extract_first()
        mil_item['source'] = response.xpath("//div[@id='article']//div[@class='article-desc clearfix']//div[@class='author-txt']//p[@class='author-name']/text()").extract_first()
        mil_item['date'] = response.xpath("//div[@id='article']//div[@class='article-desc clearfix']//div[@class='author-txt']//div[@class='article-source article-source-bjh']//span[@class='date']/text()").extract_first()
        mil_item['time'] = response.xpath("//div[@id='article']//div[@class='article-desc clearfix']//div[@class='author-txt']//div[@class='article-source article-source-bjh']//span[@class='time']/text()").extract_first()
        mil_item['content'] = response.xpath("//div[@id='article']//div[@class='article-content']//text()").extract()
        yield mil_item
