import numpy as np
import matplotlib.pyplot as plt

def max_min_temp(y, z, city):
    fig = plt.figure()
    x = np.linspace(0, 365, 365)
    plt.subplot(2,3,1)
    plt.plot(x, y, 'g', label="$max$")
    plt.plot(x, z, 'r', label="$min$")
    plt.legend()

    plt.title("min/max daily temperatures" + city, color='green', fontsize='20')
    plt.xlabel("days", fontsize='15')
    plt.legend(loc=1)
    plt.ylabel("temperatures", fontsize='15')
    plt.legend(loc=2)

    plt.show()

max_min_temp(y, z, city)





