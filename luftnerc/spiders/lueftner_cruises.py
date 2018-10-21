# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime


class LueftnerCruisesSpider(scrapy.Spider):
    name = 'lueftner-cruises'
    allowed_domains = ['www.lueftner-cruises.com']
    start_urls = [
        'https://www.lueftner-cruises.com/en/river-cruises/cruise.html'
    ]

    custom_settings = {
        "DOWNLOAD_DELAY": 6,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 10
    }

    def parse(self, response):
        for href in response.css('.travel-box-container .travel-box-heading \
                span.yearContainer a::attr(href)'):
            yield response.follow(href, self.parse_cruiselistitempage)

    # Search float in string
    def search4float(self, string_with_float):
        s = str(string_with_float).replace('\u20ac', '').replace(
            '.', '').replace(',', '.')
        return float(s)

    # Search int in string
    def search4int(self, string_with_int):
        s = string_with_int.split()[0]
        return int(s)

    def parse_cruiselistitempage(self, response):
        # Itinerary
        itinerary = []
        for routecity in response.css('span.route-city::text').extract():
            routecity_formatted = str(routecity).replace(' ', '').replace(
                '\n', '').strip().lower()
            itinerary.append(routecity_formatted)

        # Dates
        dates = []
        dates_dictionary = {}
        for priceduration in response.css(
                'div.accordeon-panel-default > div > a'):
            price_and_ship = {}
            #  Date precursor extract, split and obtain first element.
            #  Initial date format example is 24. Oct 2018.
            dateprecursor = priceduration.css(
                'span.price-duration::text').extract_first().split('-')[0].strip()
            date = datetime.strptime(dateprecursor, "%d. %b %Y").strftime(
                "%Y-%m-%d")

            pricestring = priceduration.css(
                'span.big-table-font::text').extract_first().strip()
            price = self.search4float(pricestring)

            price_and_ship['ship'] = priceduration.css(
                'span.table-ship-name::text').extract_first().lower()
            price_and_ship['price'] = price
            dates_dictionary[date] = price_and_ship

        dates.append(dates_dictionary)
        days = response.css('p.cruise-duration::text').extract_first().strip()
        yield{
            'name': response.css('h1::text').extract_first().strip(),
            'days': self.search4int(days),
            'itinerary': itinerary,
            'dates': dates,
        }
