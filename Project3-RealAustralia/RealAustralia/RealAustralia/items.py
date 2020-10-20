# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RealaustraliaItem(scrapy.Item):
    status=scrapy.Field()
    price = scrapy.Field()
    bedroom = scrapy.Field()
    bathroom = scrapy.Field()
    carpark = scrapy.Field()
    area=scrapy.Field()
    type=scrapy.Field()
    address = scrapy.Field()
    zipcode = scrapy.Field()
    house_url = scrapy.Field()

    agent_name = scrapy.Field()
    agent_position = scrapy.Field()
    agent_company = scrapy.Field()
    agent_sale = scrapy.Field()
    agent_phone = scrapy.Field()
    agent_location = scrapy.Field()
    agent_url = scrapy.Field()