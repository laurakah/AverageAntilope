#!/usr/bin/python

import json
import random
import time
import copy

DATA_SET_COUNT = 1000

LONGITUDE_CONST = 520000.0
LONGITUDE_MIN = 2240
LONGITUDE_MAX = 3811
LATITUDE_CONST = 130000.0
LATITUDE_MIN = 2933
LATITUDE_MAX = 9000
SOUND_MIN = 0
SOUND_MAX = 800
LIGHT_MIN = 0
LIGHT_MAX = 600
DUST_MIN = 0
DUST_MAX = 8000
UV_MIN = 0
UV_MAX = 400
ACCELERATION_MIN = 0
ACCELERATION_MAX = 500
TEMPERATURE_MIN = -20
TEMPERATURE_MAX = 55
HUMIDITY_MIN = 0
HUMIDITY_MAX = 100

def generateData(key, min, max, dic):
    dataValue = random.randint(min, max)
    dataKey = key
    dic[dataKey] = dataValue

def generateLocation(min, max, const):
    dataValue = (const + random.randint(min, max)) / 10000.0
    return dataValue

def generateTime(dic):
    dataValue = time.strftime("%Y-%m-%dT%H:%M:%S")
    dataKey = "dateTime"
    dic[dataKey] = dataValue

def generateId(buff):
    dataValue = random.randint(0, 10000)
    dataKey = "deviceId"
    buff[dataKey] = dataValue

def wrapData(buff, dic):
    generateId(buff)
    dataValue = dic
    dataKey = "deviceData"
    buff[dataKey] = dataValue

def wrapLocation(buff):
    geoJsonWrapper = {"type": "Point"}
    coordinates = []
    coordinateKey = "coordinates"
    coordinates.append(generateLocation(LONGITUDE_MIN, LONGITUDE_MAX, LONGITUDE_CONST))
    coordinates.append(generateLocation(LATITUDE_MIN, LATITUDE_MAX, LATITUDE_CONST))
    geoJsonWrapper[coordinateKey] = coordinates
    dataKey = "location"
    buff[dataKey] = geoJsonWrapper

def writeData(data, fileName):
    json.dump(data, fileName)

def generateJson(dataSource, locationSource, dic):
    generateTime(dic)
    for keyName in dataSource.keys():
        generateData(keyName, dataSource[keyName][0], dataSource[keyName][1], dic)

def generateDataSet(dataSource, locationSource, dic, buff):
    generateJson(dataSource, locationSource, dic)
    wrapData(buff, dic)
    wrapLocation(buff)
    return buff

def main():
    dataFile = open("testData.json", "a")
    sensorData = {"noise": [SOUND_MIN, SOUND_MAX], "light": [LIGHT_MIN, LIGHT_MAX], "pollution": [DUST_MIN, DUST_MAX], "uv": [UV_MIN, UV_MAX], "acceleration": [ACCELERATION_MIN, ACCELERATION_MAX], "temperature": [TEMPERATURE_MIN, TEMPERATURE_MAX], "humidity": [HUMIDITY_MIN, HUMIDITY_MAX]}
    locationData = {"longitude": [LONGITUDE_MIN, LONGITUDE_MAX, LONGITUDE_CONST], "latitude": [LATITUDE_MIN, LATITUDE_MAX, LATITUDE_CONST]}

    dataList = []
    jsonBuffer = {}
    jsonData = {}
    for i in range(DATA_SET_COUNT):
        buff = generateDataSet(sensorData, locationData, jsonData, jsonBuffer)
        dataList.append(copy.deepcopy(buff))
    writeData(dataList, dataFile)

main()
