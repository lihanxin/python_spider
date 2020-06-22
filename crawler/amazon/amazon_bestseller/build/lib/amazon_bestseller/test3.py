import subprocess
import time
import os


CYCLE_TIME = 30

spiders = ['nie_amazon']

cmd = 'scrapy crawl {}'
i = 0
while True:
    for s in spiders:
        subprocess.Popen(cmd.format(s), shell=True if os.name == 'posix' else False)
    i += 1
    print("第{}轮执行".format(i))
    time.sleep(CYCLE_TIME)

