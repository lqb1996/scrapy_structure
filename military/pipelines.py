# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import military.mysql_dao as py2db

class MilitaryPipeline(object):
    def process_item(self, item, spider):
        buffer = ['news_title', 'news_url', 'news_date', 'news_times', 'news_source', 'news_content', 'news_object']
        value = [item['title'], item['url'][0], item['date'], item['time'], item['source'], item['content'], item['object']]
        try:
            py2db.insert_field("baijiahao_mil_news", buffer, value)
        except Exception as e:
            print(value)
        return item

class USNIPipeline(object):
    def process_item(self, item, spider):
        print("spider" + spider)
        print("item" + item)
        return item
