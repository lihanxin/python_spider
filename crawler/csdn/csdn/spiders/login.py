# -*- coding: utf-8 -*-
import scrapy
import re
import json
class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['csdn.net']
    start_urls = ['http://csdn.net/']

    def start_requests(self):
        url='https://passport.csdn.net/v1/register/pc/login/doLogin'
        data={"pwdOrVerifyCode": "478362291@qq.com","userIdentification": "abc8952006"}
        yield scrapy.Request(url,headers={"content-type": "application/json;charset=utf-8"}, body=json.dumps(data), callback=self.parse)
#        yield scrapy.FormRequest(url,formdata=data,callback=self.parse)

    def parse(self, response):
        yield scrapy.Request(
            url='https://blog.csdn.net/github_38589282/article/details/76735688?utm_medium=distribute.pc_relevant.none-task-blog-baidujs-8',
            callback=self.parse_detail
        )

    def parse_detail(self,response):
        print(re.findall('DEmon_121',response.body.decode()))


