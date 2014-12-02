import csv, json
import os, sys
import re
from pygeocoder import Geocoder

current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

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

def normalize(input):
	return re.sub('[^0-9a-zA-Z ]+', '', input.strip().lower().replace('mt', 'mount').strip())

coord = [0, 0]
practices_list = []
failed_list = []
fees_list = {}
count = 0

with open('fees.csv', 'r') as fees_file:
 	fees_reader = csv.reader(fees_file)
 	for fees_row in fees_reader:
 		fees_list.update({normalize(fees_row[0]): fees_row[1:]})

with open('practices 2013.csv', 'r') as prac_file:
	prac_reader = csv.reader(prac_file)
	for row in prac_reader:
		address = row[1] + ", " + row[2]
		try:
			result_array = Geocoder.geocode(address + ", New Zealand")
			coord = result_array[0].coordinates
		except:
		 	failed_list.append("ERROR " + row[0] + ": Couldn't geocode: " + row[1])
		 	continue

		fees = partial_match(normalize(row[0]), fees_list)

		if (len(fees) == 0):
			failed_list.append("WARNING " + row[0] + ": Couldn't find fees.")
			prices = []
		else:
			prices =  [
				{
				'age': 0,
				'price': float(fees[0]),
				},
				{
				'age': 6,
				'price': float(fees[1]),
				},
				{
				'age': 18,
				'price': float(fees[2]),
				},
				{
				'age': 25,
				'price': float(fees[3]),
				},
				{
				'age': 45,
				'price': float(fees[4]),
				},
				{
				'age': 65,
				'price': float(fees[5]),
				},
			] 

		practice = {
			'name': row[0],
			'url': 'None supplied',
			'address': address,
			'phone': row[4],
			'pho': 'Procare Networks',
			'coordinates': coord,
			'prices': prices
		}
		count += 1
		practices_list.append(practice)

with open(current_dir + '\\data.json', 'w') as outFile:
	json.dump(practices_list, outFile, ensure_ascii=False, sort_keys=True, indent=4)

print("Dumped " + str(count) + " practices to file.")

if (len(failed_list) > 0):
	print(str(len(failed_list)) +  " practices had errors: ")
	failed_file = open(current_dir + '\\failed_list.txt', 'w')
	for f in failed_list:
		failed_file.write("%s\n" % f)
		print(f)
	failed_file.close()
