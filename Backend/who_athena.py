import requests

# https://www.who.int/data/gho/info/athena-api
# https://apps.who.int/gho/athena/public_docs/examples.html#ex2
ids = {"Life expectancy at birth (years)": "WHOSIS_000001"}

altnames = {"United States": "United States of America",
            "Bolivia": "Bolivia (Plurinational State of)",
            "Ivory Coast": "Cote d\'Ivoire",
            "North Korea": "Democratic People's Republic of Korea",
            "Iran": "Iran (Islamic Republic of)",
            "United Kingdom": "United Kingdom of Great Britain and Northern Ireland",
            "Tanzania": "United Republic of Tanzania",
            "Moldova": "Republic of Moldova",
            "Russia": "Russian Federation",
            "Laos": "Lao People's Democratic Republic",
            "Czechia": "Czech Republic"}

o = open("demofile2.txt", "r")
rev_geolocation = []
for line in o:
    split = line.split(",")
    curr = []
    for val in split:
        curr.append(val)
    rev_geolocation.append(curr)
# https://github.com/thampiman/reverse-geocoder


def data(dataset, viewport, time):
    return create_points(request_data(format_request(dataset, time)), viewport)


def format_request(dataset: dict, time: str) -> str:
    # id should be based on dataset -> id mapping contained in this file
    if dataset not in ids:
        return "Error finding Athens id for " + dataset
    id = ids[dataset]
    time = int(time)
    gender = True
    # https://apps.who.int/gho/athena/api/GHO/WHOSIS_000001.json?filter=YEAR:2000&profile=simple
    if (gender):
        url = f'https://apps.who.int/gho/athena/api/GHO/{id}.json?filter=YEAR:{time};SEX:BTSX&profile=simple'
        return url
    url = f'https://apps.who.int/gho/athena/api/GHO/{id}.json?filter=YEAR:{time}&profile=simple'
    return url


# Returns Dict of country -> value
def request_data(url) -> dict:
    response = requests.get(url).json()
    facts = response["fact"]
    res = {}
    for fact in facts:
        if "COUNTRY" in fact["dim"]:
            res[fact["dim"]["COUNTRY"]] = fact["Value"]
    return res


def create_points(countrymap: dict, viewport: dict):
    res = []
    latmin = min(viewport["lat1"], viewport["lat2"])
    latmax = max(viewport["lat1"], viewport["lat2"])
    lonmin = min(viewport["lon1"], viewport["lon2"])
    lonmax = max(viewport["lon1"], viewport["lon2"])
    interval = viewport["interval"]
    i = latmin
    while i < latmax:
        j = lonmin
        while j < lonmax:
            t = get_country(i, j)
            if t in countrymap:
                res.append({"lon": i, "lat": j, "value1": countrymap[t]})
            elif t in altnames and altnames[t] in countrymap:
                res.append(
                    {"lon": i, "lat": j, "value1": countrymap[altnames[t]]})
            # else:
            #     #  res.append({"lon": i, "lat": j, "value1": -1})
            #     continue
            j += interval
        i += interval
    return res


# coord to country lookup
def get_country(lat, lon) -> str:
    if lat <= 0:
        i = int(lat + 180)
    else:
        i = int(lat)
    if lon <= 0:
        j = int(lon + 360)
    else:
        j = int(lon)
    if i >= len(rev_geolocation):
        i = len(rev_geolocation )- 1
    if j >= len(rev_geolocation[0]):
        j = len(rev_geolocation[0]) - 1
    a = rev_geolocation
    return rev_geolocation[i][j]
