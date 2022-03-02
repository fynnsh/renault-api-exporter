import os
import json
import time
import re
import sys
from prometheus_client import start_http_server, Gauge, Enum
from zozo import Zoe

myRenaultUser = "xxxxx"
myRenaultPass = "xxxxx"


# Exporter Stuff

#Battery Section
batteryLevel = Gauge('batteryLevel', 'State of Charge')
batteryTemperature = Gauge('batteryTemperature', 'Battery Temperature')
batteryAvailableEnergy = Gauge('batteryAvailableEnergy', 'Avail Energy in kwh')
plugStatus = Gauge('plugStatus', 'info')
chargingInstantaneousPower = Gauge('chargingInstantaneousPower', 'info')
chargingStatus = Gauge('chargingStatus', 'info')
chargingRemainingTime = Gauge('chargingRemainingTime', 'info')

#Location Section
gpsLongitude = Gauge('gpsLongitude', 'GPS LONG')
gpsLatitude = Gauge('gpsLatitude', 'GPS LAT')

#total Mileage
totalMileage = Gauge('totalMileage', 'GPS LAT')


if __name__ == '__main__':
    print("Renault API exporter v0.1\n")
    server_port = 3230

    print("Running on...")
    print("Port: " + str(server_port) + "\n")

    start_http_server(server_port)


    while True:

        zoe = Zoe(myRenaultUser, myRenaultPass)
        zoe.getPersonnalInfo()

        #Battery Section
        strin = str(zoe.batteryStatus())
        strin = strin.replace("\'", "\"")
        response = json.loads(strin)
        batteryLevel.set(response['data']['attributes']['batteryLevel'])
        batteryTemperature.set(response['data']['attributes']['batteryTemperature'])
        batteryAvailableEnergy.set(response['data']['attributes']['batteryAvailableEnergy'])
        plugStatus.set(response['data']['attributes']['plugStatus'])
        chargingInstantaneousPower.set(response['data']['attributes']['chargingInstantaneousPower'])
        chargingStatus.set(response['data']['attributes']['chargingStatus'])
        chargingRemainingTime.set(response['data']['attributes']['chargingRemainingTime'])

        #Location Section
        strin = str(zoe.location())
        strin = strin.replace("\'", "\"")
        strin = strin.replace(', "gpsDirection": None', '')
        strin = strin.replace('"gpsDirection": None,', '')
        response = json.loads(strin)
        gpsLongitude.set(response['data']['attributes']['gpsLongitude'])
        gpsLatitude.set(response['data']['attributes']['gpsLatitude'])
        
        strin = str(zoe.cockpit())
        strin = strin.replace("\'", "\"")
        response = json.loads(strin)
        totalMileage.set(response['data']['attributes']['totalMileage'])

        print("Query succeed")

        time.sleep(600)