import sys, argparse, csv
import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from  more_itertools import unique_everseen


def MinMax(file_name,year, mode):
    """Open Cities.txt file."""
    try:
        with open(sys.argv[1], 'r') as the_file:
          filename=the_file.read()
          
    except IOError as err:
        print("Unable to open the file", file_name, "Ending program...\n", err)
        sys.exit()
    else:
        return filename

"""Cities.txt Year as an argument"""     
try:
   my_file = MinMax(sys.argv[1],sys.argv[2], 'r')
except:
   print("MinMax needs two arguments", "\nEnding program...\n")
   sys.exit()


extension=".csv"
for line in my_file.splitlines():
  file_name=line+extension  #createlist of csv file based on Cities.txt file
  
 
  try:
    with open('data/'+file_name, "rU") as files:
      
      user_input=sys.argv[2]
      check_year_in_file=[x[0] for x in csv.reader(files)]
      
      if user_input in check_year_in_file:
       with open('data/'+file_name, "rU") as files: 
        max_min_temp = [x[3:5] for x in csv.reader(files) if str(x[0]) == sys.argv[2]] #extracting min/max temp for the year passed as an argument
        max_temp=list(zip(*max_min_temp))[0]
        max_temp = ['0' if x is '' else x for x in max_temp] 
        min_temp = list(zip(*max_min_temp))[1]
        min_temp = ['0' if x is '' else x for x in min_temp] 
        fig = plt.figure()
        plt.plot(max_temp, 'r', label="Max")
        plt.plot(min_temp, 'g', label="Min")
        plt.xlim(0,400)
        plt.xlabel("Days")
        plt.ylabel("Temperature")
        title='Min/Max Daily Temp for ' +line + ' Year - '+sys.argv[2]
        plt.title(title,fontsize=14)
        plt.legend()
        plt.pause(2)
        plt.draw()
        figs=None
        save_plot = PdfPages("Min_Max_Daily_Temp.pdf")
        if figs is None:
           figs = [plt.figure(n) for n in plt.get_fignums()]
        for fig in figs:
          fig.savefig(save_plot, format='pdf')
        save_plot.close()
      else:
       print("No data available for Year - "+sys.argv[2])  
       break
      


       
     
  except IOError as err:
    print("error", err)
    






