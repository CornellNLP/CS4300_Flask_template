import scrapy

class WcomWineSpider(scrapy.Spider):
    name = 'wcom-wine'
    start_urls = [
        'https://wine.com/list/wine/7155/{}'.format(i) for i in range(1, 204)
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