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
links = []
nutrients = []
ratings = []

# scraper = scrape_me(
#     "https://www.allrecipes.com/recipe/" + str() + "/")
# print(scraper)
# random sample
# do we include things with empty fields?
count = 0
while count < 100:
    i = random.randint(0, 300000)

    print(i)
    # try:
    scraper = scrape_me(
        "https://www.allrecipes.com/recipe/" + str(i) + "/")
    title = scraper.title()
    if title == "":
        # i += 1
        continue
    print("found")
    titles.append(title)
    authors.append(scraper.author())
    total_times.append(scraper.total_time())
    yields.append(scraper.yields())
    ingredients.append(scraper.ingredients())
    instructions.append(scraper.instructions())
    images.append(scraper.instructions())
    host.append(scraper.host())
    nutrients.append(scraper.nutrients())
    ratings.append(scraper.ratings())
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
    'total time': total_times,
    'yields': yields,
    'ingredients': ingredients,
    'images': images,
    'host': host,
    'links': links,
    'nutrients': nutrients
})

recipes.to_csv('p02_recipes.csv')
