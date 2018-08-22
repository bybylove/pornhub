# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class BybylovePipeline(object):
    def __init__(self):
        self.client = pymysql.connect(
            host = '127.0.0.1',
            port = 3306,
            user = 'root',
            passwd = '0477Jiafanyu',
            charset = 'utf8',
            database = 'pornhub'
        )
        self.cur = self.client.cursor()
    def process_item(self, item, spider):
        try:
            sql = "INSERT INTO video(name,category,url) VALUES (%s,%s,%s)"
            lis = (item['name'], item['type'], item['url'])
            self.cur.execute(sql, lis)
            self.client.commit()
        except BaseException as e:
            pass
        return item
    def __del__(self):
        self.cur.close()
        self.client.close()