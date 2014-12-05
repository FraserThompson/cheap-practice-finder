from bs4 import BeautifulSoup, Comment
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

def normalize(input):
	return scrapers.normalize(input).replace(' st', 'street')

# Access the URL
rootURL = 'http://www.aucklandpho.co.nz'
listUrlSouped = scrapers.openAndSoup(rootURL + '/fees/')
rows = listUrlSouped.find('table', {'id': 'feestable'}).find_all('tr')[1:]

pracURLSouped = scrapers.openAndSoup(rootURL + '/practices/practice-locations/')
coord_list = pracURLSouped.find_all('div', {'class': 'cggm_marker'})
for item in coord_list:
	comments = item.find_all(text=lambda text:isinstance(text, Comment))
	comments2 = [comment.extract() for comment in comments]
	item_phone = comments2[0].split('</b>')[1].split('<br />')[0]
	item_coord = [float(item.find('input', {'name': 'latitude'}).get('value')), float(item.find('input', {'name': 'longitude'}).get('value'))]
	item_name = item.find('input', {'name': 'title'}).get('value')
	item_info = item.find('div', {'class': 'cggm_infowindow_item'})
	item_address = item_info.get_text().splitlines()[1].split(':')[1].strip()
	item_url = rootURL + "/" + item_info.find('a').get('href')
	details_dict.update({normalize(item_name): [item_address, item_url, item_phone, item_coord]})

print("Done. Iterating rows...")
for row in rows:
	coord = [0,0]
	cells = row.find_all('td')
	name = cells[0].get_text(strip=True)
	normal_name = normalize(name).split()
	website = "None"
	address = "None"
	phone = "None"

	prac_details = [v for k,v in details_dict.items() if k.startswith(' '.join(normal_name[:2]))]
	if len(prac_details) == 0 or len(prac_details[0]) < 4:
		error_list.append(name + ": Could not find details.")
		continue
	else:
		address = prac_details[0][0]
		website = prac_details[0][1]
		phone = prac_details[0][2]
		coord = prac_details[0][3]

	practice = {
		'name': name,
		'url': website,
		'address': address,
		'phone': phone,
		'pho': 'Auckland PHO',
		'coordinates': coord,
		'prices': [
				{
				'age': 0,
				'price': float(cells[1].get_text(strip=True).replace(" ", "").replace("$", "")),
				},
				{
				'age': 6,
				'price': float(cells[2].get_text(strip=True).replace(" ", "").replace("$", "")),
				},
				{
				'age': 18,
				'price': float(cells[3].get_text(strip=True).replace(" ", "").replace("$", "")),
				},
				{
				'age': 24,
				'price': float(cells[4].get_text(strip=True).replace(" ", "").replace("$", "")),
				},
				{
				'age': 45,
				'price': float(cells[5].get_text(strip=True).replace(" ", "").replace("$", "")),
				},
				{
				'age': 65,
				'price': float(cells[6].get_text(strip=True).replace(" ", "").replace("$", "")),
				}
			]
		}
	practices_list.append(practice)

with open(current_dir + '\\data.json', 'w') as outFile:
	json.dump(practices_list, outFile, ensure_ascii=False, sort_keys=True, indent=4)

scrapers.dealWithFailure(error_list, warning_list, current_dir)