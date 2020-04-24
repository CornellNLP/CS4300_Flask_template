cd scraper
scrapy crawl shack-beer -o ../data/shack-beer.json -t json
scrapy crawl conno-beer -o ../data/conno-beer.json -t json
scrapy crawl wcom-wine -o ../data/wcom-wine.json -t json