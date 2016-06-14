from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import sys
import csv
FolderName = 'data'

Data = []

Year = sys.argv[2]

fig = plt.figure()

#Read GDD data
with open(sys.argv[1].split('.')[0] + 'Map.txt', 'r') as cf:
	for line in cf.read().splitlines():
		CityData = line.split(',')
		filename = CityData[0] + ',' + CityData[1]
		with open(FolderName + '/' + filename + '.csv', 'r') as f:
			reader = csv.DictReader(f)
			GDDSum = 0
			for row in reader:
				if row['Year'] == Year:
					if row['GDD'] != '':
						GDDSum += float(row['GDD'])
			#City Name, latitude, longitude, GDD sum
			Data.append((CityData[0], float(CityData[2]), float(CityData[3]), GDDSum))

def get_marker_color(GDD):
    # Returns red for small GDD, yellow for moderate
    #  GDD, and green for significant GDD.
    if GDD < 510.0:
        return ('ro')
    elif GDD < 900.0:
        return ('yo')
    else:
        return ('go')

#Plotting map of Canada
MyMap = Basemap(llcrnrlon=-145.9927, llcrnrlat=44.49, urcrnrlon=-35.4459, urcrnrlat=71.8125,
              projection='lcc', resolution = 'h', area_thresh = 15000.0,
 lat_1=-4., lat_0=30.83158, lon_0=-50.)

MyMap.drawmapboundary(fill_color='aqua')
MyMap.fillcontinents(color='white', lake_color='aqua', zorder = 0)
MyMap.drawcoastlines(color = '0.15')
MyMap.drawcountries()

lats = [city[1] for city in Data]
lons = [city[2] for city in Data]
magnitudes = [city[3] for city in Data]
labels = [city[0] for city in Data]



min_marker_size = 2.5
for lon, lat, mag, name in zip(lons, lats, magnitudes, labels):
	x,y = MyMap(lon, lat)
	msize = mag * min_marker_size
	marker_string = get_marker_color(mag)
	MyMap.plot(x, y, marker_string, markersize=10)
	plt.text(x+100000,y+150000, name) #distance of labels: 10 Km East and 10 Km North
plt.text(5, 1000000, r'GDD > 900', color='g')
plt.text(5, 500000, r'GDD > 510', color='y')
plt.text(5, 100000, r'GDD < 510', color='r')
plt.text(5, 1500000, r'no data', color='w')
plt.title(r'Acumulated GDD for ' + Year, fontsize=20, color='b')
plt.draw()
save_plot = 'plots/GDDMap_' + Year + '.png'
fig.savefig(save_plot, format='png')
