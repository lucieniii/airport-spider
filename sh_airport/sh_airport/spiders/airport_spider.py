# coding=utf-8

import scrapy
import time
from selenium import webdriver
from scrapy.selector import Selector
from sh_airport.items import ShAirportItem
import random
from fake_useragent import UserAgent


def print_clean(f, data):
    if not data:
        return ''
    data = data.replace(' ', '').replace('\n', '')
    if len(data) > 0:
        f.write(data + '\n')


def extract_clean(data):
    if not data:
        return ''
    return data.replace(' ', '').replace('\n', '')


class AirportSpider(scrapy.Spider):
    name = "sh-airport"
    allowed_domains = ["shanghaiairport.com"]
    start_urls = ["http://www.shanghaiairport.com:8081/cn/flights.html"]
    output_file = None

    def parse(self, response):
        option = webdriver.ChromeOptions()
        option.add_argument("--user-agent=" + UserAgent().random)
        # 启动远程driver
        driver = webdriver.Remote("http://123.57.46.218:4444/wd/hub", desired_capabilities=webdriver.DesiredCapabilities.CHROME, options=option)
        driver.get(response.url)
        time.sleep(10 + 10 * random.random())
        items = []
        while True:
            # 提取数据
            html = driver.page_source
            for it in Selector(text=html).xpath("//*[@id=\"data\"]/tr"):
                item = ShAirportItem()
                item["plan_departure_time"] = extract_clean(it.xpath("td[@class=\"TD1\"]/text()").extract_first())
                item["main_flight_id"] = extract_clean(it.xpath("td[@class=\"TD2\"]/div[@class=\"HangBanID\"]/text()").extract_first())
                item["airline"] = extract_clean(it.xpath("td[@class=\"TD3\"]/text()").extract_first())
                item["terminal"] = extract_clean(it.xpath("td[@class=\"TD4\"]/text()").extract_first())
                item["destination_via"] = extract_clean(it.xpath("td[@class=\"TD5\"]/text()").extract_first())
                item["check_in"] = extract_clean(it.xpath("td[@class=\"TD6\"]/text()").extract_first())
                item["actual_departure_time"] = extract_clean(it.xpath("td[@class=\"TD7\"]/text()").extract_first())
                flight_list = []
                for it1 in it.xpath("td[@class=\"TD2\"]/div[@class=\"HangBan_list\"]/div/div/ul"):
                    for it2 in it1.xpath("li/text()"):
                        data = extract_clean(it2.extract())
                        if data not in flight_list:
                            flight_list.append(data)
                item["sub_flight_id"] = flight_list
                items.append(item)
            # 翻页
            try:
                next_page = driver.find_element_by_css_selector('#Pages > a.next')
                next_page.click()
                time.sleep(10 + 10 * random.random())
            except:
                break
        return items

