import os
import sys
import pprint
import logging
import json

from pyflowater import PyFlo

def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def main():
    user = os.getenv('FLO_USER', None)
    password = os.getenv('FLO_PASSWORD', None)

    if (user == None) or (password == None):
        print("ERROR! Must define env variables FLO_USER and FLO_PASSWORD")
        raise SystemExit

    pp = pprint.PrettyPrinter(indent = 2)
 
    flo = PyFlo(user, password)

    print(f"User = #{flo.user_id}")

    locations = flo.locations()

    for location in locations:
        for device in location['devices']:
            id = device['id']
            print("device id:",id)

            deviceinfo = flo.device(id)

            telemetry = deviceinfo['telemetry']
            current = telemetry['current']
            psi = current['psi']
            gpm = current['gpm']
            time = current['updated']

            print("psi:",psi)
            print("gpm:",gpm)
            print("timestamp:",time)


if __name__ == "__main__":
    main()