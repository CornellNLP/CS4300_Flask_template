import scrapy
import re
import json
from w3lib.html import remove_tags

class KWLiquorSpider(scrapy.Spider):
    name = 'kw-liquor'
    def start_requests(self):
            urls = [
                "https://www.kandwliquor.com/spirits/?page={}".format(i) for i in range(36)
            ]
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        yield from response.follow_all(css='table[class*="wf_content"] a', callback=self.parse_product)

    def parse_product(self, response):
        origin_type = response.css('a[class*=prodlink]::text').getall()
        # Extract origin and liquor type
        if len(origin_type) >= 3:
            type = origin_type[2]
        else:
            type = origin_type[1]
        # Extract description if present
        description_words = response.css('div.prod_detail p::text').getall()
        if len(description_words) > 1:
            description = description_words[1]
        else:
            description = None
        yield {
        'name' : response.css('h1::text').get(),
        'price' : response.css('span[itemprop*="price"]::text').get(),
        'abv' : None,
        'description' : description,
        'rating' : None,
        'origin' : origin_type[0],
        'type' : type,
        'url' : response.request.url
        }
