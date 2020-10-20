from scrapy.core.downloader.handlers.http11 import TunnelError
from twisted.internet.error import (
    ConnectError,
    ConnectionDone,
    ConnectionLost,
    ConnectionRefusedError,
    DNSLookupError,
    TCPTimedOutError,
    TimeoutError,
)

try:
    response = 'asd'
    transaction_time = response.xpath('//p[@class="record_detail"]/text()').get()
    average_price = transaction_time.split(',')[0].replace('单价', '')
except AttributeError:
    raise TunnelError
