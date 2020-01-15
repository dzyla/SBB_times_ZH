import colorsys
import pandas as pd
import numpy as np
import switzerland_coordinate_system_convert as scsc
import gmplot
from colour import Color

# Google maps API key to
API = ''


def rgb2hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def get_color(red_to_green):
    # This is directly taken from stackexchange
    assert 0 <= red_to_green <= 1
    # in HSV, red is 0 deg and green is 120 deg (out of 360);
    # divide red_to_green with 3 to map [0, 1] to [0, 1./3.]
    hue = red_to_green
    r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
    r, g, b = map(lambda x: int(255 * x), (r, g, b))
    return rgb2hex(r, g, b)


def normalize_list(list):
    return (list - np.min(list)) / (np.max(list) - np.min(list))


# Load list of cities in Switzerland
cities = 'Swiss_stops.csv'
cities = pd.read_csv(cities, sep=',', encoding='utf-8')
cities_shape = cities.shape

# Load travel times from Zurich and create new column
time_data = np.load('final_time_array.npy', allow_pickle=True)
cities['Travel time'] = np.zeros(cities.shape[0])

# Combine travel times with destinations
for idx, name in enumerate(cities['Nom']):

    try:
        cities.at[idx, 'Travel time'] = time_data[np.where(time_data[:, 0] == name)[0][0]][1]

    except:
        pass

# Create new columns for the coordinates conversion from Swiss to normal
cities['Coord_lat'] = np.zeros(cities.shape[0])
cities['Coord_lng'] = np.zeros(cities.shape[0])

# Convert coordinates
converter = scsc.GPSConverter()

long_list = []
lat_list = []
distance = []
travel_time = []

for idx, name in enumerate(cities['x_Coord_Nord']):
    test_x = cities.iloc[idx]['x_Coord_Nord']
    test_y = cities.iloc[idx]['y_Coord_Est']

    coords_test_lat = converter.CHtoWGSlat(test_y, test_x)
    coords_test_lng = converter.CHtoWGSlng(test_y, test_x)

    cities.at[idx, 'Coord_lat'] = coords_test_lat
    cities.at[idx, 'Coord_lng'] = coords_test_lng

    long_list.append(coords_test_lng)
    lat_list.append(coords_test_lat)

    zurich_lat, zurich_long = 47.36667, 8.55

    travel_time.append(cities.iloc[idx]['Travel time'])

# save the data as csv
cities.to_csv('all_cities_CH_time_geo.cvs', sep=',', encoding='utf-8')

# Normalize travel time for the coloring scheme
travel_time = np.array(travel_time)

# Remove a few outliers above 14000 s
travel_time[travel_time > 14000] = 14000
travel_time = normalize_list(travel_time)
unique_times = np.unique(np.array(travel_time))
red = Color("green")
colors = list(red.range_to(Color("red"), cities_shape[0]))

cities.to_csv('new_data2.csv', encoding='utf-8')

# print(travel_time)

# Generate map
gmap1 = gmplot.GoogleMapPlotter(46.8181877,
                                8.2275124, 9, apikey=API)

for idx, lat_ in enumerate(lat_list):
    frac = idx / len(lat_list)
    if travel_time[idx] != 0:
        color_value = colors[int(travel_time[idx] * cities_shape[0] - 1)].get_hex()

        # Alternative coloring scheme
        # color_value = np.where(unique_times == travel_time[idx])[0][0]
        # gmap1.scatter([lat_list[idx]], [long_list[idx]], color_value,
        #                           size = 1000, marker = False)

        # gmap1.scatter([lat_list[idx]], [long_list[idx]], colors[color_value].get_hex(),
        #               size=1000, marker=False)

        gmap1.scatter([lat_list[idx]], [long_list[idx]], get_color(travel_time[idx]),
                      size=300, marker=False)

gmap1.draw("map_noapi.html")

# Change map color to gray
map = open('map_noapi.html', 'r')
map_gray = open('map_gray_noapi.html', 'w')

var_to_map_gray = '''		var stylez = [
				{
				  featureType: "all",
				  elementType: "all",
				  stylers: [
					{ saturation: -100 } // <-- THIS
				  ]
				}
			];
		var mapType = new google.maps.StyledMapType(stylez, { name:"Grayscale" });
		map.mapTypes.set("map_canvas", mapType);
		map.setMapTypeId("map_canvas");

'''

for line in map:
    line = line.replace('\n', '')
    print(line, file=map_gray)
    if line == '		var map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);':
        print(var_to_map_gray, file=map_gray)
