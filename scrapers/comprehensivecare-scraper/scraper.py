import sys, codecs, os
import json
import re
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '\\..\\')
import scrapers

practices_list = []
details_dict = {}
coords_list = []
error_list = []
warning_list = []
current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

# Access the URL
listUrlSouped = scrapers.openAndSoup('http://www.comprehensivecare.co.nz/category/region/auckland/')
rows = listUrlSouped.find_all('article', {'class': 'post type-post status-publish format-standard hentry category-post-formats has_thumbnail post-teaser'})

print("Done. Iterating rows...")
for row in rows:
	coord = [0,0]
	name = row.find('a').get_text(strip=True)
	website = row.find('header').find('a').get('href')
	address = row.find('div').find('span', {'class': 'address1'}).get_text()
	phone = row.find('div').find('span', {'class': 'address2'}).get_text()

	# Try find the coordinates of the address for Google Maps to display
	coord = scrapers.geolocate(address + ', Auckland')
	if coord[0] == 0:
		error_list.append(website + ": Couldn't geocode address: " + address)
		continue

	# Go deeper
	pracUrlSouped = scrapers.openAndSoup(website)
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
				'age': scrapers.getFirstNumber(fee[0]) if count != 2 else 0,
				'price': scrapers.getFirstNumber(fee[1].replace("Free", "0"))
			})
		except IndexError:
			print("================================WTF====================")
			warning_list.append(website + ": Couldn't get all the prices?")

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

scrapers.dealWithFailure(error_list, warning_list, current_dir)