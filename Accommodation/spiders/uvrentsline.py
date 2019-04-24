# -*- coding: utf-8 -*-
import scrapy


class UvrentslineSpider(scrapy.Spider):
    name = 'uvrentsline'
    allowed_domains = ['www.uvrentsline.com']
    start_urls = ['https://www.uvrentsline.com/']

    def parse(self, response):
        frmdata = {'action': 'submit-advanced-search',
                    'max': 'all',
                    'n': '1',
                    'priceHigh': '10000',
                    'sortOrder': 'PriceLowToHigh'}
        url = "https://www.uvrentsline.com/page/advanced-search"
        yield scrapy.http.FormRequest(url, callback=self.parse_search_page, formdata=frmdata)
    
    def parse_search_page(self, response):
        urls = response.css('.adtitle a::attr(href)').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_post)

    def parse_post(self, response):
        yield {
            'url': response.url,
            'price': self.extract_price(response),
            'lat': None,
            'long': None,
            'beds':  self.extract_beds(response),
            'area': None,
            'furnished': self.extract_furnished(response),
            'available': self.extract_availablity(response)
        }

    def extract_price(self, response):
        h3s = response.css('h3').extract()
        for h3 in h3s:
            if 'Rent' in h3:
                tokens = h3.split()
                rate = 1
                if 'weekly' in tokens:
                    rate = 4
                for token in tokens:
                    if '$' in token:
                        return rate * int(token[1:])
        return None

    def extract_beds(self, response):
        h3s = response.css('h3').extract()
        for h3 in h3s:
            if 'Bedrooms' in h3:
                start = h3.rfind(':') + 2
                end = h3.rfind('<')
                return int(h3[start:end])
        return None

    def extract_availablity(self, response):
        spans = response.css('span').extract()
        for span in spans:
            if 'Status:' in span:
                start = span.rfind('-') + 2
                end = span.rfind('strong') - 2
                return span[start:end]
        return None

    def extract_furnished(self, response):
        divs = response.css('div').extract()
        for div in divs:
            if div.count('div') == 2 and 'Furnished' in div and 'img' in div and 'alt=' in div:
                tokens = div.split()
                for token in tokens:
                    if 'alt=' in token:
                        if 'Yes' in token:
                            return True
                        elif 'No' in token:
                            return False
        return None
