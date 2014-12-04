from urllib.request import urlopen, HTTPError, URLError
from bs4 import BeautifulSoup, Comment
from pygeocoder import Geocoder
import sys, codecs, os
import json
import re

def toURL(input):
	normal = re.sub('[^0-9a-zA-Z ]+', '', input.strip())
	return normal.lower().replace(' ', '-') + "/"

def getFirstNumber(string):
	return float(re.findall('[-+]?\d*\.\d+|\d+', string)[0])

practices_list = []
failed_list = []
current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
regions = ['Auckland-Central', 'Auckland-South', 'auckland-east', 'Auckland-West', 'Tairawhiti', 'midlands-region']
#regions = ['Auckland-Central']

# Access the URLs
for region in regions:
	print("Accessing URL...")
	listUrl = urlopen('http://www.nhc.maori.nz/index.php?page=' + region).read()
	print("Done. Souping it...")
	listUrlSouped = BeautifulSoup(listUrl)
	rows = listUrlSouped.find_all('div', {'class': 'news_post'})
	print("Done. Iterating rows...")

	for row in rows:
		coord = [0,0]
		name = row.find('h4').get_text(strip=True)
		left_panel = row.find('div', {'class': 'c_left'})
		right_panel = row.find('div', {'class': 'c_right'})
		pho_name = left_panel.find('p').get_text(strip=True).split(':')[1]

		if 'is taking new patients' not in right_panel.find_all('p')[2].get_text():
			failed_list.append('WARNING ' + name + ': Is not taking patients')
			continue

		if right_panel.find('a'):
			website = right_panel.find('a').get('href')
		else:
			#Try find URL
			try:
				website = 'http://www.healthpoint.co.nz/doctors/gp/' + toURL(name)
				urlopen(website)
			except HTTPError as e:
				failed_list.append("WARNING " + name + ": Couldn't find URL: " + str(e.code))
				website = ""
			except URLError as e:
				failed_list.append("WARNING " + name + ": Couldn't find URL: " + str(e.code))
				website = ""
			else:
				print("ok")

		address = right_panel.find_all('p')[1].get_text(strip=True)
		phone = right_panel.find_all('p')[0].get_text().splitlines()[1].split(':')[1].strip()

		# Try find the coordinates of the address for Google Maps to display
		try:
			result_array = Geocoder.geocode(address + ", New Zealand")
			coord = result_array[0].coordinates
		except:
			failed_list.append("ERROR " + website + ": Couldn't geocode address: " + address)
			continue



		fees_table = left_panel.find('table', {'class': 'tbl fees'}).find_all('tr')
		prices = []
		count = 0
		for tr in fees_table:
			cells = tr.find_all('td')
			count += 1
			try:
				prices.append({
					'age': getFirstNumber(cells[0].get_text()) if count != 1 else 0,
					'price': getFirstNumber(cells[1].get_text())
				})
			except IndexError:
				print("================================WTF====================")
				failed_list.append("WARNING " + website + ": Couldn't get all the prices?")

		practice = {
			'name': name,
			'url': website,
			'address': address,
			'phone': phone,
			'pho': pho_name,
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