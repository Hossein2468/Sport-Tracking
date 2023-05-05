import xml.etree.ElementTree as ET
import datetime 
from math import cos, asin, sqrt, pi
import os
from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, url_for

UPLOAD_FOLDER = 'F:\\Hossein2468\\Sport-Tracking\\UPLOAD_FOLDER'
ALLOWED_EXTENSIONS = {'gpx'}

app = Flask(__name__ , static_folder='static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_gpx_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Click "choose file" button to upload your gpx file</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/elements' , methods=['GET']) 
def gpx_elements():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
    f = open(f"F:\\Hossein2468\\Sport-Tracking\\UPLOAD_FOLDER\\{filename}" , "r")
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

    def distance(lat1, lon1, lat2, lon2):
        p = pi/180
        a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
        return 12742 * asin(sqrt(a))
    
    for b in track_points_elements : 
        latitude = b.attrib['lat']
        longitude = b.attrib['lon']
        time = b.find('gpx:time' , salam).text 
        elevation = b.find('gpx:ele' , salam).text 
        trackpoints.append((latitude , longitude , time , elevation))
    num = 1
    last_distance = 0 
    avarage_speed_chart = []
    for loop in trackpoints :
        if num == 1 : 
            time1 = datetime.datetime.strptime(loop[2] , '%Y-%m-%dT%H:%M:%S.%fZ') 
        if num == len(trackpoints) : 
            time2 = datetime.datetime.strptime(loop[2] , '%Y-%m-%dT%H:%M:%S.%fZ') 
            last_time = (time2 - time1).total_seconds()
        if num % 2 != 0 :
            lat1 = float(loop[0])
            lon1 = float(loop[1])
        if num % 2 == 0 : 
            lat2 = float(loop[0]) 
            lon2 = float(loop[1])
            last_position = distance(lat1 , lon1 , lat2 , lon2)
            last_distance += last_position 
        if num % 5 == 0 and num % 10 != 0 : 
            time3 = datetime.datetime.strptime(loop[2] , '%Y-%m-%dT%H:%M:%S.%fZ')
            l_distance = last_position
        if num % 10 == 0 : 
            time4 = datetime.datetime.strptime(loop[2] , '%Y-%m-%dT%H:%M:%S.%fZ')
            l_time = (time4 - time3).total_seconds()
            l_distance = (last_distance - l_distance) * 1000 
            a_speed = l_distance / l_time
            avarage_speed_chart.append(l_time)
        num += 1 
    last_distance = last_distance * 1000
    avarage_speed = last_distance / last_time
    return app.send_static_file('elements.html')


if __name__ == '__main__' : 
    app.run(host='0.0.0.0' , port=80)