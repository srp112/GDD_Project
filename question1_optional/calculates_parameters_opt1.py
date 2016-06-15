import csv
import os
import copy
import argparse as arg

def percentile_Calculation(MinTemp,MaxTemp,percent):
	MinTempPercentile = []
	MaxTempPercentile = []
	percent = percent/100
	for index in range(len(MinTemp)):
		MinTempPercentile.append(MinTemp[index]+(MinTemp[index]*percent))
		MaxTempPercentile.append(MaxTemp[index]-(MaxTemp[index]*percent))
	return MinTempPercentile,MaxTempPercentile

parser = arg.ArgumentParser(description='Accept input and calculate GDD.')
parser.add_argument('file', metavar='a txt file', type=str, help='Complete File Path of Cities File (Required!).')
#parser.add_argument('tbase', metavar='Base Temperature', type=float, nargs='?', default=10, help='Base Temperature (default: 10).')
#parser.add_argument('tupper', metavar='Upper Temperature', type=float, nargs='?', default=30, help='Upper Temperature (default: 30).')

FolderName = 'data'

args = parser.parse_args()
with open(args.file, 'r') as cf:
	for filename in cf.read().splitlines():
		newData = []
		with open(FolderName + '/' + filename + '.csv' , 'r') as f:
			reader = csv.reader(f)	
			newData.append(next(reader) + ['Average'])
			newData.append(next(reader) + ['Min_5_95'])
			newData.append(next(reader) + ['Max_5_95'])	
			newData.append(next(reader) + ['Min_25_75'])
			newData.append(next(reader) + ['Max_25_75'])
			for row in reader:
				Average = ''

				MinTemp = row[3]
				MaxTemp = row[4]
				if MinTemp != '' and MaxTemp != '':
					#upper = min(float(MinTemp), args.tupper)
					upper = float(MinTemp)
					lower = float(MaxTemp)
					for index in range(len(MinTemp)):
						Average = round((upper + lower) / 2) 
						newData.append(row + [str(Average)])

        

						percent = 5
						Min_5_95,Max_5_95 = percentile_Calculation(MinTemp,MaxTemp,percent)
						percent = 25
						Min_25_75,Max_25_75 =percentile_Calculation(MinTemp,MaxTemp,percent)
						
						newData.append(row + [str(Min_5_95)])
						newData.append(row + [str(Max_5_95)])
						newData.append(row + [str(Min_25_75)])
			newData.append(row + [str(Max_25_75)])
		with open(FolderName + '/' + filename + '.csv' , 'w') as f:
			writer = csv.writer(f, lineterminator = '\n')
			for row in newData:
				writer.writerow(row)
