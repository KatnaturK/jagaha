import scrapy
from jagaha.items import JagahaItem
from scrapy.spiders import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.selector import HtmlXPathSelector
from urlparse import urljoin
import urlparse
import time 
import datetime

from requests.auth import HTTPProxyAuth

class JagahaSpider(Spider):
    name = "jspy"
    allowed_domains = ['jagaha.com']

    start_urls = [
            'http://www.jagaha.com/SearchProperty/GetSearchProperties?_escaped_fragment_PropertyType=Office&TransactionType=Buy&PlaceId=ChIJwe1EZjDG5zsRaYxkjY_tpF0&LocationName=Mumbai%2C-Maharashtra%2C-India&Lat=19.0759837&Lng=72.87765590000004&MinPrice=0&MaxPrice=0&MinArea=0&MaxArea=0&Page=1&PropertyTypeIds=&AmenityIds=&OwnershipIds=&Keyword=%5E&ImmediatePossession=false&IsDragMap=false&NorthEastLatAX=0&NorthEastLongAY=0&SouthWestLatCX=0&SouthWestLongCY=0',
            'http://www.jagaha.com/SearchProperty/GetSearchProperties?_escaped_fragment_PropertyType=Office&TransactionType=Lease&PlaceId=ChIJwe1EZjDG5zsRaYxkjY_tpF0&LocationName=Mumbai%2C-Maharashtra%2C-India&Lat=19.0759837&Lng=72.87765590000004&MinPrice=0&MaxPrice=0&MinArea=0&MaxArea=0&Page=1&PropertyTypeIds=&AmenityIds=&OwnershipIds=&Keyword=%5E&ImmediatePossession=false&IsDragMap=false&NorthEastLatAX=0&NorthEastLongAY=0&SouthWestLatCX=0&SouthWestLongCY=0',  
            'http://www.jagaha.com/SearchProperty/GetSearchProperties?_escaped_fragment_PropertyType=Retial&TransactionType=Lease&PlaceId=ChIJwe1EZjDG5zsRaYxkjY_tpF0&LocationName=Mumbai%2C-Maharashtra%2C-India&Lat=19.0759837&Lng=72.87765590000004&MinPrice=0&MaxPrice=0&MinArea=0&MaxArea=0&Page=1&PropertyTypeIds=&AmenityIds=&OwnershipIds=&Keyword=%5E&ImmediatePossession=false&IsDragMap=false&NorthEastLatAX=0&NorthEastLongAY=0&SouthWestLatCX=0&SouthWestLongCY=0',  
            'http://www.jagaha.com/SearchProperty/GetSearchProperties?_escaped_fragment_PropertyType=Retial&TransactionType=Buy&PlaceId=ChIJwe1EZjDG5zsRaYxkjY_tpF0&LocationName=Mumbai%2C-Maharashtra%2C-India&Lat=19.0759837&Lng=72.87765590000004&MinPrice=0&MaxPrice=0&MinArea=0&MaxArea=0&Page=1&PropertyTypeIds=&AmenityIds=&OwnershipIds=&Keyword=%5E&ImmediatePossession=false&IsDragMap=false&NorthEastLatAX=0&NorthEastLongAY=0&SouthWestLatCX=0&SouthWestLongCY=0'
        ]
    base_url = 'http://www.jagaha.com'
    custom_settings = {
            'BOT_NAME': 'jagaha',
            'DEPTH_LIMIT': 1000,
            'DOWNLOAD_DELAY': 3
        }
    start_time = time.time()
    data_id_list = []

    def parse(self,response):
        hxs = Selector(response)
        path = "//div[@id='content']/ul/li/div"
        x = hxs.xpath(path)
        url = response.url.split('_escaped_fragment_')[1].split('&')
        for i in x:
            if ' Mumbai' in i.xpath('div[2]/span/text()').extract_first().split(','):
                if 'Navi' not in i.xpath('div[2]/span/text()').extract_first().split(','):
                    data_id = i.xpath('../@data-id').extract()
                    if data_id not in self.data_id_list:
                        self.data_id_list.append(data_id)
                        item = JagahaItem()
                        item['data_id'] = i.xpath('../@data-id').extract()
                        item['data_time'] = time.strftime("%d/%m/%Y")
                        time.sleep(2)
                        item['platform'] = 'jagaha'
                        item['city'] = 'Mumbai'
                        txn_property = i.xpath('div/b/text()').extract_first()
                        if 'Per' in  i.xpath('a/div/span[1]/text()').extract_first().split(' '):
                            item['txn_type'] = 'Lease'
                            item['selling_price'] = '---'
                            item['monthly_rent'] = i.xpath('a/div/span[1]/text()').extract_first()
                        else:
                            item['txn_type'] = 'Buy'
                            item['selling_price'] = i.xpath('a/div/span[1]/text()').extract_first()
                            item['monthly_rent'] = '---'
                        item['lat'] = i.xpath('input[1]/@value').extract_first().split(' ')[0]
                        item['lng'] = i.xpath('input[1]/@value').extract_first().split(' ')[1]
                        item['google_place_id'] = i.xpath('input[3]/@value').extract_first()
                        item['building_name'] = i.xpath('div/span/text()').extract_first().split(',')[0]
                        item['area'] = i.xpath('a/div/span[2]/text()').extract_first()
                        item['location'] = i.xpath('div/span/text()').extract_first()
                        d_url = urljoin(self.base_url, i.xpath('a/@href').extract_first())
                        yield Request(d_url, callback=self.parse_item,  meta={'item': item}, dont_filter = True)
                    
        max_page = int(x.xpath("../../../div[last()]/ul/span/text()").extract_first().split(' ')[-1])
        count = int(url[10].split('=')[-1]) 
        page_num = count + 1
        url[10] = 'Page={page_num}'.format(page_num=page_num)
        url = 'http://www.jagaha.com/SearchProperty/GetSearchProperties?_escaped_fragment_' + '&'.join(url)
        if page_num < max_page:
            yield Request(url, callback=self.parse)
            
    def parse_item(self, response):
        hxs = Selector(response)
        item = response.meta['item']
        path = "//div[@id='propertydetailwrapper']/div[3]/div"
        x = hxs.xpath(path)
        
        item['desc'] = x.xpath('div[2]/p[2]/text()').extract_first()
        item['property_type'] = x.xpath('div[3]/div[2]/span/text()').extract_first()
        item['furnished'] = x.xpath('div[3]/div[4]/span/text()').extract_first()
        item['immediate_possession'] = x.xpath('div[3]/div[5]/span/text()').extract_first()
        item['age'] = x.xpath('div[3]/div[7]/span/text()').extract_first()
        item['locality'] = x.xpath('div[2]/p[4]/strong/text()').extract_first()
        yield item
     
