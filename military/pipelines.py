# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import military.mysql_dao as py2db
# ImagesPipeline 为系统中下载图片的管道
import scrapy, os, time
from scrapy.utils.project import get_project_settings
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


# 处理网页信息
class USNIPagesPipeline(object):
    def process_item(self, item, spider):
        settings = get_project_settings()
        store_dir = os.path.join(os.getcwd(), settings.get('PAGES_STORE'))
        if not os.path.exists(store_dir):
            os.makedirs(store_dir)
        t = time.strptime(item['time'], "%B %d, %Y %I:%M %p")
        store_name = time.strftime("%Y-%m-%d %H:%M:%S", t) + '.txt'
        with open(os.path.join(store_dir, store_name), 'a+') as f:
            f.write('title:' + item['title'] + '\n')
            f.write('time:' + item['time'] + '\n')
            f.write('url:' + item['url'] + '\n')
            f.write(item['content'])
        return item