import pySBB
import pandas as pd
import numpy as np
import glob


# open all cities data
cities = r'H:\PycharmProjects\untitled1\Swiss_stops.csv'
cities = pd.read_csv(cities, sep=',', encoding='utf-8')
city_names = list(cities['Nom'])
cities_shape = cities.shape

# join arrays despite the redundancy
times_arrays = glob.glob(r'H:\PycharmProjects\untitled1\*.npy')

if len(times_arrays) != 0:

    for n, time_arr in enumerate(times_arrays):
        if n == 0:
            final_arr = np.load(time_arr, allow_pickle=True)
        else:
            final_arr = np.concatenate((final_arr, np.load(time_arr, allow_pickle=True)))

    # save only unique based on name
    unique_name_idx = np.unique(final_arr[:,0], return_index=True)[1]
    final_arr = final_arr[unique_name_idx]

    np.save('final_time_array.npy', final_arr)
    print('Saved new array with shape {}'.format(final_arr.shape))

else:
    final_arr = np.zeros((2,2))

# Check if all stops were already checked
final_arr = np.load(r'H:\PycharmProjects\untitled1\final_time_array.npy', allow_pickle=True)
names_to_search = []
for city_name_ in city_names:
    if city_name_ not in final_arr[:,0]:
        names_to_search.append(city_name_)

print('Travel times to find: {}'.format(len(names_to_search)))


times = []
for n_, city_ in enumerate(names_to_search):
    city = city_
    connections = pySBB.get_connections("Zürich HB", city, time='08:00')

    trip_time = 0
    for n_connections, c in enumerate(connections):
        trip_time = + c.duration.seconds
    try:
        trip_time = trip_time / n_connections
        times.append([city, trip_time])
        times_array = np.array(times)
    except:
        times.append([city, 0])
        times_array = np.array(times)

    np.save('fetched_times_additional.npy', times_array, allow_pickle=True)

    print('Done {}%, Zurich to {}'.format(round(n_ / len(names_to_search)*100, 4), city))

print('Done!')


