
import MySQLdb


def connect():
    con = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="Naoya0781",
        db="test2",
        use_unicode=True,
        charset="utf8")
    return con

lists=[["鈴木","M","法政大学","投手",2],
        ["井上","M","社会人","内野手",3],
        ["井口","M","大学","監督",1]]
        
for i in range(len(lists)):



    con = connect()

    cur = con.cursor()

    cur.execute("""INSERT INTO list 
                (name,sex,school,post,admin) 
                VALUES (%(name)s,%(sex)s,%(school)s,%(post)s,%(admin)s)""",
                {"name":lists[i][0],"sex":lists[i][1],"school":lists[i][2],
                "post":lists[i][3],"admin":lists[i][4]})

    con.commit()

    con.close()