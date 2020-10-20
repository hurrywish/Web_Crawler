# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
import requests
from scrapy.downloadermiddlewares.retry import RetryMiddleware
import logging
from fake_useragent import UserAgent
from scrapy.utils.response import response_status_message
import time
from scrapy.exceptions import NotConfigured

PROXIES = ['tps185.kdlapi.com:15818']


class Retry(RetryMiddleware):
    # global PROXIES
    def __init__(self, settings):
        super().__init__(settings)
        if not settings.getbool('RETRY_ENABLED'):
            raise NotConfigured
        self.max_retry_times = 10
        self.retry_http_codes = set(int(x) for x in settings.getlist('RETRY_HTTP_CODES'))
        self.priority_adjust = settings.getint('RETRY_PRIORITY_ADJUST')
        self.logger = logging.getLogger(__name__)

    def process_response(self, request, response, spider):

        if request.meta.get('dont_retry', False):
            return response

        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            self.logger.warning('错误！！！' + str(reason))
            # url = "https://dps.kdlapi.com/api/getdps/?orderid=900257417255019&num=1&pt=1&sep=2"
            # time.sleep(round(random.uniform(0, 1), 1))
            # resp = requests.get(url)
            # resp = resp.text.split('\n')
            # PROXIES = resp
            time.sleep(round(random.uniform(0, 1), 1))
            #PROXIES = ['tps185.kdlapi.com:15818']
            print(PROXIES)

            return self._retry(request, reason, spider) or response

        judge_text = response.xpath('//p[@class="record_detail"]/text()').get()
        if not judge_text and '人机身份认证' in response.text:
            reason = response_status_message(response.status)
            print('已被反爬识别！！！', 'error_url:', str(response.url))
            time.sleep(round(random.uniform(30, 60), 1))
            #PROXIES = ['tps185.kdlapi.com:15818']
            print(PROXIES)

            return self._retry(request,reason, spider) or response


        return response

    def process_exception(self, request, exception, spider):
        global PROXIES
        if (
                isinstance(exception, self.EXCEPTIONS_TO_RETRY)
                and not request.meta.get('dont_retry', False)
        ):
            print('错误！！！' + str(exception))
            time.sleep(round(random.uniform(0, 1), 1))
            # url = "https://dps.kdlapi.com/api/getdps/?orderid=900257417255019&num=1&pt=1&sep=2"
            # resp = requests.get(url)
            # resp = resp.text.split('\n')
            #PROXIES = resp
            #PROXIES=['tps185.kdlapi.com:15818']
            print(PROXIES)
            return self._retry(request, exception, spider)


# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class LianjiaBeijingSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.

        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class LianjiaBeijingDownloaderMiddleware:
    global PROXIES
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

        #time.sleep(round(random.uniform(0, 1), 1))
        User_Agent = [
            'Mozilla/5.0 CK={} (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763',
            'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:45.0) Gecko/20100101 Firefox/45.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'

        ]

        user_agent = random.choice(User_Agent)
        request.headers['User-Agent'] = user_agent

        proxy = random.choice(PROXIES)
        proxy = 'https://' + proxy
        request.meta['proxy'] = proxy

        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        # global PROXIES
        # judge_text = response.xpath('//p[@class="record_detail"]/text()').get()
        # if not judge_text and '人机身份认证' in response.text:
        #     print('已被反爬识别！！！', 'error_url:', str(response.url))
        #     time.sleep(round(random.uniform(60, 120), 1))
        #     # url = "https://dps.kdlapi.com/api/getdps/?orderid=900257417255019&num=1&pt=1&sep=2"
        #     # resp = requests.get(url)
        #     # resp = resp.text.split('\n')
        #     # PROXIES = resp
        #     PROXIES = ['tps185.kdlapi.com:15818']
        #     new_request = request.copy()
        #     new_request = new_request.replace(url=request.url)
        #     print(PROXIES)
        #
        #     return new_request

        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        #
        # global PROXIES
        # if '6' in str(exception):
        #     url = "http://dps.kdlapi.com/api/getdps/?orderid=900257417255019&num=1&pt=1&sep=1"
        #     resp = requests.get(url)
        #     resp = resp.text
        #     print(resp, str(exception))
        #     PROXIES = [resp]
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

# class ProcessAllExceptionMiddleware(object):
#     def process_exception(self, request, exception, spider):
#         global PROXIES
#         if '61' in str(exception) or '503' in str(exception):
#             url = "http://dps.kdlapi.com/api/getdps/?orderid=900257417255019&num=1&pt=1&sep=1"
#             resp = requests.get(url)
#             resp = resp.text
#             print(resp,str(exception))
#             PROXIES = [resp]
#
#         return request
#         # proxy = random.choice(PROXIES)
#         # proxy = 'http://' + proxy
#         # request.meta['proxy'] = proxy
