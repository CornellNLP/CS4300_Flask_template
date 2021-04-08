from recipe_scrapers import scrape_me
import pandas as pd


titles = []
total_times = []
yields = []
ingredients = []
images = []
host = []
links = []
nutrients = []

# scraper = scrape_me(
#     "https://www.allrecipes.com/recipe/" + str() + "/")
# print(scraper)
# random sample
# do we include things with empty fields?
count = 0
i = 15868
while count < 100:
    print(i)
    # try:
    scraper = scrape_me(
        "https://www.allrecipes.com/recipe/" + str(i) + "/")
    title = scraper.title()
    if title == "":
        i += 1
        continue
    titles.append(title)
    total_times.append(scraper.total_time())
    yields.append(scraper.yields())
    ingredients.append(scraper.ingredients())
    images.append(scraper.instructions())
    host.append(scraper.host())
    nutrients.append(scraper.nutrients())
    i += 1
    count += 1
    # except:
    # i += 1
    # continue
    # print(titles)

print(titles)

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
