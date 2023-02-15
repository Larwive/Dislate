import sqlite3

list_ = [1, 20, 354]
conn = sqlite3.connect('example.db')
c = conn.cursor()

#Create table
#c.execute('''Create TABLE if not exists server(poke0001)''')
c.execute("""
  CREATE TABLE IF NOT EXISTS players(
       id INTEGER PRIMARY KEY,
       name TEXT,
       vol INTEGER DEFAULT 0,
       color INTEGER DEFAULT 0,
       language INTEGER DEFAULT 0,
       privacy INTEGER DEFAULT 0,
       dexlink INTEGER DEFAULT 0,
       gamestats INTEGER DEFAULT 0,
       raritycolor INTEGER DEFAULT 0
  )
  """)
#Insert links into table
def data_entry():
    for i in range(6,2000, 5):

        #c.execute("INSERT INTO server(sites) VALUES(?)", (item,))
        col = "poke{}{}".format("0"*((i<10)+(i<100)+(i<1000)), i)
        c.execute("ALTER TABLE server ADD COLUMN {} real DEFAULT 0".format(col))
    conn.commit()

id, name, vol, color, privacy, dexlink, gamestats = 1732, "Yourname", 0, 6, 1, 1, 1
id2 = id+34
c.execute("INSERT INTO players (id, name, vol, color, privacy, dexlink, gamestats) VALUES(?, ?, ?, ?, ?, ?, ?)", (id, name, vol, color, privacy, dexlink, gamestats))
c.execute("INSERT INTO players (id) VALUES(?)", (id2,))
#data_entry()
c.execute("SELECT * FROM players WHERE id=={}".format(id))
res = c.fetchall()
print(res)
c.execute("SELECT {} FROM players WHERE id=={}".format("name", id))
res = c.fetchone()
print(res)
c.execute("UPDATE {} SET ({})=({}) WHERE id=={}".format("players", "name, language", " 'newname', 5" , id))
c.execute("SELECT * FROM players WHERE id=={}".format(id))
res = c.fetchone()
print(list(res))
c.execute("SELECT * FROM players".format(id))
res = c.fetchall()
print(list(res))
conn.close()
