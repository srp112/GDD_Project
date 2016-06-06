import numpy as np
import math

data = np.loadtxt(open("/Users/air/Desktop/temperatures.csv"),delimiter=",",skiprows=0)
data_sum = data.sum(axis = 1)
base = 10

def gdd(DataSet, base):
    avg = DataSet.sum(axis = 1) / 2
    gdd = avg - base
    gdd = gdd.clip(min=0)

    return gdd

DataSet = data
gdd(DataSet, 10)

np.savetxt('/Users/air/Desktop/GDD_Calculation.csv', gdd(DataSet, 10), delimiter = ',')
