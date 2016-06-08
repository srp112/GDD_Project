import sys, argparse, csv
import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


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
   print("MinMax needs one argument", "\nEnding program...\n")
   input("Press the enter key to exit.")
   sys.exit()

print(my_file)
extension=".csv"
for line in my_file.splitlines():
    file_name=line+extension
  
    print(file_name) 
    try:
     with open('data/'+file_name, "rU") as files:
      val = list(csv.reader(files))[1:]
      #print(val)
      max_temp = list(zip(*val))[3]
      max_temp = ['0' if x is '' else x for x in max_temp] 
      #print(b)
      min_temp = list(zip(*val))[4]
      min_temp = ['0' if x is '' else x for x in min_temp] 
      #x=np.linspace(1,365,365, endpoint=True)
      fig = plt.figure()
      plt.plot(max_temp, 'r', label="Max")
      plt.plot(min_temp, 'g', label="Min")
      plt.xlabel("Day")
      plt.ylabel("Temp.")
      plt.title("Min/Max Daily Temp "+line,fontsize=18,color='g')
      plt.legend()
      plt.pause(2)
      plt.draw()
      figs=None
      pp = PdfPages("Min_Max_Daily_Temp.pdf")
      if figs is None:
         figs = [plt.figure(n) for n in plt.get_fignums()]
      for fig in figs:
        fig.savefig(pp, format='pdf')
      pp.close()
      
      
      #print(max_temp,min_temp)
     
    except IOError as err:
       print("error", err)
    






