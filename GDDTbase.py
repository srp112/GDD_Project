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

Year = 0

"""Cities.txt file as an argument"""     
try:
	my_file = open_file(sys.argv[1], 'r')
	Year = sys.argv[2]
except:
	print("program needs two arguments", "\nEnding program...\n")
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
	xData = []
	yData = []
	TBaseLabels = []
	with open('data/'+ file_name, "rU") as files:
		val = list(csv.DictReader(files))  
		f = plt.figure(index + 1)
		tBaseIndex = -1
		for tbase in range(10, 16):
			xData.append([])
			yData.append([])
			TBaseLabels.append(tbase)
			tBaseIndex += 1
			CumSum = 0
			for row in val:
				if row['Year'] == Year:
					MinTemp = row['Min Temp']
					MaxTemp = row['Min Temp']
					if MinTemp != '' and MinTemp != '':
						upper = min(float(MinTemp), 30)
						lower = float(MaxTemp)
						GDD = round(((upper + lower) / 2) - tbase, 2)
						if GDD < 0:
							GDD = 0
						CumSum += GDD
						xData[tBaseIndex].append(dt.date(2016, int(row['Month']), int(row['Day'])))
						yData[tBaseIndex].append(CumSum)

		ax = plt.gca()
		for x, y, tbase in zip(xData, yData, TBaseLabels):
			ax.plot(x, y, label = tbase)
		plt.legend()
		plt.title('GDD of ' + line)

		xax = ax.get_xaxis() # get the x-axis
		adf = xax.get_major_formatter() # the the auto-formatter

		adf.scaled[1.0] = '%m/%d' # set the > 1d < 1m scale to Y-m-d
		adf.scaled[30.] = '%m' # set the > 1m < 1Y scale to Y-m
		adf.scaled[365.] = '%m' # set the > 1y scale to Y

		plt.draw()
		#plt.show()
		f.savefig(FolderName + '/' + line + '_GddPlot', format = 'png')
