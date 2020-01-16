# SBB_times_ZH
A fun project to see how long does it take to get somewhere in Switzerland with SBB from Zurich (or from any other stop).

# The idea
I am a resident of Switzerland and a huge fan of weekend single day hiking trips. Public transport in Switzerland is excellent and allows to travel almost everywhere. However, there is not much fun spending half of a day on a train/bus and only a fraction of it at the place.
I had an idea to create a map where the time travel (and ticket price) to various places would be easily indicated. This is the implementation of this idea!

## Preparation
First I had to get the list of all stops in Switzerland. It is really surprising how much free databases from Switzerland are available online. On https://opendata.swiss/en/ there is plenty of different datasets, including the list of all public transport stops. There is 27680 of them in Switzerland!
As I learned already multiple times, the distance to place is not always correlated with the travel time (that's why I had the idea of this map). To the next point was to check how long does it take to travel somewhere with SBB. Fortunately, there is an API for searching SBB connections, already in Python (PySBB). First idea was to get the data for all stops (27680 x 27680) but I quickly dropped the idea. Firstly, SBB webserver API has 1000 requests limit per day per IP. Secondly, honestly, I cared only about Zurich where I live in.
The last thing which I was completely unaware but very important if I would like to plot anything. Apparently, Switzerland does not use the standard coordinate system, but one centred on... Bern. Fortunately, there is available easy conversion script also in Python (and other languages) called Swisstopo-WGS84-LV03 available on Github (https://github.com/ValentinMinder/Swisstopo-WGS84-LV03).

## Implementation
In the beginning, I have fetched the travel times from SBB and saved them as a single numpy array. Due to the fact that there are only 1000 requests per day per IP, I had to save and merge the new data with already fetched.
Secondly, having all travel times from Zurich, HB I could add them in pandas to CSV file. In addition I also converted the LV03 to WGS84 coordinates and also added them to csv.
Plotting the map was slightly more challenging than expected. I used the google maps python plotting library (GoogleMapPlotter). It's not optimal but works. Maybe someone else could try to improve the visualisation of the data. The distances are showed from Red to Blue/Purple based on the hue shift in HSV. This is the parts I struggled the most ;)


## Quick look at the map
![alt text](https://github.com/dzyla/SBB_times_ZH/blob/master/Untitled1.png)

Is there anything interesting what the map shows? It's quite easy and relatively fast to get to most places in Switzerland. There are some outliers (St. Galen and Appenzeller cantons) where is relatively close but hard to get. It takes longer to get to not very populated places which are quite close (e.g. UNESCO Biosphäre Entlebuch). There is also a lot of Switzerland which is not available by public transport, mostly due to high mountains. Another observation is that it is much easier to travel to places north from the mountains.

## Final thoughts
Overall, I was expecting slightly bigger differences, but as I mentioned already, it was a fun project. The data can be used in many other plots and analyses. In theory, the same map can be done from any other public transport stop in Switzerland, once would have to replace the reference city in the get_sbb_times.py.
