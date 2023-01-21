from StatsDB import StatsDB

if __name__ == "__main__":
    db = StatsDB("vars.csv")
    db.print()
    db.query("J/Op")
    db.query("W/Op")