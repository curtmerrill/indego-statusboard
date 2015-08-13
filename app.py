import csv
import requests
import io

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
    kiosk_data = []
    kiosk_headers = ["Station","Bikes","Docks"]
     
    r = requests.get('http://api.phila.gov/bike-share-stations/v1', headers=HEADERS)
    if r.status_code == 200:
        data = r.json()['features']
        for kiosk in data:
            if str(kiosk['properties']['kioskId']) in station_ids:
                kiosk_data.append({"Station": kiosk['properties']['name'],
                    "Bikes": kiosk['properties']['bikesAvailable'],
                    "Docks": kiosk['properties']['docksAvailable'] })
    else:
        kiosk_data.append({"Station": "Error fetching data"})

    si = io.StringIO()
    cw = csv.DictWriter(si, fieldnames=kiosk_headers)
    cw.writeheader()
    for row in kiosk_data:
        cw.writerow(row)
   
    output = make_response(si.getvalue())
    output.headers["Content-type"] = "text/csv"
    
    return output

if __name__ == "__main__":
    # app.debug = True
    app.run(host="0.0.0.0")
