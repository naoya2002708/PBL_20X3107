
import MySQLdb


def connect():
    con = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="Naoya0781",
        db="user",
        use_unicode=True,
        charset="utf8")
    return con

con = connect()

cur = con.cursor()

cur.execute("""INSERT INTO list 
            (name,height,weight,sex,age,password) 
            VALUES ('高山','180','65','M',20, 'Naoya708')""")

con.commit()

con.close()