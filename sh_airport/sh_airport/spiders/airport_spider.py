import scrapy
from scrapy_splash import SplashRequest


def print_clean(f, data):
    data = data.replace(' ', '').replace('\n', '')
    if len(data) > 0:
        f.write(data + '\n')


def extract_clean(data):
    return data.replace(' ', '').replace('\n', '')


class AirportSpider(scrapy.Spider):
    name = "sh-airport"
    allowed_domains = ["shanghaiairport.com"]
    output_file = None
    script = """
        function main(splash, args)
          splash.images_enabled = false  
          assert(splash:go(args.url))
          assert(splash:wait(1))
          js = string.format("document.querySelector('#Pages > a.next').click();", args.page)
          splash:runjs(js)
          assert(splash:wait(5))
          return splash:html()
        end
    """

    def start_requests(self):
        self.output_file = open("result.txt", "w")
        yield SplashRequest("http://www.shanghaiairport.com:8081/cn/flights.html",
                            callback=self.parse, endpoint='execute',
                            args={'lua_source': self.script, 'page': 4, 'wait': 10})

    def parse(self, response):
        print_clean(self.output_file, "--------------------------------")
        for it in response.xpath("//*[@id=\"data\"]"):
            for it2 in it.xpath("tr"):
                for it3 in it2.xpath("td"):
                    for i in it3.xpath("text()").extract():
                        print_clean(self.output_file, i)
                    for j in it3.xpath("div[@class=\"HangBanID\"]/text()").extract():
                        print_clean(self.output_file, j)
                    for it4 in it3.xpath("div[@class=\"HangBan_list\"]/div/div/ul"):
                        flight_list = []
                        for it5 in it4.xpath("li/text()"):
                            data = extract_clean(it5.extract())
                            if data not in flight_list:
                                flight_list.append(data)
                        for k in flight_list:
                            print_clean(self.output_file, k)
                print_clean(self.output_file, "--------------------------------")

