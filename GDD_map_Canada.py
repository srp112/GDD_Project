from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import sys

FolderName = 'data'

def get_marker_color(GDD):
    # Returns red for small GDD, yellow for moderate
    #  GDD, and green for significant GDD.
    if GDD < 3.0:
        return ('ro')
    elif GDD < 7.0:
        return ('yo')
    else:
        return ('go')

#Plotting map of Canada
map = Basemap(llcrnrlon=-145.9927, llcrnrlat=44.49, urcrnrlon=-35.4459, urcrnrlat=71.8125,
              projection='lcc', resolution = 'h', area_thresh = 10000.0,
 lat_1=-4., lat_0=30.83158, lon_0=-50.)


map.drawmapboundary(fill_color='aqua')
map.fillcontinents(color='grey', lake_color='aqua', zorder = 0)
map.drawcoastlines(color = '0.15')
map.drawcountries()

# Location of St. John's, Vancouver, Regina, Saskatoon, Montreal, Toronto
lons = [-52.707866, -123.151382, -104.635418, -106.646736, -73.563254, -79.400041]
lats = [47.570861, 49.406457, 50.834696, 52.139572, 45.500137, 43.670495] 
# convert to map projection coords.
# Note that lon,lat can be scalars, lists or numpy arrays.
x,y = map(lons,lats)
# convert back to lat/lon

marker_string = get_marker_color(mag)
map.plot(x, y, marker_string, markersize=10)  # plot a colorful dot there

labels = ['St. John\'s', 'Vancouver', 'Regina', 'Saskatoon', 'Montreal', 'Toronto']
for label, xpt, ypt in zip(labels, x, y):
    plt.text(xpt+100000,ypt+100000, label) #distance of labels: 10 Km East and 10 Km North

plt.show()

#Read GDD data
with open(sys.argv[1], 'r') as cf:
	for filename in cf.read().splitlines():
		GDD = []
		with open(FolderName + '/' + filename + '.csv', 'r') as f:
			reader = csv.DictReader(f)
			for row in reader:
				if row['GDD'] != '':
					GDD.append(row)
		for value in GDD:
			print(value['Year'], '/', value['Month'], '/', value['Day'], ' ', value['GDD']) 
