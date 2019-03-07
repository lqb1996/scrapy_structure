from scrapy import cmdline
import mysql_dao as pdbc


cmdline.execute('scrapy crawl baijiahao -a parms="F22"'.split())
# cmdline.execute('scrapy crawl baijiahao'.split())
