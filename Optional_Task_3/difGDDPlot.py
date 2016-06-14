import sys, argparse, csv
import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from  more_itertools import unique_everseen
from scipy.interpolate import spline

def Dif_GDD(file_name,year, mode):

  with open(file_name, 'r') as the_file:
    filename=the_file.read() 
    
  my_file = filename

  extension=".csv"
  for line in my_file.splitlines():
      file_name=line+extension  #createlist of csv file based on Cities.txt file
      
     
      try:
        with open('data/'+file_name, "r") as files:
          
          user_input=year
          check_year_in_file=[x[0] for x in csv.reader(files)]
          
          if user_input in check_year_in_file:
           with open('data/'+file_name, "rU") as files: 
            GDD_dif = [x[5:11] for x in csv.reader(files) if str(x[0]) == year]
            GDD_1 = list(zip(*GDD_dif))[0]
            GDD_1 = ['0' if x is '' else x for x in GDD_1]
            GDD_2 = list(zip(*GDD_dif))[1]
            GDD_2 = ['0' if x is '' else x for x in GDD_2]
            GDD_3 = list(zip(*GDD_dif))[2]
            GDD_3 = ['0' if x is '' else x for x in GDD_3]
            GDD_4 = list(zip(*GDD_dif))[3]
            GDD_4 = ['0' if x is '' else x for x in GDD_4]
            GDD_5 = list(zip(*GDD_dif))[4]
            GDD_5 = ['0' if x is '' else x for x in GDD_5]
            GDD_6 = list(zip(*GDD_dif))[5]
            GDD_6 = ['0' if x is '' else x for x in GDD_6]
            fig = plt.figure()
            #GDD_1S = np.linspace(GDD_1.min(), GDD_1.max(), 300)
            #power_smooth = spline(GDD_1, power, GDD_1S)
            plt.plot(GDD_1, 'red', label = "Tbase=10")
            plt.plot(GDD_2, 'green', label = "Tbase=11")
            plt.plot(GDD_3, 'blue', label = "Tbase=12")
            plt.plot(GDD_4, 'black', label="Tbase=13")
            plt.plot(GDD_5,'yellow', label="Tbase=14")
            plt.plot(GDD_6, 'grey', label="Tbase=15")
            plt.xlim(0, 400)
            plt.xlabel("Days")
            plt.ylabel("GDD")
            plt.title('Different GDD in ' +line + ' Year - '+year, color = 'red')
            plt.legend()
            #plt.pause(2) 
            plt.grid()
            plt.draw()
            figs=None
            save_plot = 'plots/'+line+'_DifGDD.png'
            if figs is None:
              figs = [plt.figure(n) for n in plt.get_fignums()]
            for count,fig in enumerate(figs):
              fig.savefig(save_plot.format(count), format='png')
          
          else:
            print("No data available for Year - "+year)  
            break
     
             
      except IOError as err:
        print("error", err)

my_file = Dif_GDD(sys.argv[1],sys.argv[2], 'r') 

       
        
