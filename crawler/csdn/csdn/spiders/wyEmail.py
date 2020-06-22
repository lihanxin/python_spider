# -*- coding: utf-8 -*-
import scrapy
import re

class WyemailSpider(scrapy.Spider):
    name = 'wyEmail'
    allowed_domains = ['163.com']
    start_urls = ['http://163.com/']
    def start_requests(self):
        cookies_temp = '_ntes_nnid=e7b30eeccc95a758bfa2b4f1fdf97ef4,1583991432993; _ntes_nuid=e7b30eeccc95a758bfa2b4f1fdf97ef4; vinfo_n_f_l_n3=cb676056be0601fe.1.0.1585389540411.0.1585389637345; starttime=; NTES_SESS=Fz97XUC2kq_Dvb8wd83rfYceo5M7jGeSE9oZ93BQGw3wEox_E6mDyt65Xr3XMNPsKSUR1dx1Zg6V6kCvoXtfjPzO89g53L_KXRNXkDu6quUzmonH7Zszd02Oi7Ggc7q.KGd4QhpyYn25.22ML_67soBGDiITlyCwyPxlT4De1rMoQ1Ho2zPJor39Lfwi5qL7uJbBL6E.DPlIJwCqPsXmiJ6VBbw8Zdwkx; S_INFO=1590228257|0|3&80##|m18898601264; P_INFO=m18898601264@163.com|1590228257|0|mail163|00&99|null&null&null#gud&440300#10#0#0|188264&1||18898601264@163.com; nts_mail_user=18898601264@163.com:-1:1; df=mail163_letter; mail_upx=t1bj.mail.163.com|t2bj.mail.163.com|t3bj.mail.163.com|t4bj.mail.163.com|t2bj.mail.163.com|t3bj.mail.163.com|t4bj.mail.163.com|t1bj.mail.163.com; mail_upx_nf=; mail_idc=; Coremail=c5893550364ef%VAfEjJJdUErxZJnfbRddojvXNPgOXPHC%g3a19.mail.163.com; MAIL_MISC=m18898601264; cm_last_info=dT1tMTg4OTg2MDEyNjQlNDAxNjMuY29tJmQ9aHR0cHMlM0ElMkYlMkZtYWlsLjE2My5jb20lMkZqczYlMkZtYWluLmpzcCUzRnNpZCUzRFZBZkVqSkpkVUVyeFpKbmZiUmRkb2p2WE5QZ09YUEhDJnM9VkFmRWpKSmRVRXJ4WkpuZmJSZGRvanZYTlBnT1hQSEMmaD1odHRwcyUzQSUyRiUyRm1haWwuMTYzLmNvbSUyRmpzNiUyRm1haW4uanNwJTNGc2lkJTNEVkFmRWpKSmRVRXJ4WkpuZmJSZGRvanZYTlBnT1hQSEMmdz1odHRwcyUzQSUyRiUyRm1haWwuMTYzLmNvbSZsPS0xJnQ9LTEmYXM9dHJ1ZQ==; MAIL_SESS=Fz97XUC2kq_Dvb8wd83rfYceo5M7jGeSE9oZ93BQGw3wEox_E6mDyt65Xr3XMNPsKSUR1dx1Zg6V6kCvoXtfjPzO89g53L_KXRNXkDu6quUzmonH7Zszd02Oi7Ggc7q.KGd4QhpyYn25.22ML_67soBGDiITlyCwyPxlT4De1rMoQ1Ho2zPJor39Lfwi5qL7uJbBL6E.DPlIJwCqPsXmiJ6VBbw8Zdwkx; MAIL_SINFO=1590228257|0|3&80##|m18898601264; MAIL_PINFO=m18898601264@163.com|1590228257|0|mail163|00&99|null&null&null#gud&440300#10#0#0|188264&1||18898601264@163.com; secu_info=1; mail_entry_sess=60c0b0965ef57b9630f9cd7e5148b1209822b65db766c5bd46814568ef908ef2ef2ddb8801455ab11f865f1efe44eafd79b8ab3530458eb78bc81733c6d2f4612e6e76510385acbdd1f9495ba7944f7c296859cbf15b6bbedea5f5185d85fe2c343690e431f444d639de3a6cee04aaaa3adcd9ce97161ac63c7aa93690a4cb8450fd0c0fd48109b6df342276dc924e6fdf0e0c4606d55e55107e38e11c9f7f3eaf7065a9c4ddfa37cc7336812d7b8893e1152ef034b7ff2dfd3c00dd6cb3240a; locale=; face=js6; mail_style=js6; mail_uid=m18898601264@163.com; mail_host=mail.163.com; Coremail.sid=VAfEjJJdUErxZJnfbRddojvXNPgOXPHC; JSESSIONID=A8255FDB7CFF5C9237EFAF97A582A469'
        cookies = {i.split('=')[0]: i.split('=')[1] for i in cookies_temp.split('; ')}
        yield scrapy.Request(
            url='https://mail.163.com/js6/main.jsp?sid=VAfEjJJdUErxZJnfbRddojvXNPgOXPHC',
            callback=self.parse,
            cookies=cookies
        )

    def parse(self, response):
        # cookies_temp='uuid_tt_dd=10_20045694210-1584712573345-791920; dc_session_id=10_1584712573345.982694; __gads=ID=3d8dba977ff4a473:T=1584712574:S=ALNI_MaX0g_IJRs4sMJvBLMfj8dL5mkDvA; Hm_lvt_e5ef47b9f471504959267fd614d579cd=1586485265; Hm_ct_e5ef47b9f471504959267fd614d579cd=6525*1*10_20045694210-1584712573345-791920; __yadk_uid=MZm34JAZa1OIDecGgQfPimduknzygNVg; UN=DEmon_121; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=6525*1*10_20045694210-1584712573345-791920!5744*1*DEmon_121; dc_sid=19168fb88f49cee20cceaf388e91f4e6; TY_SESSION_ID=05a7b2ee-0075-4738-be8f-1853d26df3e0; c_first_ref=www.baidu.com; c_utm_source=blogxgwz2; aliyun_webUmidToken=T40E31D7A57341D6D1FF02511912682B5A8433961B88F4E05A0ABA94EEC; c_first_page=https%3A//blog.csdn.net/itgujing/article/details/82392179; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1590048836,1590056826,1590118490,1590133978; c_utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-2.nonecase; c_ref=https%3A//blog.csdn.net/itgujing/article/details/82392179; SESSION=bc4913ae-9ae7-491e-a01f-6256a48be70e; UserName=DEmon_121; UserInfo=a3a729cd595b4d84b94f941b21847a20; UserToken=a3a729cd595b4d84b94f941b21847a20; UserNick=DEmon_121; AU=3A4; BT=1590139224398; p_uid=U000000; Hm_up_6bcd52f51e9b3dce32bec4a3997715ac=%7B%22islogin%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isonline%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isvip%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%7D; announcement=%257B%2522isLogin%2522%253Atrue%252C%2522announcementUrl%2522%253A%2522https%253A%252F%252Fbss.csdn.net%252Fm%252Ftopic%252Flive_recruit%253Futm_source%253Dannounce0515%2522%252C%2522announcementCount%2522%253A0%252C%2522announcementExpire%2522%253A3600000%257D; dc_tos=qaq79s; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1590139217'
        # cookies={i.split('=')[0]:i.split('=')[1] for i in cookies_temp.split('; ')}
        print("==")
        print(re.findall('汉鑫', response.body.decode()))
        yield scrapy.Request(
            url='https://reg1.vip.163.com/newReg1/?from=new_mailtop_163&utm_source=new_mailtop_163',
            callback=self.parse_detail,
        )

    def parse_detail(self, response):
        print("====")
        print(re.findall('18898601264', response.body.decode()))
        # yield scrapy.Request(
        #     url='https://blog.csdn.net/honglicu123/article/details/75453107?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-3.nonecase&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-3.nonecase',
        #     callback=self.parse_detail_more,
        #     #cookies=response.request.cookies
        # )
