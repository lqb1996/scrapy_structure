from scrapy import cmdline
import military.mysql_dao as py2db

object_list = py2db.fetch_row("event_mil_news", "news_url")
cmdline.execute('scrapy crawl baijiahao -a parms=F22'.split())
# cmdline.execute('scrapy crawl baijiahao'.split())
