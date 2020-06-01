# -*- coding: utf-8 -*-
import scrapy
import re
import json


class AttendanceSpider(scrapy.Spider):
    name = 'Attendance'
    allowed_domains = ['italent.cn']
    start_urls = ['https://cloud.italent.cn/Attendance/',
                  'https://cloud.italent.cn/api/v2/UI/TableList?viewName=Attendance.SingleObjectListView.EmpAttendanceDataList&metaObjName=Attendance.AttendanceStatistics&app=Attendance'
                  ]

    def start_requests(self):
        cookies_temp='Tita_PC=YiSzliuGtU-_kjC11uYCAppKMkmuHgeU9OHHLpaWCJ049GH6Celc43OEvQm4WMU6; iTalent-tenantId=109937; ssn_Tita_PC=YiSzliuGtU-_kjC11uYCAppKMkmuHgeU9OHHLpaWCJ049GH6Celc43OEvQm4WMU6; key-128320933=true'
        cookies = {i.split('=')[0]: i.split('=')[1] for i in cookies_temp.split('; ')}
        payload = {
            "table_data": {
                "paging": {"total": 26, "capacity": 30, "page": 0, "capacityList": [15, 30, 60, 100]}
            },
            "search_data": {
                "metaObjName": "Attendance.AttendanceStatistics",
                "searchView": "Attendance.EmpAttendanceDataSearch",
                "items": [{
                    "name": "Attendance.AttendanceStatistics.SwipingCardDate",
                    "text": "2020/05/01~2020/05/31",
                    "value": "2020/05/01-2020/05/31"}]
            }
        }
        request = scrapy.Request(
            self.start_urls[1],
            cookies=cookies,
            body=json.dumps(payload),
            method='POST',
            callback=self.parse
        )
        yield request

    def parse(self, response):
        data_list = json.loads(response.body.decode())
        result = [{
            "date_type": data["DateType"]["text"],
            "date_time": data["SwipingCardDate"]["text"],
            "start_time": data["ActualForFirstCard"]["text"] if "ActualForFirstCard" in data else '',
            "end_time": data["ActualForLastCard"]["text"] if "ActualForLastCard" in data else ''} for data in
            data_list["biz_data"]]
        #创建文件并写入
        with open('{0}5月考勤.py'.format(data_list["biz_data"][0]["StaffId"]["text"]), 'w+', encoding='utf-8') as f:
            i = 0
            for re in result:
                # 工作日加班超过22.30
                if re['end_time'] != '' and re['date_type'] == '工作日' and (
                        (re['end_time'].split(':')[0] == '22' and re['end_time'].split(':')[1] > '29') or
                        re['end_time'].split(':')[0] > '22'):
                    i += 1
            f.write("#总条数{0}\n#工作日加班超过22:30天数:{1}\n#考勤数据:\nlist_data={2}".format(len(result), i, result))
            f.close()

        #读取上面写入的文件文本
        with open('{0}5月考勤.py'.format(data_list["biz_data"][0]["StaffId"]["text"]),'r',encoding='utf-8') as file:
            print(file.read())
            file.close()

