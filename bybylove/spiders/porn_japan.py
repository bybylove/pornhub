import scrapy
from selenium import webdriver
from bybylove.items import BybyloveItem
class Japan(scrapy.Spider):
    name = 'japan'

    def __init__(self):
        chrome_opt = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2,
                 "plugins.plugins_disabled": ['Adobe Flash Player'],}
        chrome_opt.add_experimental_option("prefs", prefs)
        self.browser = webdriver.Chrome('/Users/baijingwen/Downloads/chromedriver',chrome_options=chrome_opt)
        self.browser.set_page_load_timeout(150)

    def close(self,spider):
        self.browser.close()

    def start_requests(self):
        self.browser.delete_all_cookies()
        urls = [
            'https://www.pornhub.com/categories',

        ]
        for url in urls:
            yield scrapy.Request(url=url ,callback=self.parse)


    def parse(self, response):
        with open('result','wb') as f:
            f.write(response.body)
        urlfollows = response.xpath('/html/body/div[8]/div/div[3]/div/div[2]/ul/li/div/a/@href').extract()
        for url in urlfollows:
            fullurl = 'https://pornhub.com' + url
            yield scrapy.Request(url = fullurl,callback=self.parse1)

    def parse1(self, response):
        item = BybyloveItem()
        item['type'] = response.xpath('/html/body/div[10]/div/div[5]/div/div[1]/h1/text()').extract()[0]
        urlfollows = response.xpath('/html/body/div[10]/div/div[5]/div/ul/li/div/div[1]/div[2]/a/@href').extract()
        for url in urlfollows:
            fullurl = 'https://pornhub.com' + url
            yield scrapy.Request(url = fullurl,callback=self.parse2,meta={'item':item})
        nextpage = response.xpath('/html/body/div[10]/div/div[9]/ul/li[@class = "page_next"]/a/@href').extract()[0]
        newpage = 'https://pornhub.com' + nextpage
        yield scrapy.Request(url = newpage,callback=self.parse1)

    def parse2(self, response):

        url = response.css('video').xpath('source/@src').extract()[0]
        name = response.xpath('/html/body/div[11]/div/div[4]/div[2]/div[3]/h1/span/text()').extract()[0]
        item = response.meta['item']
        item['name'] = ''
        item['url'] = ''
        item['name'] = name
        item['url'] = url
        yield  item


