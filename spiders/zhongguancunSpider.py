# -*- coding:utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import log
import scrapy
import urllib
import os
import re
import xlrd
import xlwt
from xlutils.copy import copy
from xlwt import Style
import sys

from zhongguancun.items import ZhongguancunItem

# reload(sys)
# sys.setdefaultencoding('utf-8')

class ZhongguancunSpider(Spider):
    brand_list = [u"三星",u"vivo",u"华为",u"中兴",u"OPPO",u"苹果",u"LG",u"荣耀",u"金立",u"魅族",u"华硕",u"TCL",u"酷派",u"大神",u"努比亚",
    u"Moto",u"神舟",u"索尼移动",u"飞利浦",u"360",u"诺基亚",u"乐视",u"一加",u"小米",u"HTC",u"美图",u"锤子科技",u"联想",u"黑莓",u"联想ZUK",
    u"8848",u"海信",u"小辣椒",u"微软",u"朵唯",u"谷歌",u"ivvi",u"奇酷",u"中国移动",u"长虹",u"SUGAR",u"乐目",u"酷比",u"天语",u"夏普",u"康佳",
    u"纽曼",u"格力",u"国美",u"Gigaset金阶",u"MANN",u"21克",u"蓝魔",u"云狐",u"惠普",u"AGM",u"海尔",u"青橙",u"PPTV",u"邦华",u"YotaPhone",u"VEB",
    u"优豊",u"imoo",u"先锋",u"sonim",u"意龙",u"COMIO",u"innos",u"独影天幕",u"波导",u"朗界",u"新石器",u"小格雷",u"Antone",u"传奇",u"垦鑫达",
    u"华度",u"阿尔卡特",u"青想",u"彩石",u"米蓝",u"首云",u"领虎",u"富可视",u"青葱",u"卡布奇诺",u"图灵",u"manta",u"柯达",u"汇威",u"Acer宏碁",
    u"松下",u"爱我",u"百事",u"超多维",u"明基",u"阔密",u"全普",u"百合",u"泛泰",u"TP-LINK",u"美猴王",u"易百年",u"索野",u"小宇宙",u"IUNI",u"BROR",
    u"VAIO",u"途为",u"雅马亚虎",u"卓普",u"读书郎",u"言信",u"VANO",u"同洲",u"宝丽来",u"天禄",u"POMP",u"原点",u"100+",u"veaka",u"福满多",u"长虹",
    u"小采",u"果壳电子",u"E人E本",u"美莱仕",u"优护",u"火凤凰",u"德赛",u"为美",u"橙石",u"nibiru",u"大Q",u"直角",u"78点",u"VOTO",u"锋达通",
    u"欧恩",u"山寨手机",u"佳通",u"港利通",u"高斯贝尔",u"盛隆",u"普莱达",u"华录",u"VEVA",u"i-mate",u"斐讯",u"迪士尼",u"伟恩",u"现代手机",
    u"齐乐",u"迪奥",u"盛泰",u"高新奇",u"首派",u"诺亚信",u"唯科",u"豪特",u"欧博信",u"altek",u"金鹏",u"CECT",u"摩西",u"首信",u"夏新",u"戴尔",
    u"天丽",u"技嘉",u"富士通",u"爱国者",u"华银",u"经纬",u"东芝",u"MOPS",u"卓拉",u"卡西欧",u"Yahoo",u"BFB",u"Getac",u"影驰",u"DigiTalk",u"夏朗",
    u"美迪欧",u"亿通",u"万利达",u"奥克斯",u"多普达",u"Palm",u"衡天越",u"优派",u"NO.1",u"UT斯达康",u"创维",u"恒基伟业",u"优珀",u"中天",
    u"艾美讯",u"O2",u"弘谷电",u"京瓷",u"宇达电通MIO",u"英华达",u"七喜",u"佳域",u"摩奇",u"Intel",u"Runbo",u"大可乐",u"优思",u"大唐电信",
    u"INQ",u"华信",u"欧盛",u"和信",u"欧新",u"友派",u"seals",u"网尔",u"iwoo",u"欧谷",u"东信",u"首亿",u"优美"]

    name = "zhongguancun"
    start_urls = [
        #OPPO,VIVO,华为,荣耀,小米
        # "http://detail.zol.com.cn/cell_phone_advSearch/subcate57_1_m1795-m613-m1673-m50840-m34645-s1398-s7074-s6500-s6502-s6106_1_1__1.html?#showc",
        #全部
        "http://detail.zol.com.cn/cell_phone_advSearch/subcate57_1_m98-m1795-m613-m642-m1673-m544-m143-m50840-m1632-m1434-m227-m171-m1606-m36761-m35005-m295-m35615-m1069-m159-m35350-m297-m33992-m35579-m34645-m33080-m35179-m35849-m1763-m12772-m37319-m49202-m19-m35320-m364-m33855-m1922-m37427-m37121-m33626-m1589-m35224-m34492-m34023-m32729-m300-m599-m1081-m750-m52602-m34773-m35121-m35228-m1050-m34547-m223-m34660-m221-m34857-m36791-m34906-m36511-m34686-m37438-m51710-m342-m33668-m51808-m35004-m34741-m52034-m355-m40737-m37433-m51558-m51576-m41107-m34874-m37585-m531-m49477-m51194-m36594-m51281-m51978-m36409-m34927-m36647-m49232-m36538-m139-m35335-m218-m84-m37131-m49825-m49354-m407-m51107-m50842-m41933-m1528-m174-m37263-m41365-m36792-m35147-m35611-m43188-m50829-m50865-m49221-m1826-m33767-m51993-m51417-m32161-m713-m35491-m35358-m35430-m35361-m35419-m35420-m35398-m35213-m35208-m34275-m35342-m37279-m38442-m36631-m35958-m36555-m35638-m36347-m36819-m36379-m34050-m33477-m33382-m33303-m33249-m33248-m33247-m33243-m33242-m33139-m33096-m33084-m33540-m34038-m34010-m34004-m33977-m33969-m33968-m33964-m33941-m33936-m33926-m33912-m33878-m33665-m32893-m826-m807-m715-m563-m21-m34594-m234-m283-m29-m34566-m34884-m209-m34523-m34538-m321-m34691-m34571-m34126-m35012-m34520-m34069-m34056-m34096-m1071-m34584-m1041-m515-m34099-m314-m34966-m1074-m1591-m341-m34590-m32887-m32795-m32780-m32730-m486-m1806-m1602-m23-m34866-m34901-m125-m35029-m35000-m34986-m32512-m34391-m34208-m34200-m34207-m34298-m34369-m34679-m34677-m34639-m34487-m828-m34445-m34794-s1398-s7074-s6500-s6502-s6106_1_1__1.html?#showc",
        #灯塔
        # "http://detail.zol.com.cn/cell_phone_advSearch/subcate57_1_m98-m1795-m613-m642-m1673-m50840-m1632-m1434-m1606-m35005-m35350-m33992-m35579-m34645-m35179-m35849-m1763-m37319-m19-m35320-m33626-m599-m33936-s1398-s7074-s6500-s6502-s6106_1_1__1.html?#showc"
        #dana
        # "http://detail.zol.com.cn/cell_phone_advSearch/subcate57_1_s7235-s6472-p29978_1_1_0_1.html?#showc"
    ]  #start url at the first page

    wb = xlwt.Workbook()
    sheet = wb.add_sheet(u"手机数据信息", cell_overwrite_ok=True)
    sheet.write(0, 0, u"品牌")
    sheet.write(0, 1, u"手机全称")
    sheet.write(0, 2, u"价格")
    sheet.write(0, 3, u"CPU型号")
    sheet.write(0, 4, u"CPU频率")
    sheet.write(0, 5, u"GPU型号")
    sheet.write(0, 6, u"内存")
    sheet.write(0, 7, u"Android_SDK")
    sheet.write(0, 8, u"上市时间")
    sheet.write(0, 9, u"分辨率")
    sheet.write(0, 10, u"指纹识别设计")
    wb.save(u"手机数据信息.xlsx")

    # total = 0

    #第一层链接，获取手机全称，价格，参数链接
    def parse(self, response):
        first = Selector(response)
        links = first.xpath('//*[@id="result_box"]/div[2]/ul').extract()[0]
        # print links
        links_cnt = links.count("dl")
        links_length = links_cnt/2
        # print links_length
        for i in range(1,int(links_length+1)):
            # self.total += 1
            name = first.xpath('//*[@id="result_box"]/div[2]/ul/li['+str(i)+']/dl/dt/a/text()').extract()[0]
            try:
                price = first.xpath('//*[@id="result_box"]/div[2]/ul/li['+str(i)+']/div[2]/span[1]/b[2]/text()').extract()[0]
            except IndexError as e:
                price = first.xpath('//*[@id="result_box"]/div[2]/ul/li['+str(i)+']/div[2]/span/b/text()').extract()[0]
            try:
                new_url = first.xpath('//*[@id="result_box"]/div[2]/ul/li['+str(i)+']/dl/dd[1]/div/ul[3]/li[3]/a/@href').extract()[0]
                url = "http://detail.zol.com.cn" + new_url
                yield scrapy.Request(url, meta = {'name':name, 'price':price}, callback=self.parse_parameter)
            except Exception as e:
                pass

        #下一页链接
        results = first.xpath('//*[@id="result_box"]/div[1]/p').extract()[0]
        results_cnt = results.count("span")
        results_length = results_cnt/2
        try:
            if results_length == 1:
                next_url = first.xpath('//*[@id="result_box"]/div[1]/p/span/a')
                next_url_text = next_url.xpath('text()').extract()[0]
                next_url_link = next_url.xpath('@href').extract()[0]
            else:
                next_url = first.xpath('//*[@id="result_box"]/div[1]/p/span[2]/a')
                next_url_text = next_url.xpath('text()').extract()[0]
                next_url_link = next_url.xpath('@href').extract()[0]
            url = "http://detail.zol.com.cn" + next_url_link
            yield scrapy.Request(url,callback=self.parse)
        except IndexError as e:
            pass
        # print self.total

    #第二层链接，获取每种手机参数
    def parse_parameter(self, response):
        item = ZhongguancunItem()
        name = response.meta['name']
        price = response.meta['price']
        brand = ""
        cpu_model = ""
        cpu_frequency = ""
        gpu_model = ""
        ram = ""
        android_sdk = ""
        market_time = ""
        resolution = ""
        fingerprint = ""

        second = Selector(response)
        try:
            #硬件
            for hardware_index in range(1,10):
                hardware_info = second.xpath('//*[@id="newTb"]/table[4]/tr/td/div/ul/li['+str(hardware_index)+']/span[1]/text()').extract()[0]
                if hardware_info == u"CPU型号":
                    try:
                        cpu_model = second.xpath('//*[@id="newTb"]/table[4]/tr/td/div/ul/li['+str(hardware_index)+']/span[2]/text()').extract()[0]
                    except Exception as e:
                        cpu_model = second.xpath('//*[@id="newTb"]/table[4]/tr/td/div/ul/li['+str(hardware_index)+']/span[2]/a/text()').extract()[0]
                elif hardware_info == u"CPU频率":
                    try:
                        cpu_frequency = second.xpath('//*[@id="newTb"]/table[4]/tr/td/div/ul/li['+str(hardware_index)+']/span[2]/text()').extract()[0]
                    except Exception as e:
                        cpu_frequency = second.xpath('//*[@id="newTb"]/table[4]/tr/td/div/ul/li['+str(hardware_index)+']/span[2]/a/text()').extract()[0]
                elif hardware_info == u"GPU型号":
                    try:
                        gpu_model = second.xpath('//*[@id="newTb"]/table[4]/tr/td/div/ul/li['+str(hardware_index)+']/span[2]/text()').extract()[0]
                    except Exception as e:
                        gpu_model = second.xpath('//*[@id="newTb"]/table[4]/tr/td/div/ul/li['+str(hardware_index)+']/span[2]/a/text()').extract()[0]
                elif hardware_info == u"RAM容量":
                    try:
                        ram = second.xpath('//*[@id="newTb"]/table[4]/tr/td/div/ul/li['+str(hardware_index)+']/span[2]/text()').extract()[0]
                    except Exception as e:
                        ram = second.xpath('//*[@id="newTb"]/table[4]/tr/td/div/ul/li['+str(hardware_index)+']/span[2]/a/text()').extract()[0]
                elif hardware_info == u"操作系统":
                    try:
                        android_sdk = second.xpath('//*[@id="newTb"]/table[4]/tr/td/div/ul/li['+str(hardware_index)+']/span[2]/text()').extract()[0]
                    except Exception as e:
                        android_sdk = second.xpath('//*[@id="newTb"]/table[4]/tr/td/div/ul/li['+str(hardware_index)+']/span[2]/a/text()').extract()[0]
        except IndexError as e:
            pass

        try:
            #基本参数
            for base_parameter_index in range(1,10):
                base_parameter_info = second.xpath('//*[@id="newTb"]/table[1]/tr/td/div/ul/li['+str(base_parameter_index)+']/span[1]/text()').extract()[0]
                if base_parameter_info == u"上市日期":
                    try:
                        market_time = second.xpath('//*[@id="newTb"]/table[1]/tr/td/div/ul/li['+str(base_parameter_index)+']/span[2]/text()').extract()[0]
                    except Exception as e:
                        market_time = second.xpath('//*[@id="newTb"]/table[1]/tr/td/div/ul/li['+str(base_parameter_index)+']/span[2]/a/text()').extract()[0]
        except IndexError as e:
            pass

        try:
            #屏幕
            for screen_index in range(1,10):
                screen_info = second.xpath('//*[@id="newTb"]/table[2]/tr/td/div/ul/li['+str(screen_index)+']/span[1]/text()').extract()[0]
                if screen_info == u"主屏分辨率":
                    try:
                        resolution = second.xpath('//*[@id="newTb"]/table[2]/tr/td/div/ul/li['+str(screen_index)+']/span[2]/text()').extract()[0]
                    except Exception as e:
                        resolution = second.xpath('//*[@id="newTb"]/table[2]/tr/td/div/ul/li['+str(screen_index)+']/span[2]/a/text()').extract()[0]
        except IndexError as e:
            pass

        try:
            #外观
            for surface_index in range(1,10):
                surface_info = second.xpath('//*[@id="newTb"]/table[6]/tr/td/div/ul/li['+str(surface_index)+']/span[1]/text()').extract()[0]
                if surface_info == u"指纹识别设计":
                    try:
                        fingerprint = second.xpath('//*[@id="newTb"]/table[6]/tr/td/div/ul/li['+str(surface_index)+']/span[2]/text()').extract()[0]
                    except Exception as e:
                        fingerprint = second.xpath('//*[@id="newTb"]/table[6]/tr/td/div/ul/li['+str(surface_index)+']/span[2]/a/text()').extract()[0]
        except IndexError as e:
            pass
        
        for i in self.brand_list:
            if name.startswith(i):
                brand = i

        item['brand'] = brand
        item['name'] =  name
        item['price'] = price
        item['cpu_model'] = cpu_model
        item['cpu_frequency'] = cpu_frequency
        item['gpu_model'] = gpu_model
        item['ram'] = ram
        item['android_sdk'] = android_sdk
        item['market_time'] = market_time
        item['resolution'] = resolution
        item['fingerprint'] = fingerprint

        yield item

        