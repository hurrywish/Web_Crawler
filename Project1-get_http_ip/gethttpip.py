import requests
from bs4 import BeautifulSoup
from queue import Queue
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# preliminary settings（User-Agent, Proxy，Queue) 请求头、初始IP、队列设定
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}
PROXIES = {'http': 'http://221.180.170.104:8080'}
IP_list = Queue(100000)


# Component1: retrieving all the HTTP/IP from a website  从网站中取得HTTP/IP
class Get_main_page:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.url = 'https://ip.ihuan.me/address/5Lit5Zu9.html?page=b97827cc'  # This is the website provides free HTTP/IP
        self.IP_list = IP_list

    def run(self):
        i = 1  # This is for settings how many pages you want to crawl 想要爬取的页数
        while i <= 5:
            i += 1
            self.parse_page(self.url)
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//ul[@class="pagination"]//li[last()]/a')))
            except:
                self.driver.refresh()
                self.driver.refresh()
            self.NextBtn = self.driver.find_element(By.XPATH, '//ul[@class="pagination"]//li[last()]/a')
            self.NextBtn.click()
            self.url = self.driver.current_url

    # This is for getting the info from website page 从网页中爬取所需信息
    def parse_page(self, url):
        self.driver.get(url)
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        trs = soup.find_all('tr')[1:]
        for tr in trs:
            IP = tr.find_all('a')[0].text
            Port = tr.find_all('td')[1].text
            HTTPS = tr.find_all('td')[4].text
            Addr = tr.find_all('a')[3].text
            Secret = tr.find_all('td')[6].text
            # print(IP, Port, HTTPS, Addr, Secret, 'Under testing')
            self.IP_list.put((IP, Port, HTTPS, Addr, Secret))


# Component2: testing all the HTTP/IP   测试从网站中取得的HTTP/IP
class Web_test:
    def __init__(self):
        self.IP_list = IP_list
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}
        self.url = 'https://www.fang.com/SoufunFamily.htm'  # This is the url you want to ping 想要ping的网址

    def run(self):

        while True:
            try:
                IP, Port, HTTPS, Addr, Secret = self.IP_list.get()
                if HTTPS == '不支持':
                    proxies = {'http': 'http://%s:%s' % (IP, Port)}
                else:
                    proxies = {'https': 'https://%s:%s' % (IP, Port)}
                    resp = requests.get(url=self.url, headers=self.headers, proxies=proxies, timeout=5)
            except:
                print(IP, Port, 'Timeout')

            else:
                print('IP:', IP, 'PORT:', Port, 'HTTPS:', HTTPS, 'ADDR:', Addr, 'ADDR:', Secret, "is Available")


if __name__ == '__main__':
    t1 = threading.Thread(target=Get_main_page().run())
    t1.start()

    t2 = threading.Thread(target=Web_test().run())
    for i in range(100):
        t2.start()
