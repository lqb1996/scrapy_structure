from scrapy import cmdline
import military.mysql_dao as py2db

#爬取百家号的baijiahao.py
# object_list = py2db.fetch_row("word", "syn")
# for obj in object_list:
#     for simple_obj in obj[0][1:-1].split(','):
#         cmdline.execute(('scrapy crawl baijiahao -a parms=%s' % simple_obj.replace(' ', '')).split())

#爬取USNI
cmdline.execute('scrapy crawl USNI_PAGES'.split())
# cmdline.execute('scrapy crawl USNI_NEWS'.split())
# cmdline.execute('scrapy crawl baijiahao'.split())
