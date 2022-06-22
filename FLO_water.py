import os
from datetime import datetime, timezone
import pprint
import time

import mysql.connector
from pyflowater import PyFlo

cnx = mysql.connector.connect(user='root', password=os.getenv('MYSQL_PASSWORD', None),
                              host='127.0.0.1',
                              database='FLO_water')
cursor = cnx.cursor()

user = os.getenv('FLO_USER', None)
password = os.getenv('FLO_PASSWORD', None)
py_flo = PyFlo(user, password)

def adddata(flo):
    locations = flo.locations()

    for location in locations:
        for device in location['devices']:
            id = device['id']
            deviceinfo = flo.device(id)

            telemetry = deviceinfo['telemetry']
            current = telemetry['current']
            psi = current['psi']
            gpm = current['gpm']
            
            timestamp = current['updated']
            dt_timestamp = datetime.strptime(timestamp,'%Y-%m-%dT%XZ')
            cvt_dt_timestamp = dt_timestamp.replace(tzinfo=timezone.utc).astimezone(tz=None)
            new_timestamp = cvt_dt_timestamp.strftime("%Y-%m-%d %X")

            add_data = "INSERT INTO water_usage VALUES(\'"+new_timestamp+"\',"+str(psi)+","+str(gpm)+");"
            print(add_data)
            cursor.execute(add_data)
            cnx.commit()

if __name__ == "__main__":
    i = 0
    while i < 50000:
        time.sleep(5)
        adddata(py_flo)
        i+1
