# -*- coding: utf-8 -*-
import scrapy


class Places4studentsSpider(scrapy.Spider):
    name = 'places4students'
    allowed_domains = ['www.places4students.com']
    start_urls = ['https://www.places4students.com/Places/PropertyListings?SchoolID=jKylFPwtNwo%3d']
    base_url = 'https://www.places4students.com'

    def start_requests(self):
        print('%%%%%')
        yield scrapy.Request(self.start_urls[0], cookies={'Places4StudentDisclaimer':'Agree'}, callback=self.parse)

    def parse(self, response):
        urls = response.css(".listing-title a::attr(href)").extract()
        # TODO
