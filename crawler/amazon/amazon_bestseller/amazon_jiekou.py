import json
from datetime import datetime, timedelta
from flask import request,Flask
import pymongo

app = Flask(__name__)
from retrying import retry

def get_collections(dbname,coll):
    client = pymongo.MongoClient('120.78.67.236', 27017)
    auth = client.admin
    auth.authenticate("root", "Yibai1101")
    db = client[dbname]
    collections = db[coll]
    return collections

def default(obj):
    """
    只要检查到了是bytes类型的数据就把它转为str类型
    :param obj:
    :return:
    """
    if isinstance(obj, bytes):
        return str(obj, encoding='utf-8')



@app.route('/amazon/')
@retry(stop_max_attempt_number=1)
def find():
    m=[]
    start_time_init = ((datetime.today() + timedelta(days=-1))).strftime("%Y-%m-%d 00:00:00")  # 查询时间为今天
    end_time_init = ((datetime.today() + timedelta(days=-1))).strftime("%Y-%m-%d 23:59:59")  # 查询时间为今天
    start_time = request.args.get('start_time') if request.args.get('start_time') else start_time_init
    end_time = request.args.get('end_time') if request.args.get('end_time') else end_time_init
    pagesize = int(request.args.get('pagesize')) if request.args.get('pagesize') else 50
    page = int(request.args.get('page')) if request.args.get('page') else 1
    skip=pagesize *(page-1) if page>=1  else pagesize
    v = collections.find({"crawling_time":{"$gte":start_time,"$lte":end_time},"end":"1"},
    {"title":1,"price":1,"image_url":1,"product_url":1,"product_location":1,"scrore":1,"reviews":1,"crawling_time":1}).limit(pagesize).skip(skip)

    for x in v:
        m.append({"title":x["title"],"price":x["price"],"image_url":x["image_url"],"product_url":x["product_url"],
                "product_location":x["product_location"],"scrore":x["scrore"],"reviews":x["reviews"],"crawling_time":x["crawling_time"]})
    return json.dumps({"status": 'true', "data": m}, ensure_ascii=False, indent=1)

if __name__=="__main__":

    collections = get_collections("YB_others_spider", "Amazon_bestseller")
    app.run(host='0.0.0.0', port=8686)

