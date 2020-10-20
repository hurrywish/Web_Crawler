import scrapy
import time
from selenium import webdriver
import re
from RealAustralia.items import RealaustraliaItem

HOUSE_URLS = list()


class MainSpiderSpider(scrapy.Spider):
    global HOUSE_URLS
    name = 'main_spider'
    allowed_domains = ['domain.com.au']
    start_urls = ['https://www.domain.com.au/sold-listings/melbourne-region-vic/?excludepricewithheld=1&page=1']

    def parse(self, response):
        for i in range(1, 51):
            main_page_urls = 'https://www.domain.com.au/sold-listings/melbourne-region-vic/?excludepricewithheld=1&page={}'
            main_page_url = main_page_urls.format(str(i))
            yield scrapy.Request(url=main_page_url, callback=self.parse_main_page)

    def parse_main_page(self, response):
        house_urls = response.xpath('//a[@rel="noopener"]/@href')
        for house_url in house_urls:
            house_url = house_url.get()
            if 'https://www.domain.com.au' in house_url and house_url not in HOUSE_URLS:
                HOUSE_URLS.append(house_url)
                yield scrapy.Request(url=house_url, callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        status_price = response.xpath('//div[contains(@data-testid,"summary-title")]/text()').get()
        # status = re.search(r'(.*) - \$(.*)', status_price).group(1)
        status = response.xpath('//span[contains(@data-testid,"listing-tag")]/text()').get()
        price = re.search(r'(.*) - \$(.*)', status_price).group(2).replace(',', '')

        property_features = response.xpath('//div[@data-testid="property-features-wrapper"]')
        bedroom = property_features.xpath('.//span[1]/span[1]/text()').get()
        bathroom = property_features.xpath('.//span[2]/span[1]/text()').get()
        carpark = property_features.xpath('.//span[3]/span[1]/text()').get()
        area = property_features.xpath('.//span[4]/span[1]/text()').get()

        if 'm²' in str(bedroom):
            area = bedroom
            bedroom = None


        type = response.xpath('//div[contains(@data-testid,"property-type")]//text()').get()
        type = re.sub(' ', '', type)

        address = response.xpath('//div[@class="listing-details__copy-text"]//text()').get()
        try:
            zipcode = re.search(r'.*VIC (.*)', address).group(1)
        except:
            zipcode = None

        house_url = response.url

        agent_url1 = response.xpath('//div[contains(@data-testid,"agent-details-agent")]/a/@href').get()
        agent_url2 = response.xpath('//a[contains(@class,"agent-details-agent-name")]/@href').get()


        agent_company_url = response.xpath('//a[contains(@class,"agent-company-name")]/@href').get()



        if agent_url1:
            agent_url = agent_url1
            information = {
                'information': (status, price, bedroom, bathroom, carpark, area, type, address, zipcode, house_url)}
            yield scrapy.Request(url=agent_url, callback=self.parse_agent_page, meta=information)
        elif agent_url2:
            agent_url = agent_url2
            information = {
                'information': (status, price, bedroom, bathroom, carpark, area, type, address, zipcode, house_url)}
            yield scrapy.Request(url=agent_url, callback=self.parse_agent_page, meta=information)
        elif agent_company_url:
            agent_name=response.xpath('//h3[contains(@class,"agent-details-agent-name")]/text()').get()
            agent_url = agent_company_url
            information = {
                'information': (status, price, bedroom, bathroom, carpark, area, type, address, zipcode, house_url,agent_name)}
            yield scrapy.Request(url=agent_url, callback=self.parse_company_page, meta=information)
        else:
            agent_name = None
            agent_position = None
            agent_company = None
            agent_sale = None
            agent_phone = None
            agent_location = None
            agent_url = None
            packed_items = [status, price, bedroom, bathroom, carpark, area, type, address, zipcode, house_url,
                            agent_name, agent_position, agent_company, agent_sale, agent_phone, agent_location,
                            agent_url]
            items = self.yield_item(packed_items)
            yield items

    def parse_agent_page(self, response):

        status, price, bedroom, bathroom, carpark, area, type, address, zipcode, house_url = response.meta[
            'information']

        agent_name = response.xpath('//h2[@data-testid="agent-profiles__title"]//text()[2]').get()
        agent_position = response.xpath('//p[contains(@data-testid,"agent-job-position")]/text()[1]').get()
        agent_company = response.xpath('//h2[contains(@data-testid,"agency-details-name")]/text()').get()
        agent_sale = response.xpath('//p[@data-testid="trade-sales-summary__stat"]/text()').get()
        agent_phone = response.xpath('//span[contains(@data-testid,"phone-number")]/text()').get()
        agent_location = response.xpath('//span[contains(@data-testid,"address__label")]//text()').getall()
        agent_location=''.join(agent_location).strip()
        #agent_location = re.sub(r'\n|\s| ', '', agent_location)
        agent_url = response.url

        packed_items = [status, price, bedroom, bathroom, carpark, area, type, address, zipcode, house_url,
                        agent_name, agent_position, agent_company, agent_sale, agent_phone, agent_location,
                        agent_url]
        items = self.yield_item(packed_items)
        yield items

    def parse_company_page(self, response):
        status, price, bedroom, bathroom, carpark, area, type, address, zipcode, house_url,agent_name = response.meta[
            'information']


        agent_position = None
        agent_company = response.xpath('//*[@data-testid="trade-profile-hero-section__name"]/text()').get()
        agent_sale = None
        agent_phone = None
        agent_location = response.xpath('//span[@data-testid="address__label"]//text()').get()
        agent_url = response.url
        packed_items = [status, price, bedroom, bathroom, carpark, area, type, address, zipcode, house_url,
                        agent_name, agent_position, agent_company, agent_sale, agent_phone, agent_location,
                        agent_url]
        items = self.yield_item(packed_items)
        yield items

    def yield_item(self, packed_items):

        items = RealaustraliaItem(
            status=packed_items[0],
            price=packed_items[1],
            bedroom=packed_items[2],
            bathroom=packed_items[3],
            carpark=packed_items[4],
            area=packed_items[5],
            type=packed_items[6],
            address=packed_items[7],
            zipcode=packed_items[8],
            house_url=packed_items[9],

            agent_name=packed_items[10],
            agent_position=packed_items[11],
            agent_company=packed_items[12],
            agent_sale=packed_items[13],
            agent_phone=packed_items[14],
            agent_location=packed_items[15],
            agent_url=packed_items[16]
        )
        return items
