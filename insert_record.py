
import MySQLdb


def connect():
    con = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="Naoya0781",
        db="record",
        use_unicode=True,
        charset="utf8")
    return con

con = connect()

cur = con.cursor()

cur.execute("""INSERT INTO list 
            (record_date,steps) 
            VALUES ('20221017','2000')""")

con.commit()

con.close()