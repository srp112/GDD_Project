import pandas as pd
import numpy as np
import matplotlib as plt
import csv

with open('/Users/air/Desktop/saskatoon.csv', 'r') as f:
    # = list(csv.DictReader(f))
    with open('/Users/air/Desktop/saskatoonGDD.csv', 'w') as newfile:
        writer = csv.writer(newfile)
        for row in csv.reader(f):
            if row[0] == "Year":
                writer.writerow(row+["GDD"])
            else:
                GDD = ((float(row[3]) + float(row[4])) / 2) - 10
                if GDD <= 0:
                    writer.writerow(row+[str(0)])
                else:
                    writer.writerow(row+[str(GDD)]) 
