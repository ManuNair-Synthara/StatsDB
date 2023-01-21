from StatsDB import StatsDB

if __name__ == "__main__":
    db = StatsDB("vars.csv")
    db.print()
    db.query("Op.Hz", "#CX")
    db.query("Op.Hz", "#MVM")
    db.query("J/pkt", "#PAP")
    # db.query("W/Op")
    db.write_db_to_csv("op.csv")