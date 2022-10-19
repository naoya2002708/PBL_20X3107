
import MySQLdb

con = MySQLdb.connect(
    host="localhost",
    user="root",
    passwd="Naoya0781",
    db="record",
    use_unicode=True,
    charset="utf8")
cur = con.cursor()

cur.execute("""
            CREATE TABLE record.list
            (id MEDIUMINT NOT NULL AUTO_INCREMENT,
            record_date DATE(6),
            steps INT(6),
            PRIMARY KEY(id))
            """)

con.commit()

con.close()
