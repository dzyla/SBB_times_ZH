# SBB_times_ZH
A fun project to see how long does it take to get somewhere in Switzerland with SBB from Zurich (or from any other stop).


# The idea
I am resident of Switzeland and a huge fan of weekend single day hiking trips. Public transport in Switzerland is excellent and allows to travel to almost everywhere. However, there is not much fun spending half of a day in a train / bus and only fraction of it at the place. 

I had an idea to create a map where the time travel (and ticket price) to viarious places would be easily indicated. This is the implementation of this idea!

## Preparation
First I had to get the list of all stops in Switzerland. It is really surprising how much free databases from Switzerland are aviable online. On https://opendata.swiss/en/ there is plenty of different datasets, including the list of all public transport stops. There is 27680 of them in Switzerland!

As I learned already mutiple times, the distance to place is not always correlated with the travel time (that's why I had the idea of this map). To the next point was to check how long does it take to travel somewhere with SBB. Fortunately, there is an API for searching a SBB connections, already in Python (PySBB). First idea was to get the data for all stops (27680 x 27680) but I quickly droped the idea. Firstly, SBB webserver API has 1000 requests limit per day per IP. Secondly, honestly I cared only about Zurich where I live in.

The last thing which I was completely unaware but very important if I would like to plot anything. Apparently, Switzerland does not use the standard coordinate system but one centered on... Bern. Fortunately there is aviable easy convertion script also in Python (and other languages) called Swisstopo-WGS84-LV03 aviable on github (https://github.com/ValentinMinder/Swisstopo-WGS84-LV03).

## Implementation
In the beginning I have fetched the travel times from SBB and saved them as a single numpy array. Due to the fact, that there is only 1000 requests per day per IP, I had to save and merge the new data with already fetched. 

Secondly, having all travel times from Zurich, HB I could add them in pandas to csv file. In addition I also converted the LV03 to WGS84 coordinates and also added them to csv. 

Plotting the map was slighly more challanging than expected. I used the google maps python plotting library (GoogleMapPlotter). It's not optimal but works. Maybe someone else could try to improve the visualization of the data.

## Quick look at the map
![alt text](https://github.com/dzyla/SBB_times_ZH/blob/master/Untitled1.png)

