import requests
from requests.sessions import Session
from threading import Thread, local
from queue import Queue
from cachetools import cached, TTLCache
from openweather_helper import *

cache = TTLCache(maxsize=1000, ttl=1800)

#API_KEY = [REDACTED]  # initialize your key here

cache = dict()
q = Queue(maxsize=0)
thread_local = local()
url_list = []
result = []


def data(dataset, viewport):
    result.clear()
    url_list.clear()
    res = extract_info(request_by_coord_range(viewport), dataset)
    return res


def request_by_coord_range(viewport):
    view = round_viewport(viewport)
    queue_urls(view)
    get_all_data()

    return result


def queue_urls(view):
    for lat in float_range(view['lat1'], view['lat2'] + view['interval'], view['interval']):
        for lon in float_range(view['lon1'], view['lon2'] + view['interval'], view['interval']):
            q.put('https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=minutely,hourly,daily&appid={}&units=imperial'.format(lat, lon, API_KEY))
       


def get_session() -> Session:
    if not hasattr(thread_local, 'session'):
        thread_local.session = requests.Session()
    return thread_local.session


@cached(cache)
def get_single_data() -> None:
    session = get_session()
    while True: 
        url = q.get()
        with session.get(url) as response:
            result.append(response.json())
        q.task_done()


def get_all_data() -> None:
    thread_num = 10
    for i in range(thread_num):
        t_worker = Thread(target=get_single_data)
        t_worker.start()
    q.join()


def interpolate1(data):
    result = data.copy()

    lat_lon_sorted = sorted(data, key=lambda x: (x['lat'], x['lon'])).copy()
    for i in range(len(lat_lon_sorted) - 1):
        if (lat_lon_sorted[i]['lat'] != lat_lon_sorted[i + 1]['lat']):
            continue

        new = {'lat': (lat_lon_sorted[i]['lat'] + lat_lon_sorted[i + 1]['lat']) / 2,
                'lon': (lat_lon_sorted[i]['lon'] + lat_lon_sorted[i + 1]['lon']) / 2,
                'value1': round((lat_lon_sorted[i]['value1'] + lat_lon_sorted[i + 1]['value1']) / 2, 2)}
        result.append(new)
    
    lon_lat_sorted = sorted(result, key=lambda x: (x['lon'], x['lat'])).copy()
    for j in range(len(lon_lat_sorted) - 1):
        if (lon_lat_sorted[j]['lon'] != lon_lat_sorted[j + 1]['lon']):
            continue

        new1 = {'lat': (lon_lat_sorted[j]['lat'] + lon_lat_sorted[j + 1]['lat']) / 2,
                'lon': (lon_lat_sorted[j]['lon'] + lon_lat_sorted[j + 1]['lon']) / 2,
                'value1': round((lon_lat_sorted[j]['value1'] + lon_lat_sorted[j + 1]['value1']) / 2, 2)}
        result.append(new1)
   
    return result

def interpolate2(data):
    result = data.copy()

    lat_lon_sorted = sorted(data, key=lambda x: (x['lat'], x['lon'])).copy()
    for i in range(len(lat_lon_sorted) - 1):
        if (lat_lon_sorted[i]['lat'] != lat_lon_sorted[i + 1]['lat']):
            continue

        new = {'lat': (lat_lon_sorted[i]['lat'] + lat_lon_sorted[i + 1]['lat']) / 2,
                'lon': (lat_lon_sorted[i]['lon'] + lat_lon_sorted[i + 1]['lon']) / 2,
                'value1': round((lat_lon_sorted[i]['value1'] + lat_lon_sorted[i + 1]['value1']) / 2),
                'value2': round((lat_lon_sorted[i]['value2'] + lat_lon_sorted[i + 1]['value2']) / 2)}
        result.append(new)
    
    lon_lat_sorted = sorted(result, key=lambda x: (x['lon'], x['lat'])).copy()
    for j in range(len(lon_lat_sorted) - 1):
        if (lon_lat_sorted[j]['lon'] != lon_lat_sorted[j + 1]['lon']):
            continue

        new1 = {'lat': (lon_lat_sorted[j]['lat'] + lon_lat_sorted[j + 1]['lat']) / 2,
                'lon': (lon_lat_sorted[j]['lon'] + lon_lat_sorted[j + 1]['lon']) / 2,
                'value1': round((lon_lat_sorted[j]['value1'] + lon_lat_sorted[j + 1]['value1']) / 2, 2),
                'value2': round((lon_lat_sorted[j]['value2'] + lon_lat_sorted[j + 1]['value2']) / 2, 2)}
        result.append(new1)
   
    return result
    

def extract_info(data, channel):

    if channel == 'openweather_wind':
        extracted = [{
            'lat': data[j]['lat'],
            'lon': data[j]['lon'],
            'value1': data[j]['current']['wind_speed'],
            'value2': data[j]['current']['wind_deg']
        } for j in range(len(data))]

        inter1 = interpolate2(extracted).copy()
        inter2 = interpolate2(inter1).copy()
        inter3 = interpolate2(inter2).copy()

    else:
        extracted = [{
            'lat': data[j]['lat'],
            'lon': data[j]['lon'],
            'value1': data[j]['current'][channel.split('_')[-1]]
        } for j in range(len(data))]

        inter1 = interpolate1(extracted).copy()
        inter2 = interpolate1(inter1).copy()
        inter3 = interpolate1(inter2).copy()

    
    final = sorted(inter3, key=lambda x: (x['lat'], x['lon'])).copy()
    

    return final



# User starts app. Selects which data they want to start with (Temp or Wind or Humidity or....)
# Request is made to server. Server makes a request for those coordinates grabbing all data for
# those coordinates. We return the chosen data but cache all data for an hour. If the user
# then also selects to see another type along with the the already shown one or switches
# within that hour we send that cached data to unity. If its not within the hour
# another call to weatherapi is made and process is restarted.
