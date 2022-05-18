import sys

from shapely.geometry import shape
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely.validation import make_valid
import json

def parse_geoID():
    f = open("countryInfo.txt")
    # ISO,ISO3,ISO-Numeric,fips,Country	Capital,Area(in sq km),Population,Continent,tld,CurrencyCode,CurrencyName,Phone,Postal Code Format	Postal Code Regex
    res = {}
    for line in f:
        if(line[0] != '#'):
            a = line.split("\t")
            #print(a)
            res[a[16]] = a[4]
    return res
fi = json.load(open("shapes_simplified_low.json"))
features = fi["features"]
i =0
countries = []
countriesID = []
geoDict = parse_geoID()
for country in features:
    testshape = country["geometry"]
    polygon: Polygon = shape(testshape)
    polygon = make_valid(polygon)
    countries.append(polygon)
    countriesID.append(geoDict[country["properties"]["geoNameId"]])
geo: dict = {'type': 'Polygon',
   'coordinates': [[[23.08437310100004, 53.15448536100007],
   [23.08459767900007, 53.15448536100007],
   [23.08594514600003, 53.153587050000056],
   [23.08437310100004, 53.15448536100007]]]}
polygon: Polygon = shape(testshape)
point = Point(0, 0)
countrylookup = []


def get_match(lat, lon, countries, countriesID):
    for i in range(len(countries)):
        if lat < 0:
            dsfadsfa = 0
        point = Point(lon,lat)
        country = countries[i]
        if country.contains(point):
            return countriesID[i]
    return ""
get_match(0,0,countries,countriesID)
print("a")
for i in range(180):
    a = []
    for j in range(360):
        temp = ""
        if i >= 90:
            lat = i - 180
        else:
            lat = i
        if j >= 180:
            lon = j - 360
        else:
            lon = j
        #if i > 90:
            #print(lat, lon, get_match(lat, lon, countries, countriesID))
        a.append(get_match(lat,lon,countries,countriesID))
    print(i)
    countrylookup.append(a)

print(sys.getsizeof(countrylookup),"cap")
o = open("demofile2.txt", "a")
o.truncate(0)
for i in range(len(countrylookup)):
    for j in range(len(countrylookup[0])):
        o.write(countrylookup[i][j])
        if(j < len(countrylookup[0] )- 1):
            o.write(",")
    o.write("\n")
#print(polygon.contains(point))
#print(features[0]["properties"]["geoNameId"])
#print(geoDict[features[0]["properties"]["geoNameId"]])





