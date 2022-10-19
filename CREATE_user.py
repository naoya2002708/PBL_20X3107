
import MySQLdb

con = MySQLdb.connect(
    host="localhost",
    user="root",
    passwd="Naoya0781",
    db="user",
    use_unicode=True,
    charset="utf8")
cur = con.cursor()

cur.execute("""
            CREATE TABLE user.list
            (id MEDIUMINT NOT NULL AUTO_INCREMENT,
            name VARCHAR(30),
            height FLOAT(5),
            weight FLOAT(5),
            sex CHAR(1),
            age int(3),
            password VARCHAR(30),
            PRIMARY KEY(id))
            """)

con.commit()

con.close()
