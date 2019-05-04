# -*- coding: utf-8 -*-
import scrapy


class GovspiderSpider(scrapy.Spider):
    name = 'govspider'
    allowed_domains = ['fda.gov']
    start_urls = ['https://www.fda.gov/']

   # def start_requests(self):
    #	for url in self.start_urls:
    #		yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
    	page = response.url.split("/")[-2]
    	filename = './pages/%s.html' % page
    	with open(filename, 'wb') as f:
    		f.write(response.body)
    	self.log('Saved file %s' % filename)
    	for a in response.css('li a::attr(href)'):
    		yield response.follow(a, callback=self.parse)
    	#for a in response.css('li.next a'):
    	#	yield scrapy.Request(response.follow(a, callback=self.parse))
