import pickle
from Utility import Abbreviator
import codecs
import os
from bs4 import BeautifulSoup

'''
url = 'https://www.pro-football-reference.com'
urlPathList = ["passing.htm","rushing.htm", "opp.htm"]
year = 2020
'''
class Scraper:
    def scrape(self):
        myDict = self.getPassingData()
        with open("./pickle/passing.pickle", "wb") as data:
            pickle.dump(myDict, data, protocol=pickle.HIGHEST_PROTOCOL)
        
        myDict = self.getRushingData()
        with open("./pickle/rushing.pickle", "wb") as data:
            pickle.dump(myDict, data, protocol=pickle.HIGHEST_PROTOCOL)
        
        myDict = self.getTeamOffense()
        with open("./pickle/offense.pickle", "wb") as data:
            pickle.dump(myDict, data, protocol=pickle.HIGHEST_PROTOCOL)
        
        myDict = self.getTeamDefense()
        with open("./pickle/defense.pickle", "wb") as data:
            pickle.dump(myDict, data, protocol=pickle.HIGHEST_PROTOCOL)
        

    def getPassingData(self):
        #htmlData = request.get.(url + "/years/" + str(year) + "/passing.htm")
        with codecs.open("./htmlFiles/2020passing.html", "r") as f:
            htmlData = f.read()
        soup = BeautifulSoup(htmlData, "lxml")
        dataTable = soup.find(id="all_passing").find("tbody")
        qbDict = dict()
        features = {"team", "gs", "pass_cmp_perc", "pass_int_perc", "pass_long", "pass_yds_per_cmp"}
        
        rows = dataTable.find_all("tr")
        for row in rows:
            if (row.find("th", {"scope":"row"}) != None):
                data = row.find("td",{"data-stat": "pos"})
                stripped = data.text.strip().encode()
                pos = stripped.decode("utf-8")

                if pos == "qb":
                    collection = dict()
                    data = row.find("td",{"data-stat": "player"})
                    stripped = data.text.strip().encode()
                    name = stripped.decode("utf-8") 
                    
                    for feature in features:
                        cell = row.find("td",{"data-stat": feature})
                        sCell = cell.text.strip().encode()
                        stat = sCell.decode("utf-8")
                        collection[feature] = stat

                    qbDict[name] = collection         
        
        return qbDict

    def getRushingData(self):
        #htmlData = request.get.(url + "/years/" + str(year) + "/rushing.htm")
        with codecs.open("./htmlFiles/2020rushing.html", "r") as f:
            htmlData = f.read()
        soup = BeautifulSoup(htmlData, "lxml")
        dataTable = soup.find(id="all_rushing").find("tbody")
        rushDict = dict()
        features = {"team", "g", "rush_att", "rush_long", "rush_yds_per_att", "fumbles"}
        
        rows = dataTable.find_all("tr")
        for row in rows:
            if (row.find("th", {"scope":"row"}) != None):
                data = row.find("td",{"data-stat": "rush_att"})
                stripped = data.text.strip().encode()
                att = int(stripped.decode("utf-8"))

                if att >= 5:
                    collection = dict()
                    data = row.find("td",{"data-stat": "player"})
                    stripped = data.text.strip().encode()
                    name = stripped.decode("utf-8") 
                    
                    for feature in features:
                        cell = row.find("td",{"data-stat": feature})
                        sCell = cell.text.strip().encode()
                        stat = sCell.decode("utf-8")
                        collection[feature] = stat

                    rushDict[name] = collection         
        
        return rushDict                

    def getTeamOffense(self):
        #htmlData = request.get.(url + "/years/" + str(year))
        with codecs.open("./htmlFiles/2020toffense.html", "r") as f:
            htmlData = f.read()
        soup = BeautifulSoup(htmlData, "lxml")

        # Get attempt tendencies and penalties
        dataTable = soup.find(id="all_team_stats").find("tbody")
        tOffense = dict()
        features = {"g", "pass_att", "rush_att", "penalties"}
        rows = dataTable.find_all("tr")
        for row in rows:
            if (row.find("th", {"scope":"row"}) != None):
                collection = dict()
                data = row.find("td",{"data-stat": "team"})
                stripped = data.text.strip().encode()
                team = stripped.decode("utf-8") 
                
                for feature in features:
                    cell = row.find("td",{"data-stat": feature})
                    sCell = cell.text.strip().encode()
                    stat = sCell.decode("utf-8")
                    collection[feature] = stat

                tOffense[team] = collection
        
        # Time and drive data
        dataTable = soup.find(id="all_drives").find("tbody")
        rows = dataTable.find_all("tr")
        features = {"plays_per_drive", "start_avg","time_avg"}

        for row in rows:
            if (row.find("th", {"scope":"row"}) != None):
                data = row.find("td",{"data-stat": "team"})
                stripped = data.text.strip().encode()
                team = stripped.decode("utf-8") 
                
                for feature in features:
                    cell = row.find("td",{"data-stat": feature})
                    sCell = cell.text.strip().encode()
                    stat = sCell.decode("utf-8")
                    tOffense[team][feature] = stat    

        # Sack data
        dataTable = soup.find(id="all_passing").find("tbody")
        rows = dataTable.find_all("tr")
        features = {"pass_sacked", "pass_sacked_yds"}

        for row in rows:
            if (row.find("th", {"scope":"row"}) != None):
                data = row.find("td",{"data-stat": "team"})
                stripped = data.text.strip().encode()
                team = stripped.decode("utf-8") 
                
                for feature in features:
                    cell = row.find("td",{"data-stat": feature})
                    sCell = cell.text.strip().encode()
                    stat = sCell.decode("utf-8")
                    tOffense[team][feature] = stat

        # Fumble data
        dataTable = soup.find(id="all_rushing").find("tbody")
        rows = dataTable.find_all("tr")

        for row in rows:
            if (row.find("th", {"scope":"row"}) != None):
                data = row.find("td",{"data-stat": "team"})
                stripped = data.text.strip().encode()
                team = stripped.decode("utf-8") 
                
                cell = row.find("td",{"data-stat": "fumbles"})
                sCell = cell.text.strip().encode()
                stat = sCell.decode("utf-8")
                tOffense[team]["fumbles"] = stat

        return tOffense

    def getTeamDefense(self):
        #htmlData = request.get.(url + "/years/" + str(year) + "/rushing.htm")
        with codecs.open("./htmlFiles/2020tdefense.html", "r") as f:
            htmlData = f.read()
        soup = BeautifulSoup(htmlData, "lxml")
        dataTable = soup.find(id="all_team_stats").find("tbody")
        defDict = dict()
        features = {"pass_att","pass_cmp", "pass_int","pass_net_yds_per_att", "rush_att", "rush_yds_per_att","fumbles_lost", "penalties"}
        
        rows = dataTable.find_all("tr")
        for row in rows:
            if (row.find("th", {"scope":"row"}) != None):
                collection = dict()
                data = row.find("td",{"data-stat": "team"})
                stripped = data.text.strip().encode()
                name = stripped.decode("utf-8") 
                
                for feature in features:
                    cell = row.find("td",{"data-stat": feature})
                    sCell = cell.text.strip().encode()
                    stat = sCell.decode("utf-8")
                    collection[feature] = stat

                defDict[name] = collection

        # Sack data
        dataTable = soup.find(id="all_passing").find("tbody")
        rows = dataTable.find_all("tr")

        for row in rows:
            if (row.find("th", {"scope":"row"}) != None):
                data = row.find("td",{"data-stat": "team"})
                stripped = data.text.strip().encode()
                team = stripped.decode("utf-8") 
                
                cell = row.find("td",{"data-stat": "pass_sacked_perc"})
                sCell = cell.text.strip().encode()
                stat = sCell.decode("utf-8")
                defDict[team]["pass_sacked_perc"] = stat
                

        return defDict

    def gather(self, team1, team2):
        print(team1)
        print(team2)
        a = Abbreviator()
        team1a = a.abbreviate(team1)
        team2a = a.abbreviate(team2)
        statDict = dict()
        team1Stat = dict()
        team2Stat = dict()

        # Gather Quarterbacks
        with open("./pickle/passing.pickle", "rb") as data:
            myDict = pickle.load(data)

        team1GS = 0
        team2GS = 0
        for k in myDict.keys():
            if (myDict[k]['team'] == team1a) and (int(myDict[k]['gs']) > team1GS):
                team1Stat['qb'] = myDict[k]
                team1Stat['qb']['name'] = k
                team1GS = int(myDict[k]['gs'])  
            elif (myDict[k]['team'] == team2a) and (int(myDict[k]['gs']) > team2GS): 
                team2Stat ['qb'] = myDict[k]
                team2Stat['qb']['name'] = k 
                team2GS = int(myDict[k]['gs'])
        
        # Gather Rushers
        with open("./pickle/rushing.pickle", "rb") as data:
            myDict = pickle.load(data)
        team1Stat['rushers'] = dict()
        team2Stat['rushers'] = dict()

        for k in myDict.keys():
            if (myDict[k]['team'] == team1a):
                team1Stat['rushers'][k] = myDict[k]
            elif (myDict[k]['team'] == team2a):
                team2Stat['rushers'][k] = myDict[k]

        # Gather Team Offense
        with open("./pickle/offense.pickle", "rb") as data:
            myDict = pickle.load(data)
        team1Stat['offense'] = myDict[team1]
        team2Stat['offense'] = myDict[team2]

        # Gather Team Defense
        with open("./pickle/defense.pickle", "rb") as data:
            myDict = pickle.load(data)
        team1Stat['defense'] = myDict[team1]
        team2Stat['defense'] = myDict[team2] 

        statDict[team1a] = team1Stat
        statDict[team2a] = team2Stat

        return statDict





if __name__=="__main__": 
    myScraper = Scraper()
    myScraper.scrape()
    print(myScraper.gather("Los Angeles Chargers", "Las Vegas Raiders"))

    '''
    print("===========================================================")
    myDict = getPassingData()
    for k,v in myDict.items():
        print(k,"---",v)

    print()
    print()
    print()
    print("===========================================================")
    myDict = getRushingData()
    for k,v in myDict.items():
        print(k,"---",v) 


    print()
    print()
    print()
    print("===========================================================")
    myDict = getTeamOffense()
    for k,v in myDict.items():
        print(k,"---",v)

    print()
    print()
    print()
    print("===========================================================")
    myDict = getTeamDefense()
    for k,v in myDict.items():
        print(k,"---",v) 
     '''