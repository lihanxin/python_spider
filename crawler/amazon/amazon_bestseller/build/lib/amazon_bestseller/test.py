import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spider import Spider
from CyFirst.items import CyfirstItem


class MyFirstSpider(Spider):
    name = "MyFirstSpider"
    allowed_doamins = ["e-shenhua.com"]
    start_urls = ["https://www.e-shenhua.com/ec/auction/oilAuctionList.jsp?_DARGS=/ec/auction/oilAuctionList.jsp"]
    url = 'https://www.e-shenhua.com/ec/auction/oilAuctionList.jsp'

    def parse(self, response):

        items = []
        selector = Selector(response)
        contents = selector.xpath('//table[@class="table expandable table-striped"]/tbody/tr')
        urldomain = 'https://www.e-shenhua.com'

        for content in contents:
            item = CyfirstItem()
            productId = content.xpath('td/a/text()').extract()[0].strip()
            productUrl = content.xpath('td/a/@href').extract()[0]
            totalUrl = urldomain + productUrl
            productName = content.xpath('td/a/text()').extract()[1].strip()
            deliveryArea = content.xpath('td/text()').extract()[-5].strip()
            saleUnit = content.xpath('td/text()').extract()[-4]

            item['productId'] = productId
            item['totalUrl'] = totalUrl
            item['productName'] = productName
            item['deliveryArea'] = deliveryArea
            item['saleUnit'] = saleUnit

            items.append(item)

            print(len(items))

        # **************进入每个产品的子网页
        for item in items:
            yield Request(item['totalUrl'], meta={'item': item}, callback=self.parse_item)
            # print(item['productId'])

        # 下一页的跳转
        nowpage = \
        selector.xpath('//div[@class="pagination pagination-small"]/ul/li[@class="active"]/a/text()').extract()[0]
        nextpage = int(nowpage) + 1
        str_nextpage = str(nextpage)
        nextLink = selector.xpath('//div[@class="pagination pagination-small"]/ul/li[last()]/a/@onclick').extract()
        if (len(nextLink)):
            yield scrapy.FormRequest.from_response(response,
                                                   formdata={
                                                       # 此处代码省略
                                                   },
                                                   callback=self.parse
                                                   )

    # 产品子网页内容的抓取
    def parse_item(self, response):
        sel = Selector(response)
        item = response.meta['item']

        productInfo = sel.xpath('//div[@id="content-products-info"]/table/tbody/tr')
        titalBidQty = ''.join(productInfo.xpath('td[3]/text()').extract()).strip()
        titalBidUnit = ''.join(productInfo.xpath('td[3]/span/text()').extract())
        titalBid = titalBidQty + " " + titalBidUnit
        minBuyQty = ''.join(productInfo.xpath('td[4]/text()').extract()).strip()
        minBuyUnit = ''.join(productInfo.xpath('td[4]/span/text()').extract())
        minBuy = minBuyQty + " " + minBuyUnit

        isminVarUnit = ''.join(sel.xpath('//div[@id="content-products-info"]/table/thead/tr/th[5]/text()').extract())
        if (isminVarUnit == '最小变量单位'):
            minVarUnitsl = ''.join(productInfo.xpath('td[5]/text()').extract()).strip()
            minVarUnitdw = ''.join(productInfo.xpath('td[5]/span/text()').extract())
            minVarUnit = minVarUnitsl + " " + minVarUnitdw
            startPrice = ''.join(productInfo.xpath('td[6]/text()').extract()).strip().rstrip('/')
            minAddUnit = ''.join(productInfo.xpath('td[7]/text()').extract()).strip()
        else:
            minVarUnit = ''
            startPrice = ''.join(productInfo.xpath('td[5]/text()').extract()).strip().rstrip('/')
            minAddUnit = ''.join(productInfo.xpath('td[6]/text()').extract()).strip()

        item['titalBid'] = titalBid
        item['minBuyQty'] = minBuy
        item['minVarUnit'] = minVarUnit
        item['startPrice'] = startPrice
        item['minAddUnit'] = minAddUnit
        return item