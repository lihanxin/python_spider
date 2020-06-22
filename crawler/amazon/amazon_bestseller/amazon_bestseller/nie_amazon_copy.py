# -*- coding: utf-8 -*-
import scrapy
from lxml import etree
from bs4 import BeautifulSoup
from amazon_bestseller.items import AmazonBestsellerItem
import time
class NieAmazonSpider(scrapy.Spider):
    name = 'nie_amazon_copy'
    allowed_domains = ['amazon.com']
    start_urls = ['https://www.amazon.com/gp/bestsellers/?currency=USD&language=en_US']
    def parse(self, response):

        higher_ups =response.xpath('//*[@id="zg_browseRoot"]/li/span/text()').extract_first() #顶级名称
        end1= 0 if len(response.xpath('//*[@id="zg_browseRoot"]/ul/li[1]/a/text()').extract_first())>1 else 1 #标识最后一个节点
        trs_bestsell = response.xpath('//*[@id="zg_browseRoot"]/ul/li')
        for i in range(len(trs_bestsell)):
            item = AmazonBestsellerItem()
            product_name_one = trs_bestsell[i].xpath("./a/text()").extract_first()
            product_name_one_url = trs_bestsell[i].xpath("./a/@href").extract_first()
            item["product_name_one"] = product_name_one
            item["product_name_one_url"] = product_name_one_url
            level1="1"
            print("1级",product_name_one, product_name_one_url)
            yield scrapy.Request( url= product_name_one_url, callback=self.parse_item_url, meta=({'product_name_one': product_name_one,
            'product_name_one_url':product_name_one_url,"level1":level1,"higher_ups1":higher_ups,"end1":end1}))


    def parse_item_url(self, response):
        a1 = response.meta['product_name_one']
        a1_url = response.meta['product_name_one_url']
        level = response.meta['level1']
        higher_ups = response.meta['higher_ups1']
        end = response.meta['end1']
        nie_url = []
        first_page_url = response.xpath("//*[@id='zg-center-div']/div[2]/div/ul/li[2]/a/@href").extract_first() # 第一页网址
        if first_page_url:
            nie_url.append(first_page_url)
        two_page_url = response.xpath("//*[@id='zg-center-div']/div[2]/div/ul/li[4]/a/@href").extract_first()  # 第二页网址
        if two_page_url:
            nie_url.append(two_page_url)
        for url in nie_url:
            yield scrapy.Request(url=url, callback=self.parse_item_son_last,
                                 meta=({'product_name_one': a1, 'product_name_one_url': a1_url,"level":level,"higher_ups":higher_ups,"end":end}))



    def parse_item_son_last(self, response):
        #item = response.meta['item']
        """获取1级页面数据"""

        trs_bestsell1 = response.xpath('//*[@id="zg-ordered-list"]/li')
        for i in range(len(trs_bestsell1)):
            item = AmazonBestsellerItem()
            #price = ''.join(trs_bestsell4[i].xpath('./span/div/span//span/span/text() | ./span/div/span/div[2]/a/span/span/text()').extract())
            price = ''.join(trs_bestsell1[i].xpath('.//span[@class="p13n-sc-price"]/text()').extract())
            image_url = trs_bestsell1[i].xpath('./span/div/span/a[1]/span/div/img/@src').extract_first()
            reviews = trs_bestsell1[i].xpath('./span/div/span/div/a[2]/text() | ./span/div/span/div[1]/a[2]/text()').extract_first()
            title = trs_bestsell1[i].xpath("./span/div/span/a/div/text()").extract_first().strip()
            product_url = "https://www.amazon.com"+ trs_bestsell1[i].xpath("./span/div/span/a[1]/@href").extract_first()
            product_location =  trs_bestsell1[i].xpath("./span/div/div/span[1]/span/text()").extract_first()
            # if trs_bestsell4[i].xpath("./span/div/span/div[1]/a[1]/i/span/text()").extract_first() is None:
            #     scrore = ''.join(trs_bestsell4[i].xpath("./span/div/span/div[2]/a[1]/i/span/text()").extract_first())
            # else:
            #     scrore = ''.join(trs_bestsell4[i].xpath("./span/div/span/div[1]/a[1]/i/span/text()").extract_first())

            scrore = trs_bestsell1[i].xpath("./span/div/span/div[1]/a[1]/i/span/text() | ./span/div/span/div[2]/a[1]/i/span/text()").extract_first()
            crawling_time = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
            item["product_name_one"] = response.meta['product_name_one']
            item["product_name_one_url"] = response.meta['product_name_one_url']
            item["level"] = response.meta['level']
            item["end"] = response.meta['end']
            item["price"] = price
            item["image_url"] = image_url
            item["reviews"] = reviews
            item["title"] = title
            item["product_url"] = product_url
            item["product_location"] = product_location
            item["scrore"] = scrore
            item["higher_ups"] = response.meta['higher_ups']
            item["crawling_time"] = crawling_time
            # a1 = response.meta['product_name_one']
            # a1_url = response.meta['product_name_one_url']
            #print(price,image_url,reviews,title,product_url,product_location)
            yield item

        """获取2级页面url"""
        trs_bestsell = response.xpath('//*[@id="zg_browseRoot"]/ul/ul/li')
        higher_ups = response.meta['product_name_one']  # 1级名称
        for i in range(len(trs_bestsell)):
            item = AmazonBestsellerItem()
            product_name_two = trs_bestsell[i].xpath("./a/text()").extract_first()
            product_name_two_url = trs_bestsell[i].xpath("./a/@href").extract_first()
            a2= product_name_two
            a2_url= product_name_two_url
            item["product_name_two"] = product_name_two
            item["product_name_two_url"] = product_name_two_url
            level2 = "2"
            print("2级", product_name_two, product_name_two_url)
            yield scrapy.Request(url=product_name_two_url, callback=self.parse_item_son_last2,
                                 meta=({'product_name_two': a2, 'product_name_two_url': a2_url, "level2": level2,"higher_ups2":response.meta['product_name_one']}))


    # def parse_item_url2(self, response):
    #     a2 = response.meta['product_name_two']
    #     a2_url = response.meta['product_name_two_url']
    #     level2 = response.meta['level2']
    #     higher_ups2 = response.meta['higher_ups2']
    #     nie_url2 = []
    #     first_page_url = response.xpath("//*[@id='zg-center-div']/div[2]/div/ul/li[2]/a/@href").extract_first() # 第一页网址
    #     if first_page_url:
    #         nie_url2.append(first_page_url)
    #     two_page_url = response.xpath("//*[@id='zg-center-div']/div[2]/div/ul/li[4]/a/@href").extract_first()  # 第二页网址
    #     if two_page_url:
    #         nie_url2.append(two_page_url)
    #     for url in nie_url2:
    #         yield scrapy.Request(url=url, callback=self.parse_item_son_last2,
    #                              meta=({'product_name_two': a2, 'product_name_two_url': a2_url,"level2":level2,"higher_ups2":higher_ups2}))
    #
    #



    def parse_item_son_last2(self, response):
        """获取2级页面数据"""
        end2 = 0 if len(response.xpath('//*[@id="zg_browseRoot"]/ul/ul/ul/li[1]/a/text()').extract_first()) > 1 else 1  # 标识最后一个节点
        trs_bestsell2 = response.xpath('//*[@id="zg-ordered-list"]/li')
        for k in trs_bestsell2:
            item = AmazonBestsellerItem()
            price = ''.join(k.xpath('.//span[@class="p13n-sc-price"]/text()').extract())
            image_url = k.xpath('./span/div/span/a[1]/span/div/img/@src') .extract_first()
            reviews = k.xpath('./span/div/span/div/a[2]/text() | ./span/div/span/div[1]/a[2]/text()').extract_first()
            title = k.xpath("./span/div/span/a/div/text()").extract_first().strip()
            product_url = "https://www.amazon.com"+ k.xpath("./span/div/span/a[1]/@href").extract_first()
            product_location =  k.xpath("./span/div/div/span[1]/span/text()").extract_first()
            scrore = k.xpath("./span/div/span/div[1]/a[1]/i/span/text() | ./span/div/span/div[2]/a[1]/i/span/text()").extract_first()
            crawling_time = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
            item["product_name_one"] = response.meta['product_name_two']
            item["product_name_one_url"] = response.meta['product_name_two_url']
            item["level"] = response.meta['level2']
            item["end"] = end2
            item["price"] = price
            item["image_url"] = image_url
            item["reviews"] = reviews
            item["title"] = title
            item["product_url"] = product_url
            item["product_location"] = product_location
            item["scrore"] = scrore
            item["higher_ups2"] = response.meta['higher_ups2']
            item["crawling_time"] = crawling_time
            yield item

        two_page_url = response.xpath("//*[@id='zg-center-div']/div[2]/div/ul/li[4]/a/@href").extract_first()  # 第二页网址
        if two_page_url:
            yield scrapy.Request(url=two_page_url, callback=self.parse_item_son_last2,meta=({'product_name_two': response.meta['product_name_two'],
                                'product_name_two_url': response.meta['product_name_two_url'],"level2":response.meta['level2'],"higher_ups2":response.meta['higher_ups2']}))



        # trs_bestsell = response.xpath('//*[@id="zg_browseRoot"]/ul/ul/ul/li')
        # higher_ups3 = response.meta['product_name_two']  # 2级名称
        # """获取3级页面url"""
        # for i in range(len(trs_bestsell)):
        #     item = AmazonBestsellerItem()
        #     product_name_three = trs_bestsell[i].xpath("./a/text()").extract_first()
        #     product_name_three_url = trs_bestsell[i].xpath("./a/@href").extract_first()
        #     a2 = product_name_three
        #     a2_url = product_name_three_url
        #     level3 = "3"
        #     print("3级", a2, a2_url)
        #     yield scrapy.Request(url=product_name_three_url, callback=self.parse_item_son_last3,
        #                          meta=({'product_name_three': a2, 'product_name_three_url': a2_url, "level3": level3,
        #                                 "higher_ups3": higher_ups3}))



    def parse_item_son_last3(self, response):
        """获取3级页面数据"""
        end3 = 0 if len(response.xpath('//*[@id="zg_browseRoot"]/ul/ul/ul/ul/li[1]/a/text()').extract_first()) > 1 else 1  # 标识最后一个节点
        trs_bestsell3 = response.xpath('//*[@id="zg-ordered-list"]/li')
        for i in range(len(trs_bestsell3)):
            item = AmazonBestsellerItem()
            price =''.join(trs_bestsell3[i].xpath('.//span[@class="p13n-sc-price"]/text()').extract())
            image_url = trs_bestsell3[i].xpath('./span/div/span/a[1]/span/div/img/@src') .extract_first()
            reviews = trs_bestsell3[i].xpath('./span/div/span/div/a[2]/text() | ./span/div/span/div[1]/a[2]/text()').extract_first()
            title = trs_bestsell3[i].xpath("./span/div/span/a/div/text()").extract_first().strip()
            product_url = "https://www.amazon.com"+ trs_bestsell3[i].xpath("./span/div/span/a[1]/@href").extract_first()
            product_location =  trs_bestsell3[i].xpath("./span/div/div/span[1]/span/text()").extract_first()
            scrore = trs_bestsell3[i].xpath("./span/div/span/div[1]/a[1]/i/span/text() | ./span/div/span/div[2]/a[1]/i/span/text()").extract_first()
            crawling_time = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
            item["product_name_one"] = response.meta['product_name_three']
            item["product_name_one_url"] = response.meta['product_name_three_url']
            item["level"] = response.meta['level3']
            item["end"] = end3
            item["price"] = price
            item["image_url"] = image_url
            item["reviews"] = reviews
            item["title"] = title
            item["product_url"] = product_url
            item["product_location"] = product_location
            item["scrore"] = scrore
            item["higher_ups"] = response.meta['higher_ups3']
            item["crawling_time"] = crawling_time
            yield item

        """获取4级页面url"""
        trs_bestsell = response.xpath('//*[@id="zg_browseRoot"]/ul/ul/ul/ul/li')
        higher_ups4 = response.meta['product_name_three']  # 3级名称
        for i in range(len(trs_bestsell)):
            product_name_four = trs_bestsell[i].xpath("./a/text()").extract_first()
            product_name_four_url = trs_bestsell[i].xpath("./a/@href").extract_first()
            a4 = product_name_four
            a4_url = product_name_four_url
            level4 = "4"
            print("4级", a4, a4_url)
            yield scrapy.Request(url=product_name_four_url, callback=self.parse_item_son_last4,
                                 meta=({'product_name_four': a4, 'product_name_four_url': a4_url, "level4": level4,
                                        "higher_ups4": higher_ups4}))




    def parse_item_son_last4(self, response):
        """获取4级页面数据"""
        end4 = 0 if len(response.xpath('//*[@id="zg_browseRoot"]/ul/ul/ul/ul/ul/li[1]/a/text()').extract_first()) > 1 else 1  # 标识最后一个节点
        trs_bestsell4 = response.xpath('//*[@id="zg-ordered-list"]/li')
        for i in range(len(trs_bestsell4)):
            item = AmazonBestsellerItem()
            price = ''.join(trs_bestsell4[i].xpath('.//span[@class="p13n-sc-price"]/text()').extract())
            image_url = trs_bestsell4[i].xpath('./span/div/span/a[1]/span/div/img/@src') .extract_first()
            reviews = trs_bestsell4[i].xpath('./span/div/span/div/a[2]/text() | ./span/div/span/div[1]/a[2]/text()').extract_first()
            title = trs_bestsell4[i].xpath("./span/div/span/a/div/text()").extract_first().strip()
            product_url = "https://www.amazon.com"+ trs_bestsell4[i].xpath("./span/div/span/a[1]/@href").extract_first()
            product_location =  trs_bestsell4[i].xpath("./span/div/div/span[1]/span/text()").extract_first()
            scrore = trs_bestsell4[i].xpath("./span/div/span/div[1]/a[1]/i/span/text() | ./span/div/span/div[2]/a[1]/i/span/text()").extract_first()
            crawling_time = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
            item["product_name_one"] = response.meta['product_name_four']
            item["product_name_one_url"] = response.meta['product_name_four_url']
            item["level"] = response.meta['level4']
            item["end"] =end4
            item["price"] = price
            item["image_url"] = image_url
            item["reviews"] = reviews
            item["title"] = title
            item["product_url"] = product_url
            item["product_location"] = product_location
            item["scrore"] = scrore
            item["higher_ups"] = response.meta['higher_ups4']
            item["crawling_time"] = crawling_time
            yield item

        """获取5级页面url"""
        trs_bestsell = response.xpath('//*[@id="zg_browseRoot"]/ul/ul/ul/ul/ul/li')
        higher_ups = response.meta['product_name_four']  # 5级名称
        for i in range(len(trs_bestsell)):
            product_name_five = trs_bestsell[i].xpath("./a/text()").extract_first()
            product_name_five_url = trs_bestsell[i].xpath("./a/@href").extract_first()
            a5 = product_name_five
            a5_url = product_name_five_url
            level5 = "5"
            print("5级", a5, a5_url)
            yield scrapy.Request(url=product_name_five_url, callback=self.parse_item_son_last5,
                                 meta=({'product_name_five': a5, 'product_name_five_url': a5_url, "level5": level5,
                                        "higher_ups5": higher_ups}))



    def parse_item_son_last5(self, response):
        """获取5级页面数据"""
        end5 = 0 if len(response.xpath('//*[@id="zg_browseRoot"]/ul/ul/ul/ul/ul/ul/li[1]/a/text()').extract_first()) > 1 else 1  # 标识最后一个节点
        trs_bestsell5 = response.xpath('//*[@id="zg-ordered-list"]/li')
        for i in range(len(trs_bestsell5)):
            item = AmazonBestsellerItem()
            price =''.join(trs_bestsell5[i].xpath('.//span[@class="p13n-sc-price"]/text()').extract())
            image_url = trs_bestsell5[i].xpath('./span/div/span/a[1]/span/div/img/@src') .extract_first()
            reviews = trs_bestsell5[i].xpath('./span/div/span/div/a[2]/text() | ./span/div/span/div[1]/a[2]/text()').extract_first()
            title = trs_bestsell5[i].xpath("./span/div/span/a/div/text()").extract_first().strip()
            product_url = "https://www.amazon.com"+ trs_bestsell5[i].xpath("./span/div/span/a[1]/@href").extract_first()
            product_location =  trs_bestsell5[i].xpath("./span/div/div/span[1]/span/text()").extract_first()
            scrore = trs_bestsell5[i].xpath("./span/div/span/div[1]/a[1]/i/span/text() | ./span/div/span/div[2]/a[1]/i/span/text()").extract_first()
            crawling_time = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
            item["product_name_one"] = response.meta['product_name_five']
            item["product_name_one_url"] = response.meta['product_name_five_url']
            item["level"] = response.meta['level5']
            item["end"] =end5
            item["price"] = price
            item["image_url"] = image_url
            item["reviews"] = reviews
            item["title"] = title
            item["product_url"] = product_url
            item["product_location"] = product_location
            item["scrore"] = scrore
            item["higher_ups"] = response.meta['higher_ups5']
            item["crawling_time"] = crawling_time
            yield item

        """获取6级页面url"""
        trs_bestsell = response.xpath('//*[@id="zg_browseRoot"]/ul/ul/ul/ul/ul/ul/li')
        higher_ups6 = response.meta['product_name_five']  # 6级名称
        for i in range(len(trs_bestsell)):
            product_name_six = trs_bestsell[i].xpath("./a/text()").extract_first()
            product_name_six_url = trs_bestsell[i].xpath("./a/@href").extract_first()
            a6 = product_name_six
            a6_url = product_name_six_url
            level6 = "6"
            print("6级", a6, a6_url)
            yield scrapy.Request(url=product_name_six_url, callback=self.parse_item_son_last6,
                                 meta=({'product_name_six': a6, 'product_name_six_url': a6_url, "level6": level6,
                                        "higher_ups6": higher_ups6}))



    def parse_item_son_last6(self, response):
        """获取6级页面数据"""
        end6 = 0 if len(response.xpath('//*[@id="zg_browseRoot"]/ul/ul/ul/ul/ul/ul/ul/li[1]/a/text()').extract_first()) > 1 else 1  # 标识最后一个节点
        trs_bestsell6 = response.xpath('//*[@id="zg-ordered-list"]/li')
        for i in range(len(trs_bestsell6)):
            item = AmazonBestsellerItem()
            price =''.join(trs_bestsell6[i].xpath('.//span[@class="p13n-sc-price"]/text()').extract())
            image_url = trs_bestsell6[i].xpath('./span/div/span/a[1]/span/div/img/@src') .extract_first()
            reviews = trs_bestsell6[i].xpath('./span/div/span/div/a[2]/text() | ./span/div/span/div[1]/a[2]/text()').extract_first()
            title = trs_bestsell6[i].xpath("./span/div/span/a/div/text()").extract_first().strip()
            product_url = "https://www.amazon.com"+ trs_bestsell6[i].xpath("./span/div/span/a[1]/@href").extract_first()
            product_location =  trs_bestsell6[i].xpath("./span/div/div/span[1]/span/text()").extract_first()
            scrore = trs_bestsell6[i].xpath("./span/div/span/div[1]/a[1]/i/span/text() | ./span/div/span/div[2]/a[1]/i/span/text()").extract_first()
            crawling_time = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
            item["product_name_one"] = response.meta['product_name_six']
            item["product_name_one_url"] = response.meta['product_name_six_url']
            item["level"] = response.meta['level6']
            item["end"] =end6
            item["price"] = price
            item["image_url"] = image_url
            item["reviews"] = reviews
            item["title"] = title
            item["product_url"] = product_url
            item["product_location"] = product_location
            item["scrore"] = scrore
            item["higher_ups"] = response.meta['higher_ups6']
            item["crawling_time"] = crawling_time
            yield item

        """获取7级页面url"""
        trs_bestsell = response.xpath('//*[@id="zg_browseRoot"]/ul/ul/ul/ul/ul/ul/ul/li')
        higher_ups7 = response.meta['product_name_six']  # 7级名称
        for i in range(len(trs_bestsell)):
            product_name_seven = trs_bestsell[i].xpath("./a/text()").extract_first()
            product_name_seven_url = trs_bestsell[i].xpath("./a/@href").extract_first()
            a7 = product_name_seven
            a7_url = product_name_seven_url
            level7 = "7"
            print("7级", a7, a7_url)
            yield scrapy.Request(url=product_name_seven_url, callback=self.parse_item_son_last7,
                                 meta=({'product_name_seven': a7, 'product_name_seven_url': a7_url, "level7": level7,
                                        "higher_ups7": higher_ups7}))


    def parse_item_son_last7(self, response):
        """获取7级页面数据"""
        end7 = 0 if len(response.xpath('//*[@id="zg_browseRoot"]/ul/ul/ul/ul/ul/ul/ul/ul/li[1]/a/text()').extract_first()) > 1 else 1  # 标识最后一个节点
        trs_bestsell7 = response.xpath('//*[@id="zg-ordered-list"]/li')
        for i in range(len(trs_bestsell7)):
            item = AmazonBestsellerItem()
            price =''.join(trs_bestsell7[i].xpath('.//span[@class="p13n-sc-price"]/text()').extract())
            image_url = trs_bestsell7[i].xpath('./span/div/span/a[1]/span/div/img/@src') .extract_first()
            reviews = trs_bestsell7[i].xpath('./span/div/span/div/a[2]/text() | ./span/div/span/div[1]/a[2]/text()').extract_first()
            title = trs_bestsell7[i].xpath("./span/div/span/a/div/text()").extract_first().strip()
            product_url = "https://www.amazon.com"+ trs_bestsell7[i].xpath("./span/div/span/a[1]/@href").extract_first()
            product_location =  trs_bestsell7[i].xpath("./span/div/div/span[1]/span/text()").extract_first()
            scrore = trs_bestsell7[i].xpath("./span/div/span/div[1]/a[1]/i/span/text() | ./span/div/span/div[2]/a[1]/i/span/text()").extract_first()
            crawling_time = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
            item["product_name_one"] = response.meta['product_name_seven']
            item["product_name_one_url"] = response.meta['product_name_seven_url']
            item["level"] = response.meta['level7']
            item["end"] =end7
            item["price"] = price
            item["image_url"] = image_url
            item["reviews"] = reviews
            item["title"] = title
            item["product_url"] = product_url
            item["product_location"] = product_location
            item["scrore"] = scrore
            item["higher_ups"] = response.meta['higher_ups7']
            item["crawling_time"] = crawling_time
            yield item



    # def parse_item(self, response):
    #     item = response.meta['item']
    #     print(888, item)
    #     trs_bestsell2 = response.xpath('//*[@id="zg_browseRoot"]/ul/ul/li')
    #     for i in range( len(trs_bestsell2)):
    #         item = AmazonBestsellerItem()
    #         product_name_two = trs_bestsell2[i].xpath("./a/text()").extract_first()
    #         product_name_two_url = trs_bestsell2[i].xpath("./a/@href").extract_first()
    #         item["product_name_two"] = product_name_two
    #         item["product_name_two_url"] = product_name_two_url
    #         print("2级",product_name_two, product_name_two_url)
    #         yield scrapy.Request(url=product_name_two_url, callback=self.parse_item_son, meta=({'item': item}))
    #
    #
    # def parse_item_son(self, response):
    #     item = response.meta['item']
    #     print(888, item)
    #     trs_bestsell3 = response.xpath('//*[@id="zg_browseRoot"]/ul/ul/ul/li')
    #     for i in range(len(trs_bestsell3)):
    #         item = AmazonBestsellerItem()
    #         product_name_three = trs_bestsell3[i].xpath("./a/text()").extract_first()
    #         product_name_three_url = trs_bestsell3[i].xpath("./a/@href").extract_first()
    #         item["product_name_three"] = product_name_three
    #         item["product_name_three_url"] = product_name_three_url
    #         print("3级",product_name_three, product_name_three_url)
    #         yield scrapy.Request(url=product_name_three_url, callback=self.parse_item, meta=({'item': item}))
    #
    #
    # def parse_item_son_last(self, response):
    #     item = response.meta['item']
    #     print(888, item)
    #     trs_bestsell4 = response.xpath('//*[@id="zg-ordered-list"]/li')
    #
    #     for i in range(len(trs_bestsell4)):
    #         item = AmazonBestsellerItem()
    #         price = trs_bestsell4[i].xpath('./span/div/span/a[2]/span/span/span/text()').extract_first()
    #         image_url = trs_bestsell4[i].xpath('./span/div/span/a[1]/span/div/img/@src').extract_first()
    #         reviews = trs_bestsell4[i].xpath('./span/div/span/div/a[2]/text()').extract_first()
    #         title = trs_bestsell4[i].xpath("./span/div/span/a/div/text()").extract_first()
    #         product_url = trs_bestsell4[i].xpath("./span/div/span/a[1]/@href").extract_first()
    #         product_location =  trs_bestsell4[i].xpath("./span/div/div/span[1]/span/text()").extract_first()
    #         crawling_time = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    #         item["price"] = price
    #         item["image_url"] = image_url
    #         item["reviews"] = reviews
    #         item["title"] = title
    #         item["product_url"] = product_url
    #         item["product_location"] = product_location
    #         item["crawling_time"] = crawling_time
    #         print(price,image_url,reviews,title,product_url,product_location)
    #         yield item