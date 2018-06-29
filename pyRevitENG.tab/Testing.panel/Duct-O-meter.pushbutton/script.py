"""
Duct-O-meter
Version: 1.0
Date : 06/28/18
Autor: Pablo Derendinger 
pyrevit: 4.5
"""

__title__ = 'Duct-O-meter'


from pyrevit import script
from pyrevit.extensions import extensionmgr
from os import path

logger = script.get_logger()
logger.set_quiet_mode()

import sqlite3
import os
from os import path
from datetime import datetime, timedelta
import math
from collections import defaultdict





#region defining window
output = script.get_output()
output.window.Height= 700
output.window.Width = 300
#enregion

def getDateFromUnix(unixDate):

    date = datetime.fromtimestamp(int(unixDate))
    return date
    


def createGraphic():
    
    """Put here something """
    
    DBpath = os.path.expanduser(r'~\log.sqlite')
    conn = sqlite3.connect(DBpath)

    #Define labes, data , average and maximum
    labelsQuery = conn.execute("SELECT date FROM elements WHERE category LIKE '%s'" %('Ducts') )
    dataQuery = conn.execute("SELECT length FROM elements WHERE category LIKE '%s'" %('Ducts'))
    
    rows=[getDateFromUnix(x[0]) for x in labelsQuery] 
    data = [row[0] for row in dataQuery]
    
    conn.close()

    #Today date to compare with data dates
    today = datetime.today().date() 
    lastHour = datetime.now() - timedelta(hours = 1)
    #Fill todayRow and todayData with
    
    todayList= [ (a,b) for a,b in zip(rows,data) if a.date() == today    ]
    #Add to list if data has been added in the last hour
    lastHourData = [ b for a,b in zip(rows,data) if a >= lastHour ]
    todayRow = [x for x,y in todayList]
    todayData = [y for x,y in todayList]
    
    
    mylist=[(a,b) for a, b in todayList ]
    sums = defaultdict(float)
    
    for i, k in mylist:
        sums[str(i)] += k


    #Set averages to zero
    average = TodayAaverage = lastHourAverage= 0
    
    try:
        average = sum(data)/len(data)
        TodayAaverage = sum(todayData)/len(todayData)
        lastHourAverage = sum(lastHourData)/len(lastHourData)
    except:
        pass
    #region CHART options
    optLinearChart = {
            
            'scales': {
            'xAxes': [{
               'type': 'time',
               'time': {
                  'parser': 'YYYY-MM-DD HH:mm:ss',
                  'unit': 'day',
                  'displayFormats': {
                     'day': 'ddd'
                  },
               },
               'ticks': {
                  'source': 'data'
               }
            }]
         }}

    optTodayLineChart = {
            'legend' : {
                'display': False
                },
            'scales': {
            'xAxes': [{
               'type': 'time',
               'time': {
                  'parser': 'YYYY-MM-DD HH:mm:ss',
                  'unit': 'hour',
                  'displayFormats': {
                     'hour': 'hh:mm'
                  },
               },
               'ticks': {
                  'source': 'data'
               }
            }]
         }}

    optDouhgtChart = {
            
                'display': True,
                'text':'%s\' ducts per hour' % round(lastHourAverage, 2) ,
                'fontSize' : 30,
                'padding' : 10, 
                'wrap':True
                
        }
    #endregion

    #region History Chart
    LineChart = output.make_line_chart()
    LineChart.options = optLinearChart
    LineChart.data.labels= [str(x) for x in rows] 
    
    set_a = LineChart.data.new_dataset('Historic')
    averageData = LineChart.data.new_dataset('Average')
    [averageData.data.append(average) for x in data] 
    set_a.data = data
    set_a.tension = 0
    
    averageData.backgroundColor = 'transparent'
    
    #endregion
    
    #region Today History Chart

    TodayLineChart = output.make_line_chart()
    TodayLineChart.data.labels = [str(y) for y,x in mylist] 
    
    Todayset_a = TodayLineChart.data.new_dataset('Today')
    Todayset_a.data =[x for y,x in mylist]
    Todayset_a.tension = 0
    # TodayaverageData = TodayLineChart.data.new_dataset('Average')
    # [TodayaverageData.data.append(TodayAaverage) for x in todayData]
    
    TodayLineChart.randomize_colors()
    Todayset_a.backgroundColor = 'rgba(80, 180, 40, 0.6)'
    # TodayaverageData.backgroundColor = 'transparent'
    
    TodayLineChart.options = optTodayLineChart
    #endregion

    #region Doughnut Chart
    donutChart = output.make_doughnut_chart()
    donutChart.options.title = optDouhgtChart
    donutChart.options.legend = {'display': False}
    donutChart.options.rotation = 1 * math.pi
    donutChart.options.circumference = 1 * math.pi
    donutChart.data.labels = ["Speed",""]
    speed = donutChart.data.new_dataset('speed')
    speed.backgroundColor = ["red", "grey"]
    speed.data = [round(lastHourAverage,1), 200-round(lastHourAverage)]
    #endregion

    donutChart.draw()

    TodayLineChart.draw()
    
    LineChart.draw()
    

createGraphic()



logger.reset_level()
