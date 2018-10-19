# -*- coding: utf-8 -*-
import scrapy


class LueftnerCruisesSpider(scrapy.Spider):
    name = 'lueftner-cruises'
    allowed_domains = ['www.lueftner-cruises.com']
    start_urls = ['https://www.lueftner-cruises.com/en/river-cruises/cruise.html']

    custom_settings = {
        "DOWNLOAD_DELAY": 6,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 10
    }
    """
    def parse(self, response):
       for cruiseitem in response.css('.travel-box-container .cruise-list-item'):
           yield {
               'name': response.css('.travel-box-heading a::text').extract_first(),
               'days': response.css('p.cruise-duration::text').extract_first(),
           }
    """
    def parse(self,response):
        for href in response.css('.travel-box-container .travel-box-heading a::attr(href)'):
            #print("Response: href")
            yield response.follow(href,self.parse_cruiselistitempage)
            

    def parse_cruiselistitempage(self,response):
        def extract_with_css(query):
            try:
               return response.css(query)
            except:
                return 0
            
        yield{
            'name': response.css('h1::text').extract_first().strip(),
            'days': response.css('p.cruise-duration::text').extract_first().strip(),
            'itinenary': response.css('.route-city span::text'),
            'dates': response.css('span.price-duration::text').extract_first().strip(),
        }

#'//div[@class="cruise-list-item"]//div[@class="travel-box-heading"]/span/a/text()'
