# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter
import csv

HEADRS = ['district','transaction_house','transaction_time','transaction_area','total_price','average_price','storey','deco','house_url','agent_name','career_years','agent_location','agent_rank','agent_url']


class LianjiaBeijingPipeline:
    def __init__(self):
        self.fp = open('Lianjia_price_20201016.csv', 'a')
        self.writer = csv.writer(self.fp)
        self.writer.writerow(HEADRS)

    def process_item(self, item, spider):
        self.writer.writerow(item.values())
        return item

    def close_file(self, item, spider):
        self.fp.close()
