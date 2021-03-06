# -*- coding: utf-8 -*-
import scrapy
import json
import re
import copy
from ..items import ImagesItem
class DataflowSpider(scrapy.Spider):
    name = 'dataflow'
    allowed_domains = []
    start_urls = ['http://192.168.71.156/server/index.php?s=/api/item/info']

    def start_requests(self):
        form_data = {'item_id': '100', 'default_page_id': '7051'}
        yield scrapy.FormRequest(url=self.start_urls[0], formdata=form_data, callback=self.parse)

    def parse(self, response):
        catalogs=json.loads(response.body.decode())['data']['menu']['catalogs'][0]['catalogs'][0]['catalogs']
        for catalog in catalogs:
            if "pages" in catalog:
                for page in catalog["pages"]:
                    yield scrapy.FormRequest(
                        url='http://192.168.71.156/server/index.php?s=/api/page/info',
                        formdata={"page_id":page["page_id"]},
                        callback=self.parse_detail
                    )

    def parse_detail(self,response):
        page=json.loads(response.body.decode())['data']
        url_temp=re.findall('[(](.*?)[)]',page['page_content'])
        img_urls=url_temp if len(url_temp)>0 else None
        if img_urls is not  None:
            #只有1张图片
            if len(img_urls)==1:
                yield scrapy.Request(
                    img_urls[0],
                    callback=self.parse_download,
                    meta={'img_name':page['page_title'],'img_suffix':img_urls[0].split('.')[-1]}#copy.copy({'img_name':page['page_title'],'img_suffix':img_url.split('.')[-1]})
                )

            #有多张图片
            else:
                for index,url in enumerate(img_urls):
                    yield scrapy.Request(
                        url,
                        callback=self.parse_download,
                        meta={'img_name':'{0}{1}'.format(page['page_title'],index), 'img_suffix': url.split('.')[-1]}
                    )

    def parse_download(self,response):
        img_name=response.meta["img_name"]
        img_suffix = response.meta["img_suffix"]

        #直接下载图片
        # with open('D:\Desktop\图片下载\{0}.{1}'.format(img_name,img_suffix),'wb') as f:
        #     f.write(response.body)
        #     f.close()

        # 给到图片下载器下载图片
        image_item=ImagesItem()
        image_item['img_url']=response.url
        image_item['img_name']='{0}.{1}'.format(img_name,img_suffix)
        yield image_item





