from urllib.request import urlopen
from bs4 import BeautifulSoup, Comment
from pygeocoder import Geocoder
import sys, codecs, os
import json
import re

def getFirstNumber(string):
	return float(re.findall('[-+]?\d*\.\d+|\d+', string)[0])

practices_list = []
details_dict = {}
coords_list = []
failed_list = []
current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

# Access the URL
print("Accessing URL...")
listUrl = urlopen('http://www.comprehensivecare.co.nz/category/region/auckland/').read()
print("Done. Souping it...")
listUrlSouped = BeautifulSoup(listUrl)
rows = listUrlSouped.find_all('article', {'class': 'post type-post status-publish format-standard hentry category-post-formats has_thumbnail post-teaser'})

print("Done. Iterating rows...")
for row in rows:
	coord = [0,0]
	name = row.find('a').get_text(strip=True)
	website = row.find('header').find('a').get('href')
	address = row.find('div').find('span', {'class': 'address1'}).get_text()
	phone = row.find('div').find('span', {'class': 'address2'}).get_text()

	# Try find the coordinates of the address for Google Maps to display
	try:
		result_array = Geocoder.geocode(address + ", Auckland, New Zealand")
		coord = result_array[0].coordinates
	except:
		failed_list.append("ERROR " + website + ": Couldn't geocode address: " + address)
		continue

	# Go deeper
	pracUrl = urlopen(website).read()
	pracUrlSouped = BeautifulSoup(pracUrl)
	fees_list = pracUrlSouped.find_all('div', {'class': 'wpb_wrapper'})[2].get_text().splitlines()
	prices = []
	count = 0
	for fee in fees_list:
		if fee.strip() == '':
			continue
		count += 1
		if (count <= 1):
			continue

		print(fee)
		fee = re.split('yrs|years', fee)
		try:
			prices.append({
				'age': getFirstNumber(fee[0]) if count != 2 else 0,
				'price': getFirstNumber(fee[1].replace("Free", "0"))
			})
		except IndexError:
			print("================================WTF====================")
			failed_list.append("WARNING " + website + ": Couldn't get all the prices?")

	practice = {
		'name': name,
		'url': website,
		'address': address,
		'phone': phone,
		'pho': 'Comprehensive Care',
		'coordinates': coord,
		'prices': prices
		}
	practices_list.append(practice)

with open(current_dir + '\\data.json', 'w') as outFile:
	json.dump(practices_list, outFile, ensure_ascii=False, sort_keys=True, indent=4)

if (len(failed_list) > 0):
	print(str(len(failed_list)) +  " practices had errors: ")
	failed_file = open(current_dir + '\\failed_list.txt', 'w')
	for f in failed_list:
		failed_file.write("%s\n" % f)
		print(f)
	failed_file.close()