# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import xlrd
import xlwt
from xlutils.copy import copy
from xlwt import Style

class ZhongguancunPipeline(object):
    row = 0
    def process_item(self, item, spider):
        rb = xlrd.open_workbook(u"手机数据信息.xlsx")
        wb = copy(rb)
        table = rb.sheet_by_name(u"手机数据信息")
        sheet = wb.get_sheet(0)
        self.row += 1
        sheet.write(self.row, 0, item['brand'])
        sheet.write(self.row, 1, item['name'])
        sheet.write(self.row, 2, item['price'])
        sheet.write(self.row, 3, item['cpu_model'])
        sheet.write(self.row, 4, item['cpu_frequency'])
        sheet.write(self.row, 5, item['gpu_model'])
        sheet.write(self.row, 6, item['ram'])
        sheet.write(self.row, 7, item['android_sdk'])
        sheet.write(self.row, 8, item['market_time'])
        sheet.write(self.row, 9, item['resolution'])
        sheet.write(self.row, 10, item['fingerprint'])
        wb.save(u"手机数据信息.xlsx")
        return item
