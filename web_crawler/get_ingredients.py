from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import pandas as pd
import csv
from tqdm import tqdm
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--recipes', help='Path to Trainings Daten in CSV format',
                    default='TrainingsDaten.csv', type=str)
args = parser.parse_args()

recipe_raw = []

with open(args.recipes, newline='') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
	for row in spamreader:
		# print(', '.join(row))
		recipe_raw.append(row)

# recipes = ['https://www.yummly.com/recipe/Korean-Street-Cheese-Corn-Dogs-2309605']

# Init headless chrome 
driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')

# init empty dataframe
df = pd.DataFrame(columns=['index', 'name', 'ingredients','cuisine'])

# list of dead recipes
dead_recipes = []

for recipe in tqdm(range(1, len(recipe_raw))):

	driver.get(recipe_raw[recipe][2])

	if recipe < 2:
		# sleep
		time.sleep(1)
		# try to close ad
		try:
			driver.find_element_by_css_selector('.cancel').click()
		except:
			print('No Ad found ;)')

	time.sleep(1)

	# get all ingredient 'tabs'
	row = driver.find_elements_by_class_name("IngredientLine")
	if row == None:
		dead_recipes.append(recipe_raw[recipe][2])

	# init empty list for all ingredients in recipe
	ingredients = []
	
	for ing in row:
		tmp_entry = ''

		try:
			amount = ing.find_element_by_class_name('amount')
			if amount:
				tmp_entry += amount.text
		except:
			pass
		try:
			unit = ing.find_element_by_class_name('unit')
			if unit:
				tmp_entry += unit.text + ' '
		except:
			pass
		try:
			ingredient = ing.find_element_by_class_name('ingredient')
			if ingredient:
				tmp_entry += ingredient.text
		except:
			pass
		try:
			remainder = ing.find_element_by_class_name('remainder')
			if remainder:
				tmp_entry += ' ' + remainder.text
		except:
			pass

		ingredients.append(tmp_entry)

	# set index 
	df.at[recipe, 'index'] = recipe
	# set ingredients
	df.at[recipe, 'ingredients'] = ingredients
	# set name
	df.at[recipe, 'name'] = recipe_raw[recipe][1]
	# set cusines
	df.at[recipe, 'cuisine'] = recipe_raw[recipe][0]





print(dead_recipes)

df.to_csv('test_data_w_ingredients.csv', sep=';', encoding='utf-8')

# close browser after use
driver.close()

try:
	with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
		writer = csv.DictWriter('dead_links.csv', fieldnames=['dead_links'])
		writer.writeheader()
		for data in dead_recipes:
			writer.writerow(data)

except:
	print("No dead links found!")