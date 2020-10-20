# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaBeijingItem(scrapy.Item):
    district = scrapy.Field()
    transaction_house = scrapy.Field()
    transaction_time = scrapy.Field()
    transaction_area = scrapy.Field()
    total_price = scrapy.Field()
    average_price = scrapy.Field()
    storey=scrapy.Field()
    deco=scrapy.Field()
    house_url=scrapy.Field()


    agent_name = scrapy.Field()
    career_years = scrapy.Field()
    agent_location = scrapy.Field()
    agent_rank = scrapy.Field()
    agent_url = scrapy.Field()

