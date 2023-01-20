from StatsDB import StatsDB

if __name__ == "__main__":
    db = StatsDB("vars.csv")
    db.query("J/Op")
