#!/usr/bin/python

import unittest
import json
import copy
import averageData

class AverageDataTestCase(unittest.TestCase):

    def setUp(self):
        self.jsonDataSet = '{"deviceData": {"acceleration": 133, "noise": 46, "temperature": 11, "light": 457, "uv": 287, "humidity": 34, "time": "11:27:23", "pollution": 3321}, "deviceId": 5613, "location": {"type": "Point", "coordinates": [52.2944, 13.4053]}}'
        self.dataSet = json.loads(self.jsonDataSet)
        self.dataList = [self.dataSet]
        self.shortLoc = ['52.29', '13.40']
        self.a = averageData.AverageData()

    def tearDown(self):
        return

    def testCreateSingleLocationPoint(self):
        rv = self.a._createSingleLocationPoint(self.dataSet)
        self.assertEqual(self.shortLoc, rv)

    def testCompareLocations_locationDoesNotExist(self):
        rv = self.a._compareLocations(self.dataSet, self.a.shortenedLocations)
        self.assertEqual(False, rv)

    def testCompareLocations_locationDoesExist(self):
        self.a.shortenedLocations = [self.shortLoc]
        rv = self.a._compareLocations(self.dataSet, self.a.shortenedLocations)
        self.assertEqual(True, rv)

    def testCountDoubleLocations_appendsLocationToListWhenNotExisting(self):
        self.a._countDoubleLocations(self.dataList, self.a.shortenedLocations)
        self.assertEqual(True, self.shortLoc in self.a.shortenedLocations)

    def testCountDoubleLocations_appendWhenNotExisting(self):
        self.a._countDoubleLocations(self.dataList, self.a.shortenedLocations)
        self.dataList[0].update({"count": 1})
        self.assertEqual(self.dataList, self.a.locationData)

    def testCountDoubleLocations_updatesDataSetWhenExisting(self):
        self.dataList = self.dataList * 2
        self.a._countDoubleLocations(self.dataList, self.a.shortenedLocations)
        self.assertEqual(2, self.a.locationData[0]["count"])

    def testCountDoubleLocations_updatesDataSetDeviceData(self):
        self.dataList = self.dataList * 2
        self.a._countDoubleLocations(self.dataList, self.a.shortenedLocations)
        expectedData = []
        expectedData.append(copy.deepcopy(self.dataSet))
        k = expectedData[0]["deviceData"].keys()
        for i in range(len(k)):
            if k[i] in ["time"]:
                continue
            expectedData[0]["deviceData"][k[i]] *= 2
        expectedData[0].update({"count": 2})
        self.assertEqual(expectedData, self.a.locationData)

    def testCalculateAverageData(self):
        expectedData = copy.deepcopy(self.dataList)
        expectedData[0]["count"] = 2
        self.dataList = self.dataList * 2
        self.a._countDoubleLocations(self.dataList, self.a.shortenedLocations)
        rv = self.a._calculateAverageData(self.a.locationData)
        self.assertEqual(expectedData, rv)

if __name__ == "__main__":
    unittest.main()
