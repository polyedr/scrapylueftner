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

    def parse(self,response):
        for href in response.css('.travel-box-container .travel-box-heading span.yearContainer a::attr(href)'):
            yield response.follow(href,self.parse_cruiselistitempage)

    def parse_cruiselistitempage(self,response):
        yield{
            'name': response.css('h1::text').extract_first().strip(),
            'days': response.css('p.cruise-duration::text').extract_first().strip(),
            'itinenary': response.css('span.route-city::text').extract(),
            'dates': response.css('span.price-duration::text').extract(),
        }
