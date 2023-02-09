import sqlite3

list_ = [1, 20, 354]
conn = sqlite3.connect('example.db')
c = conn.cursor()

#Create table
c.execute('''Create TABLE if not exists server(poke0001)''')

#Insert links into table
def data_entry():
    for i in range(6,2000, 5):

        #c.execute("INSERT INTO server(sites) VALUES(?)", (item,))
        name = "poke{}{}".format("0"*((i<10)+(i<100)+(i<1000)), i)
        c.execute("ALTER TABLE server ADD COLUMN {} real DEFAULT 0".format(name))
    conn.commit()

data_entry()

conn.close()