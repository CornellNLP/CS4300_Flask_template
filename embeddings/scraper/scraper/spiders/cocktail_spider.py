import scrapy
import json
import re
from w3lib.html import remove_tags

class SpruceCocktailSpider(scrapy.Spider):
    name = 'spruce-cocktail'
    start_urls = [
        'https://www.thespruceeats.com/a-to-z-cocktail-recipes-3962886'
    ]

    def parse(self, response):
        for li in response.xpath('//div[contains(@class, "comp")]//li[not(@class)]'):
            a = li.css('a')[0]
            meta = li.css('::text').getall()
            name = meta[0]
            base = None
            if len(meta) > 1:
                raw_base = meta[1]
                base = re.search(r"\w+", raw_base).group()
            kwargs = {
                'name': name,
                'base': base
            }
            yield response.follow(a, callback=self.parse_product, cb_kwargs=kwargs)

    def parse_product(self, response, name, base):
        raw_desc = ' '.join(response.css('div#article__header--project_1-0 p').getall())
        desc = remove_tags(raw_desc).replace('\xa0', ' ')
        payload = response.xpath('//script[@id="schema-unified_1-0"]').get()
        product = json.loads(remove_tags(payload))
        rating = product['aggregateRating']['ratingValue']
        yield {
            'name': name,
            'base': base,
            'description': desc,
            'rating': rating + '/5' if rating is not None else None,
            'url': response.request.url
        }