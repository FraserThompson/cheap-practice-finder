from bs4 import BeautifulSoup
from urllib.request import urlopen

def openAndSoup(url):
	return BeautifulSoup(urlopen(url).read())

def dealWithFailure(failed_list):
	if (len(failed_list) > 0):
	print(str(len(failed_list)) +  " practices had errors: ")
	failed_file = open('failed_list.txt', 'w')
	for f in failed_list:
		failed_file.write("%s\n" % f)
		print(f)
	failed_file.close()

def normalize(input):
	return re.sub('[^0-9a-zA-Z ]+', '', input.strip().lower().replace('mt', 'mount').replace('st', 'street'))

	
		# Try find the coordinates of the address for Google Maps to display
		# try:
		# 	result_array = Geocoder.geocode(address + "Wellington, New Zealand")
		# 	coord = result_array[0].coordinates
		# except:
		# 	print("Could not geocode address: " + address)