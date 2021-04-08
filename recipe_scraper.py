from recipe_scrapers import scrape_me
import pandas as pd

# give the url as a string, it can be url from any site listed below
# scraper = scrape_me('https://www.allrecipes.com/recipe/158968/spinach-and-feta-turkey-burgers/')

# Q: What if the recipe site I want to extract information from is not listed below?
# A: You can give it a try with the wild_mode option! If there is Schema/Recipe available it will work just fine.
# scraper = scrape_me('https://www.feastingathome.com/tomato-risotto/', wild_mode=True)

# print("Title: \n", scraper.title())
# print("Total Time: \n", scraper.total_time())
# print("Yield: \n", scraper.yields())
# print("Ingredients: \n", scraper.ingredients())
# print("Instructions: \n", scraper.instructions())
# print("Image: \n", scraper.image())
# print("Host: \n", scraper.host())
# # print(scraper.links())
# print("Nutrients: \n", scraper.nutrients())  # if available

# initiate data storage
titles = []
total_times = []
yields = []
ingredients = []
images = []
host = []
links = []
nutrients = []

# scrape all
for i in range(1, 101):
    try:
        scraper = scrape_me("https://www.allrecipes.com/recipe/" + i + "/")
        titles.append(scraper.title())
        total_times.append(scraper.total_time())
        yields.append(scraper.yields())
        ingredients.append(scraper.ingredients())
        images.append(scraper.instructions())
        host.append(scraper.host())
        nutrients.append(scraper.nutrients())
    except:
        continue


# to_csv
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
