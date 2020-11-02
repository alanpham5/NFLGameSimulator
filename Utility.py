class Abbreviator:
    abbrev = {
        "Arizona Cardinals" : "ARI",
        "Atlanta Falcons" : "ATL",
        "Baltimore Ravens": "BAL",
        "Buffalo Bills": "BUF",
        "Carolina Panthers": "CAR",
        "Chicago Bears": "CHI",
        "Cincinnati Bengals": "CIN",
        "Cleveland Browns": "CLE",
        "Dallas Cowboys": "DAL",
        "Denver Broncos": "DEN",
        "Detroit Lions": "DET",
        "Green Bay Packers": "GNB",
        "Houston Texans": "HOU",
        "Indianapolis Colts": "IND",
        "Jacksonville Jaguars": "JAX",
        "Kansas City Cheifs": "KAN",
        "Las Vegas Raiders": "LVR",
        "Los Angeles Chargers": "LAC",
        "Los Angeles Rams": "LAR",
        "Miami Dolphins": "MIA",
        "Minnesota Vikings": "MIN",
        "New England Patriots": "NWE",
        "New Orleans Saints": "NOR",
        "New York Giants": "NYG",
        "New York Jets": "NYJ",
        "Philadelphia Eagles": "PHI",
        "Pittsburgh Steelers": "PIT",
        "San Francisco 49ers": "SFO",
        "Seattle Seahawks": "SEA",
        "Tampa Bay Buccaneers": "TAM",
        "Tennessee Titans": "TEN",
        "Washington Football Team": "WAS"
        }
    
    def abbreviate(self, teamName):
        return self.abbrev[teamName]

    def unabbreviate(self, abbreviation):
        for k,v in self.abbrev.items():
            if v == abbreviation:
                return k
        