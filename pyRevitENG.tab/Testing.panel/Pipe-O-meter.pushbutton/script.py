"""
Pipe-O-meter
Version: 1.0
Date : 06/10/18
Autor: Pablo Derendinger 
pyrevit: 4.5
"""

__title__ = 'Pipe-O-meter'


from pyrevit import script
from pyrevit.extensions import extensionmgr
from os import path

logger = script.get_logger()
logger.set_quiet_mode()

import sqlite3
import os
from os import path
from datetime import datetime

DBpath = os.path.expanduser(r'~\log.sqlite')
conn = sqlite3.connect(DBpath)

output = script.get_output()


def createGraphic():
    rows=[]
    for row in conn.execute("SELECT date FROM elements WHERE category LIKE '%s'" %('Pipes') ):
        date = datetime.fromtimestamp(int(row[0]))
        date = date.strftime('%H:%M:%S')
        rows.append(date)
    
    data =[]

    for row in conn.execute("SELECT length FROM elements WHERE category LIKE '%s'" %('Pipes')):
        data.append(row[0])

    
    chart = output.make_line_chart()

    set_a = chart.data.new_dataset('set_a')
    chart.data.labels =rows
    set_a.data = data
    chart.draw()

createGraphic()



logger.reset_level()
