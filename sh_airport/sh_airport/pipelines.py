# coding=utf-8
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import json
import codecs
import os

# todo: 定时爬取
# todo: 计划起飞折线图 每小时
# todo: 实际起飞折线图
# todo: 晚点情况折线图

class ShAirportPipeline:

    def __init__(self):
        self.file = codecs.open('sh-airport.json', 'w', encoding='utf-8')
        self.file.write("[\n")

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.seek(-2, os.SEEK_END)
        self.file.truncate()
        self.file.seek(0, os.SEEK_END)
        self.file.write('\n]')
        self.file.close()
