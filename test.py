# -*- coding:utf-8 -*-
import re
import datetime
import os
import sys
#正则
str='www.baidu.com'
print(re.match('www',str).span())
print(re.match('com',str))

str = "邮件拉取-适用所有平台\n\n\n![]http://dp.yibai-it.com:33344/server/../Public/Uploads/2020-05-23/5ec8e8c003d10.jpg)"
site = re.findall("[(](.*?)[)]", str)
print(site)

str = "欢迎使用易佰API文档系统！\n\n\n**售后管理数据流程图**\n\n1、客服新建售后单和登记退款单数据订单信息新建售后单，然后进行审核，审核通过后推送DSS，ERP，新建售后单需要调用平台接口进行退款，登记退款单不需要。\n数据流程图：\n![](http://192.168.71.156/server/../Public/Uploads/2020-05-23/5ec89780ae9e3.png)\n\n2、登记客诉单，确认通过后推送WMS，接收WMS处理结果后更新状态信息。\n数据流程图：\n![](http://192.168.71.156/server/../Public/Uploads/2020-05-23/5ec89792dab61.png)\n3、从订单列表登记收款请求单，调用erp接口校验所填收款信息，校验通过登记成功。\n数据流程图：\n![](http://192.168.71.156/server/../Public/Uploads/2020-05-23/5ec897a7a6be2.png)\n4、收款请求，订单列表发起收款请求，通过PayPal接口请求收款，请求成功，可以取消收款请求，请求失败更新请求状态。\n数据流程图：\n![](http://192.168.71.156/server/../Public/Uploads/2020-05-23/5ec897b5161b0.png)"
print(re.findall('[(](.*?)[)]',str))

str='showStockDate({"info":{"000001":{"name":"\u5e73\u5b89\u94f6\u884c"}},"data":{"000001":{"10":"13.32","8":"13.39","9":"13.08","13":"88296055.00","19":"1173619010.00","7":"13.10","15":"43048172.00","14":"44246183.00","69":"14.30","70":"11.70","12":"5","17":"421619.00","264648":"0.320","199112":"2.462","1968584":"0.455","2034120":"7.560","1378761":"13.292","526792":"2.385","395720":"-850480.000","461256":"-29.234","3475914":"258484630000.000","1771976":"1.630","6":"13.00","11":""}}})'
print(re.findall('showStockDate[(](.*?)[)]',str))

str='https://hq.gucheng.com/SZ000010/'
print(re.findall('\d{6}',str)[0])

str='国药一致(000028)'
print(str.split('(')[0])
print(re.findall('[(](.*?)[)]',str)[0])

str = '1102231990xxxxxxxx'
res = re.search('(?P<province>\d{3})(?P<city>\d{3})(?P<born_year>\d{4})',str)
print(res.groupdict())

#range()函数
for i in range(4):
    print(i)

#时间
print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

#yield使用
def test_yield():
    print("program is starting ")
    while True:
        res = yield 6
        print("res:", res)
data = test_yield()
print(next(data))
print("----------------------")
print(next(data))

#列表推导式
departments_list = [
    " conversor digital ",
    " receptor cine box ",
    " receptor ",
    " vaporizador ervas ",
    " alexa ",
    " smart tv "
]
print([i.strip() for i in departments_list])

#字典推导式
cookies_temp = 'uuid_tt_dd=10_20045694210-1584712573345-791920; dc_session_id=10_1584712573345.982694; __gads=ID=3d8dba977ff4a473:T=1584712574:S=ALNI_MaX0g_IJRs4sMJvBLMfj8dL5mkDvA; Hm_lvt_e5ef47b9f471504959267fd614d579cd=1586485265; Hm_ct_e5ef47b9f471504959267fd614d579cd=6525*1*10_20045694210-1584712573345-791920; __yadk_uid=MZm34JAZa1OIDecGgQfPimduknzygNVg; UN=DEmon_121; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=6525*1*10_20045694210-1584712573345-791920!5744*1*DEmon_121; dc_sid=19168fb88f49cee20cceaf388e91f4e6; TY_SESSION_ID=05a7b2ee-0075-4738-be8f-1853d26df3e0; c_first_ref=www.baidu.com; c_utm_source=blogxgwz2; aliyun_webUmidToken=T40E31D7A57341D6D1FF02511912682B5A8433961B88F4E05A0ABA94EEC; c_first_page=https%3A//blog.csdn.net/itgujing/article/details/82392179; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1590048836,1590056826,1590118490,1590133978; c_utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-2.nonecase; c_ref=https%3A//blog.csdn.net/itgujing/article/details/82392179; SESSION=bc4913ae-9ae7-491e-a01f-6256a48be70e; UserName=DEmon_121; UserInfo=a3a729cd595b4d84b94f941b21847a20; UserToken=a3a729cd595b4d84b94f941b21847a20; UserNick=DEmon_121; AU=3A4; BT=1590139224398; p_uid=U000000; Hm_up_6bcd52f51e9b3dce32bec4a3997715ac=%7B%22islogin%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isonline%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isvip%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%7D; announcement=%257B%2522isLogin%2522%253Atrue%252C%2522announcementUrl%2522%253A%2522https%253A%252F%252Fbss.csdn.net%252Fm%252Ftopic%252Flive_recruit%253Futm_source%253Dannounce0515%2522%252C%2522announcementCount%2522%253A0%252C%2522announcementExpire%2522%253A3600000%257D; dc_tos=qaq79s; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1590139217'
cookies = {i.split('=')[0]: i.split('=')[1] for i in cookies_temp.split('; ')}
print(cookies)

#列表取索引
data=['a','b','c']
for index,l in enumerate(data):
    print('{0}:{1}'.format(l,index))


#字典取值赋值
dict_tmp={'name':'ABCD','age':18}
print(dict_tmp.get('height','无'))

'''
insert_temp=''
'''
insert_sql =""" AAAA """

if '':
    print('空字符串')

print(insert_sql)





