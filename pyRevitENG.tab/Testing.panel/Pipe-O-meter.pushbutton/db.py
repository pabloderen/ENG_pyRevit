import sqlite3
import os.path


DBpath = os.path.expanduser(r'~\prueba.sqlite')

conn = sqlite3.connect(DBpath)
c = conn.cursor()

try:
    c.execute('''CREATE TABLE stocks
                (date text, trans text, symbol text, qty real, price real)''')
except:
    pass
c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
conn.commit()
print("works")