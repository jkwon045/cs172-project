# -*- coding: utf-8 -*-
import scrapy
import os

class GovspiderSpider(scrapy.Spider):
    name = 'govspider'


    def __init__(self, seed_file=None, page_count=None):
        allowed_domains = []
        if seed_file:
            with open(seed_file, 'r') as file:
                self.start_urls = file.read().splitlines()

            for domain in self.start_urls:
                allowed_domains.append(domain)
        else:
            allowed_domains = ['fda.gov']
            start_urls = ['https://www.fda.gov/']
        if page_count:
            scrapy.contrib.closespider.CloseSpider.CLOSESPIDER_PAGECOUNT = page_count

    def parse(self, response):
        for a in response.css('li a::attr(href)'):
            path_to_spider = os.path.dirname(os.path.abspath(__file__))+'/stored_files'
            filename_html = response.url.split("/")[-1] + '.html'
            filename = os.path.join(path_to_spider, filename_html)
            with open(filename, 'wb') as html_file:
                html_file.write(response.body)
            yield response.follow(a, callback=self.parse)
