import time
import os
import sys
from scrapy.cmdline import execute
while True:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    execute(['scrapy', 'crawl', 'nie_amazon'])
    time.sleep(86400)  # 每隔一天运行一次 24*60*60=86400s

