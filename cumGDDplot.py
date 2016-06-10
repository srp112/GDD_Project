#the cummulative GDD plot
import sys, argparse, csv, os

import matplotlib.pyplot as plt
import matplotlib.dates as dates
import datetime as dt

FolderName = 'plots'

def open_file(file_name, mode):
	"""Open a file."""
	try:
		with open(sys.argv[1], 'r') as the_file:
			filename=the_file.read()
          
	except IOError as err:
		print("Unable to open the file", file_name, "Ending program.\n", err)
		input("\n\nPress the enter key to exit.")
		sys.exit()
	else:
		return filename

"""Cities.txt file as an argument"""     
try:
	my_file = open_file(sys.argv[1], 'r')
except:
	print("GDD needs one argument", "\nEnding program...\n")
	input("Press the enter key to exit.")
	sys.exit()

try:
	original_umask = os.umask(0)
	if not os.path.exists(FolderName):
		os.makedirs(FolderName, 0o777)
except Exception as e:
	print("Failed to create 'data' directory, e = " + str(e))
	FolderName = ''
finally:
    os.umask(original_umask)

extension=".csv"
for index, line in enumerate(my_file.splitlines()):
	file_name=line+extension
	with open('data/'+ file_name, "rU") as files:
		val = list(csv.DictReader(files))  
		f = plt.figure(index + 1)
		xData = []
		yData = []
		for row in val:
			if row['Min Temp'] != '' and row['Max Temp'] != '':
				GDD = ((float(row['Min Temp']) + float(row['Max Temp'])) / 2) - 10
				if GDD < 0:
					GDD = 0
				xData.append(dt.date(int(row['Year']), int(row['Month']), int(row['Day'])))
				yData.append(GDD)
		ax = plt.gca()
		ax.plot(xData, yData, label = line)
		plt.title('GDD of ' + line)

		xax = ax.get_xaxis() # get the x-axis
		adf = xax.get_major_formatter() # the the auto-formatter

		adf.scaled[1.0] = '%Y/%m/%d' # set the > 1d < 1m scale to Y-m-d
		adf.scaled[30.] = '%Y/%m' # set the > 1m < 1Y scale to Y-m
		adf.scaled[365.] = '%Y' # set the > 1y scale to Y
		plt.draw()
		f.savefig(FolderName + '/' + line + '_GddPlot', format = 'png')
