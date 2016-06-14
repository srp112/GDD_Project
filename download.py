import urllib.request as url
import requests
import csv
import sys
import os
import operator
from datetime import date

StationInventoryURL = 'ftp://client_climate@ftp.tor.ec.gc.ca/Pub/Get_More_Data_Plus_de_donnees/Station%20Inventory%20EN.csv'
MissingDataThreshold = 0.20
RequestTimeOut = 30
FolderName = 'data'
LogFileName = 'log_download.txt'

def exit():
	print('Program ended prematuraly')
	logfile.close()
	sys.exit(0)

def log(text):
	print(text)
	logfile.write(text + '\n')
	
characters = ['\'', '.', ',']
def matchCityName(a, b):
	for char in characters:
		a = a.replace(char, '')
		b = b.replace(char, '')

	for word in a.split(' '):
		if not word in b:
			return False
	return True

def removeInitialLines(f, LinesToRemove):
	BeginIndex = -1
	for i in range(0, LinesToRemove):
		BeginIndex = f.find('\n', BeginIndex + 1)
	return f[BeginIndex + 1:len(f) - 1]

logfile = 0
try:
	logfile = open(LogFileName, 'w')
except IOError:
	print('Error creating log file')

try:
	CityFile = open(sys.argv[1], 'r')
except IndexError:
	log('City input filename not provided as the first argument')
	exit()

try:
	CurrentYear = date.today().year
	InputYear = int(sys.argv[2])
	if InputYear <= CurrentYear:
		ToYear = InputYear
	else:
		ToYear = CurrentYear
except IndexError:
	log('Year not provided as the second argument')
	exit()
except ValueError:
	log('Invalid input provided as the second argument, \'yyyy\' year expected')
	exit()

Cities = []

try:
	for line in CityFile:
		line = line[0:len(line) - 1]
		Cities.append([line.split(',')[0].lower(), line.split(',')[1].lower(), list(range(ToYear, date.today().year + 1)), []])
	CityFile.close()
except IndexError:
	log('Invalid input in City input file, expected \'CityName, ProvinceName\'')
	exit()

StationInventoryReader = ''
	
try:
	req = url.Request(StationInventoryURL)
	response = url.urlopen(req)
	data = response.read().decode('utf-8')
except Exception as e:
	log('Failed to download Station Inventory data ... ' + str(e))
	exit()
else:
	StationInventoryReader = csv.DictReader(removeInitialLines(data, 3).split('\n'))
	log('Successfully downloaded Station Inventory EN.csv\n')

Data = []
for i in range(0, len(Cities)):
	Data.append([])

PayLoad = {'format' : 'csv', 'stationID' : '50089', 'Year' : '2012', 'Month' : '12', 'Day' : '1', 'timeframe' : '2', 'submit' : 'Download+Data'}

for row in StationInventoryReader:
	for index, city in enumerate(Cities):
		if city[1] == row['Province'].lower():
			if matchCityName(city[0], row['Name'].lower()):
				#if row['WMO ID'] != '':
					if row['Last Year'] != '' and row['First Year'] != '':	
						for year in Cities[index][2][:]:
							if year <= int(row['Last Year']) and year >= int(row['First Year']):
								PayLoad['stationID'] = row['Station ID']
								PayLoad['Year'] = str(year)
								try:
									r = requests.get('http://climate.weather.gc.ca/climate_data/bulk_data_e.html', params = PayLoad, 														timeout = RequestTimeOut)
								except Exception as e:
									log('Failed to download data for station ' + row['Name'] + ' ID ' + row['Station ID'] + ' year ' + 											str(year))
								else:
									DataReader = list(csv.DictReader(removeInitialLines(r.text, 25).split('\n')))
									
									NumOfDays = 365
									if year % 4 == 0:
										NumOfDays = 366
									if year == date.today().year:
										NumOfDays = (date.today() - date(year, 1, 1)).days
										
									MissingData = 0
									for i in range(0, min(len(DataReader), NumOfDays)):
										if (DataReader[i]['Max Temp (°C)'] == '' or DataReader[i]['Min Temp (°C)'] == ''):
											MissingData += 1
										
									if MissingData / NumOfDays <= MissingDataThreshold:
										log('Downloading data for ' + city[0] + ', year ' + str(year))							
										Cities[index][2].remove(year)
										StationIndex = [i for i, x in enumerate(Cities[index][3]) if x[0] == row['Station ID']]
										if StationIndex == []:
											Cities[index][3].append([row['Station ID'], row['Latitude (Decimal Degrees)'], row['Longitude (Decimal Degrees)'], 1])
										else:
											StationIndex = StationIndex[0]
											#print(Cities[index][3][StationIndex][3])
											Cities[index][3][StationIndex][3] += 1
										for i in range(0, min(len(DataReader), NumOfDays)):
											Data[index].append([DataReader[i]['Year'], DataReader[i]['Month'], DataReader[i]['Day'], 																	DataReader[i]['Max Temp (°C)'], DataReader[i]['Min Temp (°C)']])
									else:
										log('Rejected file for ' + city[0] + ', year ' + str(year) + ', ' + 											str(round(MissingData / NumOfDays * 100, 2)) + '% data missing')

log('\n...Writing the downloaded data to storage...')

try:
	original_umask = os.umask(0)
	if not os.path.exists(FolderName):
		os.makedirs(FolderName, 0o777)
except Exception as e:
	log("Failed to create 'data' directory, e = " + str(e))
	FolderName = ''
finally:
    os.umask(original_umask)

try:
	# Location file name
	with open(sys.argv[1].split('.')[0] + 'Map' + '.txt' ,'w') as f:
		for city in Cities:
			index = 0
			for i in range(1, len(city[3])):
				if city[3][i][3] > city[3][index][3]:
					index = i
			f.write(city[0] + ',' + city[1] + ',' + city[3][index][1] + ',' + city[3][index][2] + '\n')
except:
	log('Failed to create Map file for cities')
    
for index, city in enumerate(Cities):
	filename = city[0] + ',' + city[1]
	with open(FolderName + '/' + filename + '.csv', 'w') as CityFile:
		CityFile.write('"Year","Month","Day","Max Temp","Min Temp"\n')
		Data[index].sort(key = operator.itemgetter(0, 1, 2))
		for row in Data[index]:
			for i in range(0, len(row) - 1):
				CityFile.write(row[i] + ',')
			CityFile.write(row[i+1] + '\n')
