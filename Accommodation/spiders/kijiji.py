# -*- coding: utf-8 -*-
import scrapy
import re


class KijijiSpider(scrapy.Spider):
    name = 'kijiji'
    allowed_domains = ['www.kijiji.ca']
    start_urls = ['https://www.kijiji.ca/b-real-estate/vancouver/c34l1700287']
    base_url = 'https://www.kijiji.ca'

    def parse(self, response):
        urls = response.css(".search-item a::attr(href)").extract()
        next_url = self.base_url + response.css("a[title=Next]::attr(href)").extract_first()

        for url in urls:
            yield scrapy.Request(self.base_url + url, callback=self.parse_post)
        if next_url:
            yield scrapy.Request(next_url, callback=self.parse)

    def parse_post(self, response):
        yield {
            'url': response.url,
            'price': self.extract_price(response),
            'lat': response.css('meta[property="og:latitude"]::attr(content)').extract_first(),
            'long': response.css('meta[property="og:longitude"]::attr(content)').extract_first(),
            'beds':  self.extract_beds(response),
            'area': None,
            'furnished': self.extract_furnished(response),
            'available': None,
        }

    def extract_price(self, response):
        price = response.css('span[class^="currentPrice"] span::text').extract_first()[1:]
        if price:
            return int(float(price.replace(",", "")))
        return None

    def extract_beds(self, response):
        attrs = response.css('ul[class^="itemAttributeList"] dl').extract()
        for attr in attrs:
            if 'Bedrooms' in attr:
                return int(re.search('>[0-9]+<', attr).group()[1:-1])
        desc = response.css('div[class^="descriptionContainer"] p::text').extract_first()
        x = re.search('[0-9]+ bedroom', desc.lower())
        if x:
            return int(x.group()[:-8])
        return None

    def extract_furnished(self, response):
        attrs = response.css('ul[class^="itemAttributeList"] dl').extract()
        for attr in attrs:
            if 'Furnished' in attr:
                if '>No<' in attr:
                    return False
                elif '>Yes<' in attr:
                    return True
        desc = response.css('div[class^="descriptionContainer"] p::text').extract_first().lower()
        if 'unfirnished' in desc:
            return False
        if 'firnished' in desc:
            return True
        return None
