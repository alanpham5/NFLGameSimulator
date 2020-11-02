import numpy as np
import random

class Pass:
    def __init__(self, qbDict, defDict):
        self.avgYds = (float(qbDict["pass_yds_per_cmp"]) + float(defDict["pass_net_yds_per_att"])) / 2
        oppCmpPct = 100 * float(defDict["pass_cmp"]) / float(defDict["pass_att"])
        self.cmpPct = (float(qbDict["pass_cmp_perc"]) + oppCmpPct) / 2
        oppIntPct = 100 * float(defDict["pass_int"]) / float(defDict["pass_att"])
        self.intPct = (float(qbDict["pass_int_perc"]) + oppIntPct) / 2
        self.lngAtt = int(qbDict["pass_long"])


    def getLength(self):
        yards = np.random.normal(self.avgYds, self.avgYds/3)
        
        if (yards > self.avgYds) and (np.random.uniform(0,1) > 0.3):
            yards = np.random.triangular(self.avgYds, yards, self.lngAtt)
        
        return abs(int(yards))

    def completionGenerator(self):
        throw = np.random.uniform(0,1)
        
        if (throw * 100) <= self.cmpPct:
            return True
        else:
            return False

    def passPlay(self):
        isInt = np.random.uniform(0,1)
        if (isInt * 100) < self.intPct:
            return (-1 * self.getLength())

        isComplete = self.completionGenerator()
        
        if isComplete:
            return self.getLength()
        else:
            return 0

class Rush:
    def __init__(self, rushDict, defDict):
        self.rushDict = rushDict;
        self.rushHat = []
        for k,v in rushDict.items():
            self.rushHat += ([k] * round(int(rushDict[k]["rush_att"])/ int(rushDict[k]["g"])))
        self.defRushAvg = float(defDict["rush_yds_per_att"])
        self.defFmbRate = 100 * int(defDict["fumbles_lost"])/int(defDict["rush_att"])
    
    def getLength(self, rusherAvg, rusherLong):
        avgYds = abs((rusherAvg + self.defRushAvg)/ 2)

        yards = np.random.normal(avgYds, avgYds/3)
        
        if (yards > avgYds) and (np.random.uniform(0,1) > 0.3):
            if yards < rusherLong:
                yards = np.random.triangular(avgYds, yards, rusherLong)
        
        return int(yards)

    def rushPlay(self):
        rusher = 0
        while (type(rusher) != str):
            rusher = random.choice(self.rushHat)

        rusherStats = self.rushDict[rusher]

        rusherFumbRate = 100 * int(rusherStats["fumbles"]) / (int(rusherStats["rush_att"]) + int(rusherStats["fumbles"]))

        fum = np.random.uniform(0,1)

        if (fum * 100) < (rusherFumbRate + self.defFmbRate)/2:
            return -5
        
        rusherAvg = float(rusherStats["rush_yds_per_att"])
        rusherLong = int(rusherStats["rush_long"])

        return self.getLength(rusherAvg, rusherLong), rusher

class PlayCaller:
    def __init__(self, offDict, defDict):
        offPassAtt = int(offDict["pass_att"])
        offRushAtt = int(offDict["rush_att"])
        self.passPlayPerc = 100 * offPassAtt/ (offPassAtt + offRushAtt)
        offSackPerc = 100 * int(offDict["pass_sacked"]) / offPassAtt
        defSackPerc = float(defDict["pass_sacked_perc"])
        self.sackPerc = (offSackPerc + defSackPerc) / 2
    
    def callPlay(self):
        rand = np.random.uniform(0,1)
        if (rand * 100) < self.passPlayPerc:
            rand = np.random.uniform(0,1)
            if (rand * 100) < self.sackPerc:
                return "sack"
            else:
                return "throw"
        else:
            return "run"
    

    


    



