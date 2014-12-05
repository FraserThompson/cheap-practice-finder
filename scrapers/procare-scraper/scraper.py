import csv, json
import os, sys, codecs
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '\\..\\')
import scrapers

#stupid shit because the windows console can't print stuff properly
sys.stdout = codecs.getwriter('cp850')(sys.stdout.buffer, 'xmlcharrefreplace')
sys.stderr = codecs.getwriter('cp850')(sys.stderr.buffer, 'xmlcharrefreplace')

current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
practices_list = []
error_list = []
warning_list = []
details_dict = {}
count = 0
print("Started scraping.")
with open('practices 2013.csv', 'r') as prac_file:
	prac_reader = csv.reader(prac_file)
	for row in prac_reader:
		address = row[1] + ", " + row[2] if row[2] != '' and row[2] != 'CBD' and row[2] != 'Royal Oak' else row[1]
		details_dict[scrapers.normalize(row[0])] = [address, row[4], [0,0]]

with open('fees.csv', 'r') as fees_file:
	fees_reader = csv.reader(fees_file)
	for fees_row in fees_reader:
		name = fees_row[0]
		print(name)
		fees = fees_row[1:]
		details = scrapers.partial_match(scrapers.normalize(name), details_dict)
		url = scrapers.getHealthpointURL(name)

		if len(details) != 3:
			if url != '':
				details = scrapers.scrapeHealthpointDetails(url)
				if details == 0:
					error_list.append(name + ": No details.")
					continue
			else:
				error_list.append(name + ": No details.")
				continue

		if details[2][0] == 0 or details[2][0] == "":
			details[2] = scrapers.geolocate(details[0] + ", Auckland")
			if details[2][0] == 0:
				address_components = details[0].split(' ')
				coord = scrapers.geolocate(address_components[len(address_components) - 1] + ", Auckland")
				if details[2][0] == 0:
					error_list.append(name + ": Couldn't geocode: " + address)
					continue

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
			'name': name,
			'url': url,
			'address': details[0],
			'phone': details[1],
			'pho': 'Procare Networks',
			'coordinates': details[2],
			'prices': prices
		}
		count += 1
		practices_list.append(practice)


with open(current_dir + '\\data.json', 'w') as outFile:
	json.dump(practices_list, outFile, ensure_ascii=False, sort_keys=True, indent=4)

print("Dumped " + str(count) + " practices to file.")
scrapers.dealWithFailure(error_list, warning_list, current_dir)
