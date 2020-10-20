import scrapy
import time
from selenium import webdriver


HOUSE_URLS=list()

class MainSpiderSpider(scrapy.Spider):
    global HOUSE_URLS
    name = 'main_spider'
    allowed_domains = ['domain.com.au']
    start_urls = ['https://www.domain.com.au/sale/vic/']

    def parse(self, response):
        
        main_urls=


        print(HOUSE_URLS)




# urls=response.xpath('//a[@rel="noopener"]/@href')
#         for url in urls:
#             url=url.get()
#             if 'https://www.domain.com.au' in str(url) and url not in HOUSE_URLS:
#                 HOUSE_URLS.append(url)

