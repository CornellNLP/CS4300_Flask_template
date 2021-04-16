from recipe_scrapers import scrape_me
import pandas as pd
import random

authors = []
titles = []
total_times = []
yields = []
ingredients = []
instructions = []
images = []
host = []
nutrients = []
ratings = []

# scraper = scrape_me(
#     "https://www.allrecipes.com/recipe/" + str() + "/")
# print(scraper)
# random sample
# do we include things with empty fields?
count = 0
while count < 100:
    i = random.randint(0, 500000)
    print(i)
    # try:
    scraper = scrape_me(
        "https://www.allrecipes.com/recipe/" + str(i) + "/")
    title = scraper.title()
    if title == "" or title in titles:
        # i += 1
        continue
    titles.append(title)
    authors.append(scraper.author() if scraper.author() else "")
    total_times.append(scraper.total_time() if scraper.total_time() else "")
    yields.append(scraper.yields() if scraper.yields() else "")
    ingredients.append(scraper.ingredients() if scraper.ingredients() else "")
    instructions.append(scraper.instructions() if scraper.instructions() else "")
    images.append(scraper.image() if scraper.image() else "")
    host.append(scraper.host() if scraper.host() else "")
    nutrients.append(scraper.nutrients() if scraper.nutrients() else "")
    ratings.append(scraper.ratings() if scraper.ratings() else "")
    # i += 1
    count += 1
    # except:
    # i += 1
    # continue
    # print(titles)

print(titles)
#remove duplicates?

recipes = pd.DataFrame({
    'title': titles,
    'authors': authors,
    'total time': total_times,
    'yields': yields,
    'ingredients': ingredients,
    'instructions': instructions,
    'images': images,
    'host': host,
    'nutrients': nutrients,
    'ratings': ratings
})

recipes.to_csv('p02_recipes.csv')

