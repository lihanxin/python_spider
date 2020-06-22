# -*- coding: utf-8 -*-
import scrapy
from Avv.items import AvvItem


class AvSpider(scrapy.Spider):
    name = 'av'  # 爬虫名
    allowed_domains = ['51porn.net/']  # 爬虫作用域

    # 爬取第2页到最后一页的代码
    url = 'http://www.51porn.net/nvyoudaquan/index_{}.html'  # 起始url，并用花括号格式化
    offset = 2  # 偏移量
    start_urls = [url.format(str(offset))]  # 拼接为完整url

    def parse(self, response):  # 第一个parse,从中提取下一层url
        # 第一部分
        links = response.xpath("//ul[@class='clearfix']/li/a/@href").extract()  # 利用xpath提取下一层的url列表，并用extract转换为字符串
        for link in links:  # 遍历上个列表
            url = "http://www.51porn.net" + link  # 由于提取出来的url不完整，所以需要拼接为完整的url
            yield scrapy.Request(url, callback=self.parse_s, dont_filter=True)  # 请求下一层url，方法为第二个parse，dont_filter=True的作用是避免有时候新的url会被作用域过滤掉


        # 第二部分
        m_page = 26  # 这里设置的是第一层的url有多少页
        if self.offset < m_page:  # 如果当前页小于最大页
            self.offset += 1  # 偏移量自增1
            yield scrapy.Request(self.url.format(str(self.offset)), callback=self.parse, dont_filter=True)  # 再此请求第一层的新的url


def parse_s(self, response):
    link = response.xpath("//div[@class='wrap loadimg avlist-small']/ul/li[1]/a/@href").extract()[0]  # 提取第2层url
    url = "http://www.51porn.net" + link  # 拼接为新的url
    yield scrapy.Request(url, callback=self.parse_t, dont_filter=True)  # 请求第3个parse


def parse_t(self, response):
    links = response.xpath("//ul[@class='alllist clearfix']/li/a/@href").extract()  # 提取第3层url
    for link in links:
        url = "http://www.51porn.net" + link  # 拼接为新的url

        yield scrapy.Request(url, callback=self.parse_last, dont_filter=True)  # 请求最后的parse


def parse_last(self, response):
    item = AvvItem()  # 实例一个引入的字典类对象
    node_list = response.xpath("//div[@class='content loadimg wow fadeInUp']")
    for node in node_list:
        # 提取以下具体信息
        item["m_num"] = node.xpath("./p[1]/text()").extract()[0]
        item["m_name"] = node.xpath("./p[2]/text()").extract()[0]
        item["s_name"] = node.xpath("./p[3]/a/text()").extract()[0]
        item["i_date"] = node.xpath("./p[4]/text()").extract()[0]
        item["l_work"] = node.xpath("./p[5]/text()").extract()[0]
        item["m_style"] = node.xpath("./p[7]/text()").extract()[0] if len(
            node.xpath("./p[7]/text()")) > 0 else "无"  # 判断此信息是否为空值
        item["c_work"] = node.xpath("./p[8]/img/@src").extract()[0]

    yield item  # 返回