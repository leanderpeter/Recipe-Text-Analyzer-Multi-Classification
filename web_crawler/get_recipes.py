import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

#links to cuisine category
cuisines = ["https://www.yummly.com/recipes?q=Best%20Chinese","https://www.yummly.com/recipes?q=Easy%20Chinese","https://www.yummly.com/recipes?q=Healthy%20Chinese",
"https://www.yummly.com/recipes?q=Best%20Mediterranean","https://www.yummly.com/recipes?q=Easy%20Mediterranean","https://www.yummly.com/recipes?q=Healthy%20Mediterranean"]

# numer of recipes wanted to search
# default = 50
numbers_of_recipes = 50

# desired dataset lenght
d_lenght = 110

# dataset
dataset = []

# Init headless chrome 
driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')

for element in cuisines:
	cuisine_tmp = element.split('%20')[1]
	# try to close ad
	try:
		driver.find_element_by_css_selector('.cancel').click()
	except:
		print('No Ad found ;)')

	# load website (element in cuisines)
	driver.get(element)
	wait = WebDriverWait(driver, 100)

	# sleep
	time.sleep(1)

	# find recipes by link-overlay
	recipes = driver.find_elements_by_class_name('link-overlay')

	rep_number_tmp = int(numbers_of_recipes/2.5)

	# split list for desired value
	recipes = recipes[:rep_number_tmp]

	for el in recipes:
		# try to get labels (eg names of recipe)
		try:
			name = el.get_attribute('aria-label')
			link = el.get_attribute('href')
			recipe = {'cuisine': cuisine_tmp, 'name':name , 'link': link}
			dataset.append(recipe)
		except:
			print('Element has no aria-label')

# close browser after use
driver.close()

# shorten dataset if necessary
if len(dataset) > d_lenght:
	dataset = dataset[:d_lenght]

print("Dataset length: ", len(dataset))

#write to csv
csv_columns = ["cuisine", "name", "link"]
csv_file = "dataset.csv"



try:
	with open(csv_file, 'w') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
		writer.writeheader()
		for data in dataset:
			writer.writerow(data)
	print('Dataset successfully saved as: ', csv_file)
except IOError:
	print("I/O error")
