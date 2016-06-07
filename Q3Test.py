import numpy as np
import math
import csv
import matplotlib as plt


with open("/Users/air/Desktop/montreal.csv") as files:
    
    #val = list(csv.reader(files))[1:3]
    val = list(csv.DictReader(files))
    
    #Max_Temp = list(zip(*val))[3]
    #Min_Temp = list(zip(*val))[4]
    #print(type(Max_Temp))
    #print(type(Min_Temp))
    for row in val:
        GDD = ((float(row['Min Temp']) + float(row['Max Temp']))/2)-10
        print(row['Min Temp'], ' ' , row['Max Temp'], ' ', str(round(GDD, 2)))
