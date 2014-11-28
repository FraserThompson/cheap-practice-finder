import csv
import json
from pygeocoder import Geocoder

def partial_match(string, dictin):
	result = []
	for key in dictin:
		if key.startswith(string):
			print("This " + string + " matches " + key)
			result = dictin.get(key)
			break

	# Go for a less accurate search if nothing is found
	if len(result) == 0:
		for key in dictin:
			if key.startswith(' '.join(string.split()[:2])):
				print("This " + string + " matches " + key)
				result = dictin.get(key)
				break

	return result


rownum = 0
coord = [0, 0]
practices_list = []
failed_list = []
fees_list = {}

with open('fees.csv', 'r') as fees_file:
 	fees_reader = csv.reader(fees_file)
 	for row in fees_reader:
 		fees_list.update({row[0]: row[1:]})

with open('prac.csv', 'r') as prac_file:
	prac_reader = csv.reader(prac_file)
	for row in prac_reader:
		if rownum > 1:
			try:
				result_array = Geocoder.geocode(row[1])
				coord = result_array[0].coordinates
			except:
			 	failed_list.append("WARNING " + row[0] + ": Couldn't geocode: " + row[1])

			fees = partial_match(row[0].replace('-', '').replace('  ', ' '), fees_list)

			if (len(fees) == 0):
				failed_list.append("ERROR " + row[0] + ": Couldn't find fees.")

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

print(str(len(failed_list)) +  " practices had errors: ")
for f in failed_list:
	print(f)
