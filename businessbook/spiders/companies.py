# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy import Request


class CompaniesSpider(Spider):
    name = 'companies'
    allowed_domains = ['businessbook.pk/']
    start_urls = ['https://www.businessbook.pk//']

    def parse(self, response):
        categories = response.xpath('//li[@class="horizontalLayout list-inline-item"]/a/@href').extract()
        for category in categories:
            yield Request(category, callback=self.parse_category, dont_filter=True)

    def parse_category(self, response):
        companies = response.xpath('//div[@class="card-body"]/div[@class="row default-view"]/div[@class="col-sm-3"]/div[@class="row col-sm-12"]')
        for company in companies:
            company_name = company.xpath('.//a/@title').extract_first()
            url = company.xpath('.//a/@href').extract_first()

            yield Request(url, callback=self.parse_company, dont_filter=True, meta={'company_name': company_name})

        next = response.xpath('//a[@rel="next"]/@href').extract_first()
        if next:
            yield response.follow(next)

    def parse_company(self, response):
        website_url = response.xpath('//div[@class="card card-default card-flip"]/ul[@class="list-group"]/li[@class="list-group-item"]/a/@href').extract_first()
        yield {
            'Company_name': response.meta['company_name'],
            'Website': website_url
        }
