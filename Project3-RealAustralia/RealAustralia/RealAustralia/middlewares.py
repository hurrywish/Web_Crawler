# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from scrapy import signals
import random
import requests
from scrapy.downloadermiddlewares.retry import RetryMiddleware
import logging
from fake_useragent import UserAgent
from scrapy.http import HtmlResponse
from scrapy.utils.response import response_status_message
import time
from scrapy.exceptions import NotConfigured
from selenium import webdriver


class RealaustraliaDownloaderMiddleware:
    def __init__(self):
        self.options = webdriver.ChromeOptions()

        # for Centos
        # self.options.add_argument("--headless")
        # self.options.add_argument('--disable-gpu')
        # self.options.add_argument('--no-sandbox')

        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)
        # for Centos
        self.driver = webdriver.Chrome(options=self.options)

        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
        })

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        self.driver.get(request.url)
        # self.driver.implicitly_wait(10)
        source = self.driver.page_source
        response = HtmlResponse(url=self.driver.current_url, body=source, request=request, encoding='utf-8')
        return response

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
