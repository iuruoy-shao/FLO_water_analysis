import os
from datetime import datetime, timezone
from pickle import TRUE
import time

import mysql.connector
from pyflowater import PyFlo

cnx = mysql.connector.connect(user='root', password=os.getenv('MYSQL_PASSWORD', None),
                              host='samplehost',
                              database='FLO_water')
cursor = cnx.cursor()

user = os.getenv('FLO_USER', None)
password = os.getenv('FLO_PASSWORD', None)
py_flo = PyFlo(user, password)    


def callback(data):
    print(data)


def adddata(flo, last_ts, last_psi, last_gpm):
    locations = flo.locations()

    for location in locations:
        for device in location['devices']:
            id = device['id']
            
            py_flo.get_real_time_listener(id,callback)
            device_info = flo.device(id)

            telemetry = device_info['telemetry']
            current = telemetry['current']
            psi = current['psi']
            gpm = current['gpm']
            
            timestamp = current['updated']

            if last_gpm < 0.0001 and gpm < 0.0001:
                return gpm, psi, timestamp

            if last_gpm < 0.0001:
                insert_data(last_ts, last_psi, last_gpm)

            insert_data(timestamp, psi, gpm)
            cnx.commit()
            return gpm, psi, timestamp


def insert_data(ts, psi, gpm):
    dt_ts = datetime.strptime(ts, '%Y-%m-%dT%XZ')
    cvt_dt_ts = dt_ts.replace(tzinfo=timezone.utc).astimezone(tz=None)
    new_ts = cvt_dt_ts.strftime("%Y-%m-%d %X")

    add_data = "INSERT INTO water_usage (timestamp,psi,gpm) VALUES(\'" + new_ts + "\'," + str(psi) + "," + str(gpm) + ");"
    cursor.execute(add_data)


if __name__ == "__main__":
    last_gpm = 0
    last_psi = 0
    last_ts = ""
    while TRUE:
        time.sleep(5)
        last_gpm, last_psi, last_ts = adddata(py_flo, last_ts, last_psi, last_gpm)
