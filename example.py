from StatsDB import StatsDB

if __name__ == "__main__":
    db = StatsDB("ex_db.csv")
    db.print()
    db.query("Op.Hz", "#CX")
    db.query("Op.Hz", "#MVM")
    db.query("J/pkt", "#PAP")
    # db.query("W/Op")
    db.write_db_to_csv("ex_op_db.csv")