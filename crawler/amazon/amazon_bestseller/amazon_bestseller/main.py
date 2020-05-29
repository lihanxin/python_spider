# from scrapy.cmdline import execute
# import os
# import sys
# while True:
#     pf ="/home/dev/Leo/amazon_bestseller/amazon_bestseller/amazon.lock" #不再读取pid
#     os.system("ps -A|grep main.py>%s"% pf) #将进程信息写入lock文件
#     if not(os.path.getsize(pf)) : #判断文件大小，当nginx没有运行时上一步写入lock的内容为空
#         print(8888)
#         sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#         execute(['scrapy','crawl','nie_amazon'])
#     else:
#         break

from scrapy import cmdline
import os
import sys
pf ="/home/dev/Leo/amazon_bestseller/amazon_bestseller/amazon.lock" #不再读取pid
while True:
    os.system("ps -A|grep main.py>%s"% pf) #将进程信息写入lock文件
    if not (os.path.getsize(pf)) : #判断文件大小，当nginx没有运行时上一步写入lock的内容为空
        print(8888)
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        cmdline.execute('scrapy crawl nie_amazon'.split())
    else:
        break

