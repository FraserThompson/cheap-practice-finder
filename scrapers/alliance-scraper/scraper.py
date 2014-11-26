import csv
import json
from pygeocoder import Geocoder

rownum = 0
coord = [0, 0]
practices_list = []

with open('ahprac.csv', 'r') as f:
	reader = csv.reader(f)
	for row in reader:
		if rownum > 1:
			try:
				result_array = Geocoder.geocode(row[1])
				coord = result_array[0].coordinates
			except:
			 	print("Could not geocode address: " + row[1])

			practice = {
				'name': row[0],
				'url': "None supplied",
				'address': row[1],
				'phone': row[2],
				'pho': 'Alliance Health Plus',
				'coordinates': coord,
				'prices': [
					{
					'age': 0,
					'price': 0,
					},
					{
					'age': 6,
					'price': 0,
					},
					{
					'age': 18,
					'price': 0,
					},
					{
					'age': 25,
					'price': 0,
					},
					{
					'age': 45,
					'price': 0,
					},
					{
					'age': 65,
					'price': 0,
					},
				] 
			}

			practices_list.append(practice)
		rownum += 1

with open('data.json', 'w') as outFile:
	json.dump(practices_list, outFile, ensure_ascii=False, sort_keys=True, indent=4)