from urllib.request import urlopen
from bs4 import BeautifulSoup
from pygeocoder import Geocoder
import sys, codecs, os
import json
import re

def getFirstNumber(string):
	return float(re.findall('[-+]?\d*\.\d+|\d+', string)[0])

#stupid shit because the windows console can't print stuff properly
sys.stdout = codecs.getwriter('cp850')(sys.stdout.buffer, 'xmlcharrefreplace')
sys.stderr = codecs.getwriter('cp850')(sys.stderr.buffer, 'xmlcharrefreplace')
current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

url = 'http://www.southernpho.health.nz/'
practices_list = []
failed_list = []
coord = [0.00, 0.00]

for i in range (1, 7):
	listUrl = urlopen(url + 'info.php?rid=' + str(i)).read()
	listUrlSouped = BeautifulSoup(listUrl)
	rows = listUrlSouped.find('div', {'class': 'content'}).find_all('table')[1].find_all('tr')
	for row in rows:
		url_suffix = row.find("a").get("href")
		name = row.find("a").text

		#### GO DEEPER #####
		practiceUrlOpened = urlopen(url + url_suffix).read()
		practiceUrlSouped = BeautifulSoup(practiceUrlOpened)
		practice_rows = practiceUrlSouped.find('div', {'class': 'contentws'}).find('table').find_all('tr')
		practice_info_cells = practice_rows[0].find_all('td')

		#### GOING IN REALLY DEEP ####
		try:
			scriptElement = practiceUrlSouped.findAll('script', {"type":"text/javascript"})
			first = scriptElement[3].text.split("LatLng(", 1)
			if (len(first) > 1):
				coord = first[1].split("),", 1)[0].split(", ");
				coord[0] = float(coord[0])
				coord[1] = float(coord[1])
		except IndexError:
			failed_list.append("ERROR " + url + url_suffix + ": No coordinates.")
			coord = coord

		try:
			address = practice_info_cells[1].find_all('p')[0].text.split("Location")[1].replace("\n", "").strip()
		except IndexError:
			failed_list.append("WARNING " + url + url_suffix + ": No address.")
			address = "None supplied"
		try:
			phone = practice_info_cells[1].find_all('p')[1].text.split("Phone: ")[1].strip()
		except IndexError:
			failed_list.append("WARNING " + url + url_suffix + ": No phone number.")
			phone = "None supplied"

		price_rows = practice_info_cells[2].find('table').find_all('tr')
		first_price = price_rows[0].find_all('td')[1].get_text(strip=True).replace(" ", "")

		# Try get all the prices regardless of formatting lol
		prices = []
		if (first_price == ""):
			failed_list.append("WARNING " + url + url_suffix + ": No price list.")
		else:
			prices.append({
				'age': 0,
				'price': 0
			})
			for i in range(1, 6):
				cells = price_rows[i].find_all('td')
				print("working on : " + str(cells))
				if 'and' not in cells[1].get_text(strip=True) and ',' not in cells[1].get_text(strip=True):
					prices.append({
						'age': getFirstNumber(cells[0].get_text(strip=True)),
						'price': getFirstNumber(cells[1].get_text(strip=True))
					})
				else:
					price_search = re.split('and|,', cells[1].get_text(strip=True))
					for price_bracket in price_search:
						price_bracket = price_bracket.split()
						print("Brackets: " + str(price_bracket))
						try:
							prices.append({
								'age': getFirstNumber(price_bracket[0]),
								'price': getFirstNumber(price_bracket[len(price_bracket)-1])
							})
						except IndexError: 
							failed_list.append("WARNING " + url + url_suffix + ": Weird price list.")
		practice = {
			'name': name,
			'url': url + url_suffix,
			'address': address,
			'phone': phone,
			'pho': "Southern PHO",
			'coordinates': coord,
			'prices': prices
		}
		
		#print("Appending Practice: rid= " + str(i) + " Address: " + address + " Phone: " + phone)
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