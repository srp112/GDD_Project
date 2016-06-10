#the cummulative GDD plot
import sys, argparse, csv
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt

def open_file(file_name, mode):
    """Open a file."""
    try:
        with open(sys.argv[1], 'r') as the_file:
          filename=the_file.read()
          
    except IOError as err:
        print("Unable to open the file", file_name, "Ending program.\n", err)
        input("\n\nPress the enter key to exit.")
        sys.exit()
    else:
        return filename

"""Cities.txt file as an argument"""     
try:
   my_file = open_file(sys.argv[1], 'r')
except:
   print("GDD needs one argument", "\nEnding program...\n")
   input("Press the enter key to exit.")
   sys.exit()


extension=".csv"
for line in my_file.splitlines():
    file_name=line+extension
    print(file_name) 
    with open('data/'+ file_name, "rU") as files:
        val = list(csv.DictReader(files))  
        l = []
    for i in range(0, len(val)):
        row = val[i]
        if row['Min Temp'] == '' or row['Max Temp'] == '':
                pass 
        else:
            GDD = ((float(row['Min Temp']) + float(row['Max Temp']))/2)-10
            l.append(GDD)

            val[i]['GDD'] = GDD
        
            #print(row['Min Temp'], ' ' , row['Max Temp'], ' ', str(round(row['GDD'], 2)))
 
            #plt.subplot(1,1,1)        
            #x = np.linspace(1, 12, 365, endpoint=True)
            
            

            """dates = ['01/02/2006','01/03/2007','01/04/2008']
            x = [dt.datetime.strptime(d,'%m/%d/%Y').date() for d in dates]
            y = range(len(x)) 
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
            plt.gca().xaxis.set_major_locator(mdates.DayLocator())"""

    x = np.linspace(1, 12, 365, endpoint=True)
    plt.plot(x,GDD, label = file_name.split(',')[0])
    plt.gcf().autofmt_xdate()
    plt.legend(loc="upper left")
            
                    
            
    plt.xlabel('Months', color='black')
    plt.ylabel('Cumulative GDD (>10°C)')
    plt.title('Accumulated Growing Degree Days')
    plt.draw()        
                   




   
    
    
  

            
 

    
