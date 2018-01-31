import json
import copy
import time

class AverageData():

    OUTPUT_FILE = "averageData.json"
    INPUT_FILE = "testData.json"

    def __init__(self):
        self.rawDataJson = []
        self.locationData = []
        self.shortenedLocations = []


    def _createSingleLocationPoint(self, dataSet):
        singleLocation = []
        singleLocation.append(str(dataSet["location"]["coordinates"][0])[:5])
        singleLocation.append(str(dataSet["location"]["coordinates"][1])[:5])
        return singleLocation

    def _compareLocations(self, dataSet, shortenedLocations):
        shortLoc = self._createSingleLocationPoint(dataSet)
        if shortLoc in shortenedLocations:
            return True
        else:
            return False

    def _findIndexByLocation(self, dataSet, locationData):
        for i in range(len(locationData)):
            if self._createSingleLocationPoint(dataSet) != self._createSingleLocationPoint(locationData[i]):
                continue
            return i

    def _countDoubleLocations(self, dataList, shortenedLocations):
        for dataSet in dataList:
            singleLocationData = {}
            exists = self._compareLocations(dataSet, shortenedLocations)
            if exists == False:
                shortLoc = self._createSingleLocationPoint(dataSet)
                shortenedLocations.append(shortLoc)
                singleLocationPoint = copy.deepcopy(dataSet)
                singleLocationPoint.update({"count": 1})
                self.locationData.append(singleLocationPoint)
            else:
                i = self._findIndexByLocation(dataSet, self.locationData)
                self.locationData[i]["count"] += 1
                k = dataSet["deviceData"].keys()
                for key in k:
                    if key in ["time"]:
                        continue
                    self.locationData[i]["deviceData"][key] += dataSet["deviceData"][key]

    def _calculateAverageData(self, dataList):
        if len(dataList) == 0:
            return
        data = copy.deepcopy(dataList)
        k = data[0]["deviceData"].keys()
        for i in range(len(data)):
            for key in k:
                if key in ["time"]:
                    continue
                data[i]["deviceData"][key] /= data[i]["count"]
        return data

    def _writeDataToFile(self, data, fileName):
        f = open(fileName, "w")
        f.write(json.dumps(data))
        f.close()

    def run(self):
        self.rawDataJson = json.load(open(self.INPUT_FILE))
        self._countDoubleLocations(self.rawDataJson, self.shortenedLocations)
        data = self._calculateAverageData(self.locationData)
        self._writeDataToFile(data, self.OUTPUT_FILE)
        return data

def main():
    # 22.5 s run time / 100.000 data sets
    # 0.5 s run time / 10.000 data sets
    print time.time()
    a = AverageData()
    a.run()
    print time.time()

if __name__ == "__main__":
    main()
