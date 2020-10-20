# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv

HEADERS = ['status',
          'price',
          'bedroom',
          'bathroom',
          'carpark',
          'area',
          'type',
          'address',
          'zipcode',
          'house_url',

          'agent_name',
          'agent_position',
          'agent_company',
          'agent_sale',
          'agent_phone',
          'agent_location',
          'agent_url'
          ]


class RealaustraliaPipeline:

    def __init__(self):
        self.fp = open('RealAustralia_20201017.csv', 'a')
        self.writer = csv.writer(self.fp)
        self.writer.writerow(HEADERS)

    def process_item(self, item, spider):
        self.writer.writerow(item.values())
        return item

    def close_file(self, item, spider):
        self.fp.close()
