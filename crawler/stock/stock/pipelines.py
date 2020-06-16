# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import pymysql

class StockPipeline:
    def open_spider(self,spider):
        self.connect=pymysql.connect(host='localhost',user='root',passwd='root',db='test')
        self.cousor=self.connect.cursor()
        print('开启数据库连接')

    #写入mysql
#     def process_item(self,item,spider):
#         insert_sql="""
#         INSERT INTO stock_info(stock_name,stock_code,stock_today_open,stock_yesterday_closed,stock_limit_up,stock_limit_down
# ,stock_turnover_rate,stock_amplitude,stock_trade_volume,stock_trade_amount,stock_in_disc,stock_out_disc
# ,stock_appoint_than,stock_price_limit,stock_pe,stock_pb,stock_trade_market_value,stock_total_market_value
# ,stock_highest,stock_lowest) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
#         """
#         self.cousor.execute(insert_sql,(item['stock_name'],item['stock_code'],item['stock_today_open'],item['stock_yesterday_closed'],item['stock_limit_up'],
#                                         item['stock_limit_down'],item['stock_turnover_rate'],item['stock_amplitude'],item['stock_trade_volume'],item['stock_trade_amount'],
#                                         item['stock_in_disc'],item['stock_out_disc'],item['stock_appoint_than'],item['stock_price_limit'],item['stock_pe'],
#                                         item['stock_pb'],item['stock_trade_market_value'],item['stock_total_market_value'],item['stock_highest'],item['stock_lowest']))
#         self.connect.commit()

    #写入mongodb
    def process_item(self, item, spider):
        client=pymongo.MongoClient()
        collection=client['stock']['stock_info']
        collection.insert(item)
        return item

    def close_spider(self,spider):
        self.connect.close()
        self.cousor.close()
        print('关闭数据库连接')



