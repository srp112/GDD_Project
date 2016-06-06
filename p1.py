import urllib.request as url
import requests
import csv
import sys
from datetime import date

RequestTimeOut = 30
ToYear = 2016
StationInventoryURL = 'ftp://client_climate@ftp.tor.ec.gc.ca/Pub/Get_More_Data_Plus_de_donnees/Station%20Inventory%20EN.csv'

StationInventoryReader = ''
Cities = []
StationIDs = []
f = ''

def exit():
	print('Program ended prematuraly')
	sys.exit(0)

characters = ['\'', '.', ',']
def matchCityName(a, b):
	for char in characters:
		a = a.replace(char, '')
		b = b.replace(char, '')

	for word in a.split(' '):
		if not word in b:
			return False
	return True

try:
	f = open(sys.argv[1], 'r')
except IndexError:
	print('City input filename not provided as the first argument')
	exit()

try:
	CurrentYear = date.today().year
	InputYear = int(sys.argv[2])
	if InputYear <= CurrentYear:
		ToYear = InputYear
	else:
		ToYear = CurrentYear
except IndexError:
	print('Year not provided as the second argument')
	exit()
except ValueError:
	print('Invalid input provided as the second argument, \'yyyy\' year expected')
	exit()

try:
	for line in f:
		line = line[0:len(line) - 1]
		Cities.append([line.split(',')[0].lower(), line.split(',')[1].lower(), list(range(ToYear, date.today().year + 1))])
	f.close()
except IndexError:
	print('Invalid input in City input file, expected \'CityName, ProvinceName\'')
	exit()
	
try:
	req = url.Request(StationInventoryURL)
	response = url.urlopen(req)
	data = response.read().decode('utf-8')
except Exception as e:
	print('Failed download Station Inventory data\n')
	exit()
else:
	LinesToRemove = 3
	BeginIndex = -1
	for i in range(0, LinesToRemove):
		BeginIndex = data.find('\n', BeginIndex + 1)
	StationInventoryReader = csv.DictReader(data[BeginIndex + 1:len(data) - 1].split('\n'))

for row in StationInventoryReader:
	for index, city in enumerate(Cities):
		if city[1] == row['Province'].lower():
			if matchCityName(city[0], row['Name'].lower()):
				if row['Last Year'] != '' and row['First Year'] != '':
					for year in Cities[index][2][:]:
						if year <= int(row['Last Year']) and year >= int(row['First Year']):
							StationIDs.append([city[0], city[1], row['Station ID'], str(year)])
							Cities[index][2].remove(year)

for station in StationIDs:
	print('City     : ', station[0])
	print('Province : ', station[1])
	print('StationID: ', station[2])
	print('Year     : ', station[3])
	print('\n')
						
#PayLoad = {'format' : 'xml', 'stationID' : '50089', 'Year' : '2012', 'Month' : '12', 'Day' : 1, 'timeframe' : '2', 'submit' : 'Download Data'}

#try:
#	r = requests.get('http://climate.weather.gc.ca/climate_data/bulk_data_e.html', params = PayLoad, timeout = RequestTimeOut)
#except Exception as e:
#	print(str(e))
#else:
#	with open('data.xml', 'wb') as f:
#		for chunk in r.iter_content(ChunkSize):
#			f.write(chunk)


