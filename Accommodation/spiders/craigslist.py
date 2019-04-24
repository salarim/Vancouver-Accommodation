# -*- coding: utf-8 -*-
import scrapy


class CraigslistSpider(scrapy.Spider):
    name = 'craigslist'
    allowed_domains = ['vancouver.craigslist.org']
    start_urls = ['https://vancouver.craigslist.org/d/apts-housing-for-rent/search/apa']
    base_url = 'https://vancouver.craigslist.org'

    def parse(self, response):
        urls = response.css(".result-row .result-info .result-title::attr(href)").extract()
        next_url = self.base_url + response.css(".button.next::attr(href)").extract_first()

        for url in urls:
            yield scrapy.Request(url, callback=self.parse_post)

        yield scrapy.Request(next_url, callback=self.parse)

    def parse_post(self, response):
        yield {
            'url': response.url,
            'price': self.extract_price(response.css('.price::text').extract_first()),
            'lat': response.css('#map::attr(data-latitude)').extract_first(),
            'long': response.css('#map::attr(data-longitude)').extract_first(),
            'beds':  self.extract_substring(response.css('.postingtitle .housing::text').extract_first(), 'br'),
            'area': self.extract_substring(response.css('.postingtitle .housing::text').extract_first(), 'ft'),
            'furnished': self.check_furnished(response),
            'available': self.extract_availablity(response)
        }

    def extract_price(self, s):
        if '$' in s:
            return int(s[1:])
        return None

    def extract_substring(self, s, substrng):
        if s is None:
            return None
        res = None
        for x in s.split():
            if substrng in x:
                res = int(x[:-2])
        return res

    def check_furnished(self, response):
        tags = ' '.join(response.css('.attrgroup span::text').extract())
        title = response.css('.postingtitle #titletextonly::text').extract_first()
        body = ' '.join(response.css('#postingbody::text').extract())
        txt = tags + ' ' + title + ' ' + body
        txt = txt.lower()
        if 'furnished' in txt and 'unfirnished' not in txt:
            return True
        return False 

    def extract_availablity(self, response):
        x = response.css('.attrgroup .housing_movein_now::text').extract_first()
        if x is None or 'available' not in x:
            return None
        return x[10:]



        