# Sim Engine
import PlayGen
import random
from Utility import Abbreviator
from StatScraper import Scraper
import matplotlib.pyplot as plt


class SimEngine:
    def __init__(self, team1, team2, stats):

        team1Dict = stats[team1]
        team2Dict = stats[team2]
        team1Plays = float(team1Dict["offense"]["plays_per_drive"])
        team2Plays = float(team2Dict["offense"]["plays_per_drive"])
        team1TimeList = (team1Dict["offense"]["time_avg"]).split(":")
        team2TimeList = (team2Dict["offense"]["time_avg"]).split(":")
        team1Time = int(team1TimeList[0]) * 60 + int(team1TimeList[1])
        stats[team1]["time"] = team1Time/team1Plays
        team2Time = int(team2TimeList[0]) * 60 + int(team2TimeList[1])
        stats[team2]["time"] = team2Time/team2Plays
        
        self.team1 = team1
        self.team2 = team2
        self.stats = stats
        self.offense = team1
        self.defense = team2
        self.half = 1
        self.time = 1800
        self.down = 1
        self.ydsRemaining = 10
        self.ball = 20
        self.scoreBoard = {team1 : 0, team2: 0}
        self.abb = Abbreviator()
    
    def drive(self):
        coach = PlayGen.PlayCaller(self.stats[self.offense]["offense"], self.stats[self.defense]["defense"])
        quarterback = PlayGen.Pass(self.stats[self.offense]["qb"], self.stats[self.defense]["defense"])
        rushers = PlayGen.Rush(self.stats[self.offense]["rushers"], self.stats[self.defense]["defense"])
        print()
        print("~~~~~~~~~~~~ Team with possession:", self.offense, "~~~~~~~~~~~~~")
        print()
        self.ydsRemaining = 10
        self.down = 1
        turnover = False

        while(self.down < 4 and self.ball > 0 and turnover == False and self.time > 0):
            # Print ball placement info
            if (self.ball + self.ydsRemaining >= 100):
                print(self.down, "& Goal")
            else:
                print(self.down, "&", self.ydsRemaining)
        
            if self.ball > 50:
                print("Ball on", self.defense,  100 - self.ball)
            else:
                print("Ball on", self.offense,  self.ball)
            print()

            play = coach.callPlay()

            if (play == "throw"):
                throw = quarterback.passPlay()
                if throw > 0:
                    print(self.stats[self.offense]["qb"]["name"], "completed pass for a gain of", throw, "yards.")
                    self.ydsRemaining -= throw
                    self.ball += throw
                elif throw == 0:
                    print(self.stats[self.offense]["qb"]["name"], "pass incomplete.")
                else:
                    throw = abs(throw)
                    if self.ball + throw < 100:
                        self.ball += throw
                    else:
                        self.ball = 80
                    turnover = True
                    if self.ball > 50:
                        placement = self.defense + " " + str(100 - self.ball) 
                    else:
                        placement = self.offense + " " + str(self.ball)
                    print(self.stats[self.offense]["qb"]["name"], "pass intercepted. Downed at", placement + ".", "Turnover!")

            elif (play == "run"):
                a = rushers.rushPlay()

                # TypeError temp fix
                while(type(a) == int):
                    a = rushers.rushPlay()
                    
                run = a[0]
                rusherName = a[1]
                if (run >= 0):
                    print(rusherName, "carry for a gain of", run, "yards.")
                    self.ydsRemaining -= run
                    self.ball += run
                else:
                    if self.ball < 95:
                        self.ball += 5
                    turnover = True
                    if (self.ball > 50):
                        placement = self.defense + " " + str(100 - self.ball) 
                    else:
                        placement = self.offense + " " + str(self.ball)
                    print(rusher, "fumble. Downed at", placement + ".", "Turnover!")

            else:
                blitz = 5 # Edit later
                self.ball -= 5
                self.ydsRemaining += 5
                print(self.stats[self.offense]["qb"]["name"], "sacked for a loss of", blitz, "yards.")
            
            # Remove time remaining
            self.time -=  self.stats[self.offense]["time"]                                                                                                                                                               
            # Down counter
            self.down += 1

            
            if (self.ydsRemaining <= 0 and self.ball <= 100):
                print("First Down!")
                self.down = 1
                self.ydsRemaining = 10

            if (self.ball >= 100 and turnover == False):
                print("Touchdown " + self.offense + "!")
                self.scoreBoard[self.offense] += 7
                self.down = 5
            

            print()
        if (turnover == True):
            turnover = False
            temp = self.defense
            self.defense = self.offense
            self.offense = temp
            self.ball = 100 - self.ball
            self.down = 1
            self.ydsRemaining = 10
        elif (self.ball <= 0):
            print("Turnover on safety!")
            self.ball = 30
            temp = self.defense
            self.defense = self.offense
            self.offense = temp
            self.down = 1
            self.ydsRemaining = 10
        elif (self.down == 4):
            if (self.ball >= 65):
                print(self.offense, "field goal try.")
                # Add new random func here
                self.scoreBoard[self.offense] += 3
                print("Field goal try is GOOD!")
                temp = self.defense
                self.defense = self.offense
                self.offense = temp
                self.down = 1
                self.ydsRemaining = 10
            else:
                print(self.offense, "punts the ball.")
                self.ball = 25 # New random func here
                print("Ball downed on", self.defense, self.ball, "yd-line.")
                temp = self.defense
                self.defense = self.offense
                self.offense = temp
                self.down = 1
                self.ydsRemaining = 10
            self.ball = 25
        elif (self.time <= 0):
            if (self.half == 1):
                print("==================== END OF THE 1ST HALF ====================")
            else:
                print("==================== END OF THE GAME ====================")
        else:
            temp = self.defense
            self.defense = self.offense
            self.offense = temp
            self.down = 1
            self.ydsRemaining = 10
            self.ball = 25



    def simGame(self):
        for i in range(2):
            while (self.time > 0):
                self.drive()
                print("====================", self.scoreBoard, "====================")
            self.time = 1800
            self.half = 2
            self.defense = self.team1
            self.offense = self.team2
            self.down = 1
            self.ydsRemaining = 10
            self.ball = 25



if __name__ == "__main__":
    print(".__   __.  _______  __              _______. __  .___  ___.  __    __   __          ___   .___________.  ______   .______       __ ")
    print("|  \ |  | |   ____||  |            /       ||  | |   \/   | |  |  |  | |  |        /   \  |           | /  __  \  |   _  \     |  |")
    print("|   \|  | |  |__   |  |           |   (----`|  | |  \  /  | |  |  |  | |  |       /  ^  \ `---|  |----`|  |  |  | |  |_)  |    |  |")
    print("|  . `  | |   __|  |  |            \   \    |  | |  |\/|  | |  |  |  | |  |      /  /_\  \    |  |     |  |  |  | |      /     |  | ")
    print("|  |\   | |  |     |  `----.   .----)   |   |  | |  |  |  | |  `--'  | |  `----./  _____  \   |  |     |  `--'  | |  |\  \----.|__|")
    print("|__| \__| |__|     |_______|   |_______/    |__| |__|  |__|  \______/  |_______/__/     \__\  |__|      \______/  | _| `._____|(__)")
    print()
    print()
    abb = Abbreviator()
    print("Team Index")
    print("--------------------")
    for i in range(len(abb.teamIndex)):
        print(i + 1, "---", abb.teamIndex[i])
    print("--------------------")
    print()
    i1 = input("Enter team 1 value (number from 1 to 32): ")
    i2 = input("Enter team 2 value (number from 1 to 32): ")
    
    a = abb.findTeam(int(i1) - 1)
    b = abb.findTeam(int(i2) - 1)

    myScraper = Scraper()
    myScraper.scrape()
    statDict = myScraper.gather(a, b)
    
    mySim = SimEngine(abb.abbreviate(a), abb.abbreviate(b), statDict)
    mySim.simGame()
