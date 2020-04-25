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

class TLSLiquorSpider(scrapy.Spider):
    name = 'tls-liquor'
    def start_requests(self):
            urls = [
                "https://www.theliquorstorejacksonhole.com/spirits/?page={}&sortby=sort_item_order&item_type=spirits".format(i) for i in range(32)
            ]
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        yield from response.follow_all(css='a[class="rebl15"]', callback=self.parse_product)

    def parse_product(self, response):
        prod_data = response.css('a[class="prodlink"]::text').getall()
        # Extract origin and liquor type
        if len(prod_data) >= 3:
            type = prod_data[2]
        elif len(prod_data) >= 2:
            type = prod_data[1]
        else:
            type = None
        regex = r"\d+.*\d*%"
        # Extract abv if present
        raw_abv_data = response.css('td[class="prodata_txt"]::text').getall()
        abv = None
        for data in raw_abv_data:
            match = re.search(regex, data)
            abv = match.group(0) if match is not None else None
        # Extract price
        sale_re = r"Sale price:\s*(\$\d+.\d*)"
        sale_price = response.css('h2[itemprop="price"]::text').get()
        reg_price = response.css('span[itemprop*="price"]::text').get()
        if reg_price is not None:
            price = "$"+reg_price
        elif sale_price is not None:
            sale_match = re.search(sale_re, sale_price)
            price = sale_match.group(1) if sale_match is not None else None
        else:
            price = None
        yield {
        'name' : response.css('h1::text').get(),
        'price' : price,
        'abv' : abv,
        'description' : " ".join(response.css('p span::text').getall()[:-3]),
        'rating' : None,
        'origin' : prod_data[0],
        'type' : type,
        'url' : response.request.url
        }

class WcomLiquorSpider(scrapy.Spider):
    name = 'wcom-liquor'
    start_urls = [
        'https://www.wine.com/list/spirits/7157/{}'.format(i) for i in range(1, 86)
    ]

    def parse(self, response):
        yield from response.follow_all(css='a.prodItemInfo_link', callback=self.parse_product)

    def parse_product(self, response):
        dollars = response.css('span.productPrice_price-regWhole::text').get().replace(',', '')
        cents = response.css('span.productPrice_price-regFractional::text').get()
        cents = cents if cents is not None else '00'
        price = float('{}.{}'.format(dollars, cents))
        abv = response.css('span.prodAlcoholPercent_percent::text').get()
        if abv == '0':
            return None
        desc_lst = response.css('div.pipWineNotes div.viewMoreModule_text').xpath('.//text()').getall()
        desc = ' '.join([s.strip() for s in desc_lst])
        reviews = ' '.join(response.css('div.pipProfessionalReviews_review').xpath('.//text()').getall())
        raw_ratings = response.css('ul.wineRatings_list span.wineRatings_rating::text').getall()
        ratings = [int(r) for r in raw_ratings]
        if len(ratings) == 0:
            return None
        rating = sum(ratings) / len(ratings)
        yield {
            'name': response.css('h1.pipName::text').get(),
            'origin': response.css('span.prodItemInfo_originText a::text').get(),
            'price': price,
            'abv': abv,
            'description': desc,
            'reviews': reviews,
            'rating': str(rating),
            'url': response.request.url
        }

# https://www.proof66.com/ good data but they have anti-crawling function
# class P66LiquorSpider(scrapy.Spider):
#     name = 'p66-liquor'
#     def start_requests(self):
#         yield scrapy.Request(url="https://www.proof66.com/", callback=self.parse_category)
#
#     def parse_category(self, response):
#         yield from response.follow_all(css='li[class*="panel dropdown mobilenav mb0"] a', callback=self.parse_collection)
#         # urls = response.css('li[class*="panel dropdown mobilenav mb0"] a').getall()[0:112]
#         # for url in urls:
#         #     yield scrapy.Request(url=response.urljoin(url), callback=self.parse_collection)
#
#     def parse_collection(self, response):
#         urls = response.css('section[id*="categorygrid"] a::attr(href)').getall()
#         for url in urls:
#             yield scrapy.Request(url=response.urljoin(url), meta = {'dont_redirect': True,'handle_httpstatus_list': [302]}, callback=self.parse_product)
#
#     def parse_product(self, response):
#         name = response.css('span[itemprop*="name"]::text').get()
#         if name is None:
#             return
#         yield {
#         'name' : name,
#         'price' : response.css('span[itemprop*="price"]::text').get(),
#         'abv' : response.css('span[class*="font16 fontRatingInfos320"]::text').getall()[2],
#         'description' : response.css('div[id*="notesDiv"] p::text').get(),
#         'rating' : response.css('span[itemprop="ratingValue"]::text').get() + " / " + response.css('span[itemprop="bestValue"]::text').get(),
#         'origin' : response.css('span[class*="font15 fontRatingInfos320"] a::text').getall()[1],
#         'type' : None,
#         'url' : response.request.url
#         }
