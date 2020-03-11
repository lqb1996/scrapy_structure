# -*- coding: utf-8 -*-
import scrapy
from military.items import MilitaryItem


class UsniNewsSpider(scrapy.Spider):
    name = 'USNI_PAGES'
    allowed_domains = ['news.usni.org']
    start_urls = ['https://news.usni.org/category/fleet-tracker']

    def parse(self, response):
        result_list = response.xpath("//div[@id='bodyMain']//section//div[@id='content']//article")
        for li in result_list:
            mil_item = MilitaryItem()
            mil_item['title'] = li.xpath(".//header//h1[@class='entry-title']//a/text()").extract_first()
            mil_item['url'] = li.xpath(".//header//h1[@class='entry-title']//a/@href").extract_first()
            mil_item['time'] = li.xpath(".//header//div[@class='post-date']//time[@class='entry-date']/text()").extract_first()
            request = scrapy.Request(mil_item['url'], callback=self.parse_detail)
            request.meta['item'] = mil_item
            yield request

        # 拿到下一页
        next_page = response.xpath("//a[@class='next']/@href").extract_first()
        if next_page:
            # next_page = next_page[0]
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_detail(self, response):
        mil_item = response.meta['item']
        mil_item['content'] = response.xpath("//div[@id='content']//article//div[@class='entry-content']").extract_first()
        yield mil_item
