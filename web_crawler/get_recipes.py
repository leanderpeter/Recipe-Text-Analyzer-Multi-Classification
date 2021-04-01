import time
import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import csv
import random

#links to cuisine category
cuisines = ["https://www.yummly.com/recipes?q=Best%20Chinese","https://www.yummly.com/recipes?q=Easy%20Chinese","https://www.yummly.com/recipes?q=Healthy%20Chinese",
"https://www.yummly.com/recipes?q=Best%20Mediterranean","https://www.yummly.com/recipes?q=Easy%20Mediterranean","https://www.yummly.com/recipes?q=Healthy%20Mediterranean"]

# numer of recipes wanted to search
# default = 50
numbers_of_recipes = 50

# desired dataset lenght
d_lenght = 100

#desired test lenght
t_lenght = 10

# dataset
dataset = []

# test dataset
test_dataset = []

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

# create shuffled list of dataset with a lenght of k
# test dataset
d_shuffled = random.sample(dataset, k=t_lenght)

# shorten dataset if necessary
if len(dataset) > d_lenght:
	dataset = dataset[:d_lenght]

# print lenght of datasets
print("Training dataset length: ", len(dataset))
print("Test dataset length: ", len(d_shuffled))


#write to csv
csv_columns = ["cuisine", "name", "link"]
csv_file = "train_dataset.csv"
csv_test_file = "test_dataset.csv"



try:
	''' Write Training Dataset to csv
	'''
	with open(csv_file, 'w') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
		writer.writeheader()
		for data in dataset:
			writer.writerow(data)
	print('Train dataset successfully saved as: ', csv_file)

	''' Write Test Dataset to csv
	'''
	with open(csv_test_file, 'w') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
		writer.writeheader()
		for data in d_shuffled:
			writer.writerow(data)
	print('Test dataset successfully saved as: ', csv_test_file)
except IOError:
	print("I/O error")


