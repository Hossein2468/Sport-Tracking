import xml.etree.ElementTree as ET
import datetime 
from math import cos, asin, sqrt, pi
from flask import Flask 
app = Flask(__name__ , static_folder='static_files')


f = open("F:\Hossein2468\Sport-Tracking\gpx files\Road_Ride__37.gpx" , "r")
data = f.read() 
myroot = ET.fromstring(data)

a = myroot.tag 
# removing gpx from the end of a 
namespace = a[1:-4]
salam = {'gpx' : namespace}
track = myroot.find('gpx:trk' , salam)
track_segment = track.find('gpx:trkseg' , salam)
track_points_elements = track_segment.findall('gpx:trkpt' , salam)
trackpoints = [] 
for b in track_points_elements : 
    latitude = b.attrib['lat']
    longitude = b.attrib['lon']
    time = b.find('gpx:time' , salam).text 
    elevation = b.find('gpx:ele' , salam).text 
    trackpoints.append((latitude , longitude , time , elevation))
num = 1
for loop in trackpoints : 
    if num == 1 : 
        time1 = datetime.datetime.strptime(loop[2] , '%Y-%m-%dT%H:%M:%S.%fZ') 
        hour1 = time1.hour 
        min1 = time1.minute 
        sec1 = time1.second 
        lat1 = float(loop[0])
        lon1 = float(loop[1])
    if num == len(trackpoints) : 
        time2 = datetime.datetime.strptime(loop[2] , '%Y-%m-%dT%H:%M:%S.%fZ') 
        hour2 = time2.hour  
        min2 = time2.minute  
        sec2 = time2.second
        lat2 = float(loop[0]) 
        lon2 = float(loop[1])
    num += 1 
lhour = (hour2 - hour1) * 3600
lmin = (min2 - min1) * 60 
lsec = sec2 - sec1 
ltime = lhour + lmin + lsec 

def distance(lat1, lon1, lat2, lon2):
    p = pi/180
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    return 12742 * asin(sqrt(a)) 

ldistance = (distance(lat1 , lon1 , lat2 , lon2) * 1000)
avarage_speed = ldistance / ltime