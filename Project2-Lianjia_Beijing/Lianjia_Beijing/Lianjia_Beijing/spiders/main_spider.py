import scrapy
import re
import requests
from lxml import etree
from Lianjia_Beijing.items import LianjiaBeijingItem


class MainSpiderSpider(scrapy.Spider):
    name = 'main_spider'
    allowed_domains = ['lianjia.com']
    start_urls = ['https://bj.lianjia.com/chengjiao/']

    def parse(self, response):
        a_labels = response.xpath('//div[@data-role="ershoufang"]/div//a')
        for a_label in a_labels:
            url = a_label.xpath('./@href').get()
            url = response.urljoin(url)
            district = a_label.xpath('./text()').get()
            # print(url,district)
            yield scrapy.Request(url=url, callback=self.parse_district_page, meta={'info': district})

    def parse_district_page(self, response):
        district = response.meta['info']
        total_page = response.xpath('//div[contains(@class,"house-lst-page-box")]/@page-data').get()
        page_number = re.search('{"totalPage":(.*?),"curPage":1', total_page).group(1)
        page_number = int(page_number)
        # print(page_number)
        for i in range(2, page_number):
            next_page_url = response.url + 'pg' + str(i) + '/'
            yield scrapy.Request(url=next_page_url, callback=self.get_detail_url, meta={'info': district})

    def get_detail_url(self, response):
        district = response.meta['info']
        lis = response.xpath('//ul[@class="listContent"]//li')
        for li in lis:
            detail_url = li.xpath('./a/@href').get()
            yield scrapy.Request(url=detail_url, callback=self.parse_detail_page, meta={'info': district})

    def parse_detail_page(self, response):
        district = response.meta['info']

        record_detail = response.xpath('//p[@class="record_detail"]/text()').get()

        try:
            average_price = record_detail.split(',')[0].replace('单价', '')
            transaction_time = record_detail.split(',')[1].replace('成交', '')
        except:
            average_price = None
            transaction_time = None
            print(response.text)
            with open('error_price.txt', 'a') as fp:
                fp.write(response.text)
                fp.write('\n'+'==' * 30+'\n')

        wrapper = response.xpath('//div[@class="wrapper"]/text()').get()
        transaction_house = wrapper.split(' ')[0]
        transaction_area = wrapper.split(' ')[2]

        storey = response.xpath('//div[@class="content"]/ul//li[2]/text()').get().strip()
        try:
            storey = re.search(r'(.*?)\(', storey).group(1)
        except:
            pass

        deco = response.xpath('//div[@class="content"]/ul//li[9]/text()').get().strip()
        # deco = re.search('装修情况(.*)',deco).group(1)

        total_price1 = response.xpath('//span[@class="dealTotalPrice"]/i/text()').get()
        total_price2 = response.xpath('//span[@class="dealTotalPrice"]/text()').get()
        total_price = total_price1 + total_price2

        house_url = response.url

        agent_url_part1 = response.url.split('chengjiao/')[0]
        agent_url_part2 = 'chengjiao/display?hid='
        agent_url_part3 = response.url.split('chengjiao/')[-1].replace('.html', '')
        agent_url = agent_url_part1 + agent_url_part2 + agent_url_part3
        information = {'information': (
            district, transaction_house, transaction_time, transaction_area, total_price, average_price, storey, deco,
            house_url)}

        yield scrapy.Request(url=agent_url, callback=self.parse_middle_page, meta=information)

    def parse_middle_page(self, response):
        district, transaction_house, transaction_time, transaction_area, total_price, average_price, storey, deco, house_url = \
            response.meta['information']
        information = response.meta
        try:
            agent_id = re.search(r'agentUcid":"(\w+?)"', str(response.body)).group(1)
            agent_url = 'https://dianpu.lianjia.com/' + str(agent_id) + '/'
            # print(agent_url)
            yield scrapy.Request(url=agent_url, callback=self.parse_agent, meta=information)
        except:
            agent_name = None
            career_years = None
            agent_location = None
            agent_rank = None
            agent_url = None
            item = LianjiaBeijingItem(
                district=district,
                transaction_house=transaction_house,
                transaction_time=transaction_time,
                transaction_area=transaction_area,
                total_price=total_price,
                average_price=average_price,
                storey=storey,
                deco=deco,
                house_url=house_url,
                agent_name=agent_name,
                career_years=career_years,
                agent_location=agent_location,
                agent_rank=agent_rank,
                agent_url=agent_url
            )
            yield item

    def parse_agent(self, response):
        district, transaction_house, transaction_time, transaction_area, total_price, average_price, storey, deco, house_url = \
            response.meta['information']
        try:
            agent_name = response.xpath('//span[@class="agent-name"]/text()').get()
            agent_location = response.xpath('//span[@class="map-text"]/text()').get()
            career_years = response.xpath('//span[@class="info-item-value"]/text()').getall()[0]
            agent_rank = response.xpath('//span[@class="pub-tag"]/text()').get()
            agent_url = response.url
            #print(agent_name, agent_location)
        except:
            agent_name = None
            agent_location = None
            career_years = None
            agent_rank = None
            agent_url = None
            with open('error_agent.txt', 'a') as fp:
                fp.write(response.text)
                fp.write('\n' + '==' * 30 + '\n')

        item = LianjiaBeijingItem(
            district=district,
            transaction_house=transaction_house,
            transaction_time=transaction_time,
            transaction_area=transaction_area,
            total_price=total_price,
            average_price=average_price,
            storey=storey,
            deco=deco,
            house_url=house_url,
            agent_name=agent_name,
            career_years=career_years,
            agent_location=agent_location,
            agent_rank=agent_rank,
            agent_url=agent_url)
        yield item
