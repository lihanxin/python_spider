# -*- coding: utf-8 -*-
import scrapy
import re

class PersonalSpider(scrapy.Spider):
    name = 'personal'
    allowed_domains = ['csdn.net','csdnimg.cn']
    start_urls = ['https://blog.csdn.net/maxmao1024/article/details/84575145']


    def start_requests(self):
        #使用cookie进行模拟登录
        cookies_temp = 'uuid_tt_dd=10_20045694210-1584712573345-791920; dc_session_id=10_1584712573345.982694; __gads=ID=3d8dba977ff4a473:T=1584712574:S=ALNI_MaX0g_IJRs4sMJvBLMfj8dL5mkDvA; UN=DEmon_121; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=6525*1*10_20045694210-1584712573345-791920!5744*1*DEmon_121; dc_sid=66aa58c23a791aedad6568d8dcd77be2; c_first_ref=www.baidu.com; c_utm_medium=distribute.pc_relevant.none-task-blog-baidujs-1; SESSION=8ee8bd3a-ecaf-4c5d-9691-8663b66ebfb2; announcement=%257B%2522isLogin%2522%253Atrue%252C%2522announcementUrl%2522%253A%2522https%253A%252F%252Fmarketing.csdn.net%252Fp%252F00839b3532e2216b0a7a29e972342d2a%253Futm_source%253D618%2522%252C%2522announcementCount%2522%253A1%252C%2522announcementExpire%2522%253A248980035%257D; UserName=DEmon_121; UserInfo=86cf88adf4b1425a8b961a15a90de606; UserToken=86cf88adf4b1425a8b961a15a90de606; UserNick=DEmon_121; AU=3A4; BT=1592463760489; p_uid=U000000; Hm_up_6bcd52f51e9b3dce32bec4a3997715ac=%7B%22islogin%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isonline%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isvip%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%2C%22uid_%22%3A%7B%22value%22%3A%22DEmon_121%22%2C%22scope%22%3A1%7D%7D; c_ref=https%3A//www.baidu.com/link; c_first_page=https%3A//blog.csdn.net/weixin_43213382/article/details/103225734; dc_tos=qc412b; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1592458965,1592463795,1592463892,1592463972; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1592463972'
        cookies = {i.split('=')[0]: i.split('=')[1] for i in cookies_temp.split('; ')}
        yield scrapy.Request(
            url=self.start_urls[0],
            callback=self.parse,
            cookies=cookies
        )




    def parse(self, response):
        print("==")
        print(re.findall('DEmon_121', response.body.decode()))
        yield scrapy.Request(
            url='https://blog.csdn.net/github_38589282/article/details/76735688?utm_medium=distribute.pc_relevant.none-task-blog-baidujs-8',
            callback=self.parse_detail,
            #cookies=response.request.cookies
        )

    def parse_detail(self,response):
        print("====")
        print(re.findall('DEmon_121',response.body.decode()))
        # yield scrapy.Request(
        #     url='https://blog.csdn.net/honglicu123/article/details/75453107?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-3.nonecase&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-3.nonecase',
        #     callback=self.parse_detail_more,
        #     #cookies=response.request.cookies
        # )

    # def parse_detail_more(self,response):
    #     img_url=response.xpath('//div[@class="user-img"]//@src').extract_first()
    #     print(re.findall('DEmon_121',response.body.decode()))
    #     yield scrapy.Request(
    #         img_url,
    #         callback=self.parse_detail_img
    #     )

    def parse_detail_img(self,response):
        with open('abc.jpg','wb') as f:
            f.write(response.body)
            f.close()
        print('图片下载成功')
        pass

    # def parse(self, response):
    #     # cookies_temp='uuid_tt_dd=10_20045694210-1584712573345-791920; dc_session_id=10_1584712573345.982694; __gads=ID=3d8dba977ff4a473:T=1584712574:S=ALNI_MaX0g_IJRs4sMJvBLMfj8dL5mkDvA; Hm_lvt_e5ef47b9f471504959267fd614d579cd=1586485265; Hm_ct_e5ef47b9f471504959267fd614d579cd=6525*1*10_20045694210-1584712573345-791920; __yadk_uid=MZm34JAZa1OIDecGgQfPimduknzygNVg; UN=DEmon_121; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=6525*1*10_20045694210-1584712573345-791920!5744*1*DEmon_121; dc_sid=19168fb88f49cee20cceaf388e91f4e6; TY_SESSION_ID=05a7b2ee-0075-4738-be8f-1853d26df3e0; c_first_ref=www.baidu.com; c_utm_source=blogxgwz2; aliyun_webUmidToken=T40E31D7A57341D6D1FF02511912682B5A8433961B88F4E05A0ABA94EEC; c_first_page=https%3A//blog.csdn.net/itgujing/article/details/82392179; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1590048836,1590056826,1590118490,1590133978; c_utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-2.nonecase; c_ref=https%3A//blog.csdn.net/itgujing/article/details/82392179; SESSION=bc4913ae-9ae7-491e-a01f-6256a48be70e; UserName=DEmon_121; UserInfo=a3a729cd595b4d84b94f941b21847a20; UserToken=a3a729cd595b4d84b94f941b21847a20; UserNick=DEmon_121; AU=3A4; BT=1590139224398; p_uid=U000000; Hm_up_6bcd52f51e9b3dce32bec4a3997715ac=%7B%22islogin%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isonline%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isvip%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%7D; announcement=%257B%2522isLogin%2522%253Atrue%252C%2522announcementUrl%2522%253A%2522https%253A%252F%252Fbss.csdn.net%252Fm%252Ftopic%252Flive_recruit%253Futm_source%253Dannounce0515%2522%252C%2522announcementCount%2522%253A0%252C%2522announcementExpire%2522%253A3600000%257D; dc_tos=qaq79s; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1590139217'
    #     # cookies={i.split('=')[0]:i.split('=')[1] for i in cookies_temp.split('; ')}
    #     print("==")
    #     print(re.findall('DEmon_121', response.body.decode()))
    #     yield scrapy.Request(
    #         'https://blog.csdn.net/github_38589282/article/details/76735688?utm_medium=distribute.pc_relevant.none-task-blog-baidujs-8',
    #         callback=self.parse_detail
    #     )
    #
    # def parse_detail(self,response):
    #     print("====")
    #     print(re.findall('DEmon_121',response.body.decode()))
    #     yield scrapy.Request(
    #         url='https://blog.csdn.net/honglicu123/article/details/75453107?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-3.nonecase&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-3.nonecase',
    #         callback=self.parse_detail_more
    #     )
    #
    # def parse_detail_more(self,response):
    #     print(re.findall('DEmon_121',response.body.decode()))






