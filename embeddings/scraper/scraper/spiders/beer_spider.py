import scrapy
import re
import json
from w3lib.html import remove_tags

class ShackBeerSpider(scrapy.Spider):
    name = 'shack-beer'
    start_urls = [
        'https://craftshack.com/collections/{}/'.format(beer) for beer in ['bottles', 'cans']
    ]

    def parse(self, response):
        page_btns = response.css('span.page').getall()
        if len(page_btns) == 0:
            page_count = 1
        else:
            match = re.search(r">(\d+)<", page_btns[-1])
            page_count = int(match.group(1))
        links = ['?page=' + str(i) for i in range(page_count)]
        yield from response.follow_all(links, callback=self.parse_collection)

    def parse_collection(self, response):
        yield from response.follow_all(css='a.grid-product__link', callback=self.parse_product)

    def parse_product(self, response):
        payload = response.xpath('//script[@id="tfx-product"]').get()
        rating = response.css('span.stamped-badge::attr(data-rating)').get()
        match = re.search(r"\{.*\}", payload)
        product = json.loads(match.group())
        raw_desc = remove_tags(product['description'])
        match = re.search(r"(\d*\.?\d*%) ABV", raw_desc)
        abv = match.group(1) if match is not None else None
        match = re.search(r"Commercial Description:\n*(.*)", raw_desc)
        desc = match.group(1) if match is not None else None
        yield {
            'name': remove_tags(product['title']),
            'price': product['price'] / 100,
            'abv': abv,
            'description': desc,
            'rating': rating,
            'url': response.request.url
        }

class ConnoBeerSpider(scrapy.Spider):
    name = 'conno-beer'
    start_urls = [
        'https://beerconnoisseur.com/search-beer?page={}'.format(i) for i in range(134)
    ]

    def parse(self, response):
        yield from response.follow_all(css='div.views-field-view-node a', callback=self.parse_product)

    def parse_product(self, response):
        yield {
            'name': response.css('div.field-name-title-field h1::text').get(),
            'price': None,
            'abv': response.css('div.field-name-field-abv div.even::text').get()[:-1],
            'description': response.css('div.field-name-body p::text').get(),
            'rating': response.css('div.views-field-field-judges-rating div::text').get(),
            'url': response.request.url
        }
