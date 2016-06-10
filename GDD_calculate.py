import csv
import os
import copy
import argparse as arg

parser = arg.ArgumentParser(description='Accept input and calculate GDD.')
parser.add_argument('file', metavar='a txt file', type=str, help='Complete File Path of Cities File (Required!).')
parser.add_argument('tbase', metavar='Base Temperature', type=float, nargs='?', default=10, help='Base Temperature (default: 10).')
parser.add_argument('tupper', metavar='Upper Temperature', type=float, nargs='?', default=30, help='Upper Temperature (default: 30).')

FolderName = 'data'

args = parser.parse_args()
with open(args.file, 'r') as cf:
	for filename in cf.read().splitlines():
		newData = []
		with open(FolderName + '/' + filename + '.csv' , 'r') as f:
			reader = csv.reader(f)
			newData.append(next(reader) + ['GDD'])
			for row in reader:
				GDD = ''
				MinTemp = row[3]
				MaxTemp = row[4]
				if MinTemp != '' and MaxTemp != '':
					upper = min(float(MinTemp), args.tupper)
					lower = float(MaxTemp)
					GDD = round(((upper + lower) / 2) - args.tbase, 2)
					if GDD < 0:
						GDD = 0
				newData.append(row + [str(GDD)])
		with open(FolderName + '/' + filename + '.csv' , 'w') as f:
			writer = csv.writer(f, lineterminator = '\n')
			for row in newData:
				writer.writerow(row)
