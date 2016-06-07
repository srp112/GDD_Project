import sys, argparse, csv
import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt


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
     with open(file_name, "rU") as files:
      val = list(csv.reader(files))[26:]
      #print(val)
      max_temp = list(zip(*val))[5]
      min_temp = list(zip(*val))[7]
      fig = plt.figure()
      plt.plot(max_temp, 'r', label="Max")
      plt.plot(min_temp, 'g', label="Min")
      plt.title("min/max daily temperatures")
      plt.ylabel("Temp.")
      plt.xlabel("Day")
      
      plt.legend()
      plt.show()
      print(max_temp,min_temp)
     
    except IOError as err:
       print("error", err)
    






