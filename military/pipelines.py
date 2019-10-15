# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import military.mysql_dao as py2db
# ImagesPipeline 为系统中下载图片的管道
import scrapy
from scrapy.pipelines.images import ImagesPipeline


# 处理百家号信息
class MilitaryPipeline(object):
    def process_item(self, item, spider):
        buffer = ['news_title', 'news_url', 'news_date', 'news_times', 'news_source', 'news_content', 'news_object']
        value = [item['title'], item['url'][0], item['date'], item['time'], item['source'], item['content'], item['object']]
        try:
            py2db.insert_field("baijiahao_mil_news", buffer, value)
        except Exception as e:
            print(value)
        return item


# 继承ImagesPipeline中下载图片的功能
class USNIPipeline(ImagesPipeline):
    # def process_item(self, item, spider):
    #     return item

    def get_media_requests(self, item, info):
        yield scrapy.Request(url=item['image'][0], meta={'item': item})

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_name = item['time']
        return image_name
