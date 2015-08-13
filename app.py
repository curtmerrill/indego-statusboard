import requests

from flask import Flask
from flask import make_response
from flask import render_template
from flask import request

app = Flask(__name__)

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.5 Safari/600.5.17',
}

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/table", methods=['GET',])
def table():
    station_ids = str(request.args.get('stations')).split('-')
    kiosk_csv = "Station\tBikes\tDocks\n"
     
    r = requests.get('http://api.phila.gov/bike-share-stations/v1', headers=HEADERS)
    if r.status_code == 200:
        data = r.json()['features']
        for kiosk in data:
            if str(kiosk['properties']['kioskId']) in station_ids:
                kiosk_csv += "%s\t%s\t%s\n" % (kiosk['properties']['name'], kiosk['properties']['bikesAvailable'], kiosk['properties']['docksAvailable'])
    else:
        kiosk_csv += "Error fetching data"

   
    output = make_response(kiosk_csv)
    output.headers["Content-type"] = "text/csv"
    
    return output

if __name__ == "__main__":
    # app.debug = True
    app.run(host="0.0.0.0")
