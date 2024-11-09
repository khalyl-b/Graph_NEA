import sqlite3



conn = sqlite3.connect('Resources/SaveData/SaveData.db')
curs = conn.cursor()
curs.execute("SELECT * FROM Account_info")
a = curs.fetchall()
print(a)

curs.execute("SELECT * FROM Folder_info")
a = curs.fetchall()
print(a)

curs.execute("SELECT * FROM Graph_info")
a = curs.fetchall()
print(a)

conn.commit()
conn.close()


