from urllib.request import urlopen
from bs4 import BeautifulSoup
from pygeocoder import Geocoder
import sys, codecs
import json

#stupid shit because the windows console can't print stuff properly
sys.stdout = codecs.getwriter('cp850')(sys.stdout.buffer, 'xmlcharrefreplace')
sys.stderr = codecs.getwriter('cp850')(sys.stderr.buffer, 'xmlcharrefreplace')

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
			coord = coord

		try:
			address = practice_info_cells[1].find_all('p')[0].text.split("Location")[1].replace("\n", "").strip()
		except IndexError:
			address = "None supplied"

		try:
			phone = practice_info_cells[1].find_all('p')[1].text.split("Phone: ")[1].strip()
		except IndexError:
			phone = "None supplied"

		price_rows = practice_info_cells[2].find('table').find_all('tr')
		first_price = price_rows[0].find_all('td')[1].get_text(strip=True).replace(" ", "")
		if (first_price == ""):
			continue

		try:
			first_float = float(price_rows[0].find_all('td')[1].get_text(strip=True).replace(" ", "").replace("$", ""))
		except ValueError:
			continue
		try:
			second_float = float(price_rows[1].find_all('td')[1].get_text(strip=True).replace(" ", "").replace("$", ""))
		except ValueError:
			continue

		practice = {
			'name': name,
			'url': url + url_suffix,
			'address': address,
			'phone': phone,
			'pho': "Southern PHO",
			'coordinates': coord,
			'prices': [
				{
				'age': 0,
				'price': first_float,
				},
				{
				'age': 6,
				'price': second_float,
				},
				{
				'age': 18,
				'price': float(price_rows[2].find_all('td')[1].get_text(strip=True).replace(" ", "").replace("$", "")),
				},
				{
				'age': 24,
				'price': float(price_rows[3].find_all('td')[1].get_text(strip=True).replace(" ", "").replace("$", "")),
				},
				{
				'age': 45,
				'price': float(price_rows[4].find_all('td')[1].get_text(strip=True).replace(" ", "").replace("$", "")),
				},
				{
				'age': 65,
				'price': float(price_rows[5].find_all('td')[1].get_text(strip=True).replace(" ", "").replace("$", "")),
				},
			] 
		}
		
		print("Appending Practice: rid= " + str(i) + " Address: " + address + " Phone: " + phone)
		practices_list.append(practice)

with open('data.json', 'w') as outFile:
	json.dump(practices_list, outFile, ensure_ascii=False, sort_keys=True, indent=4)

print("The following practices were not added: ")
for f in failed_list:
	print(f)