import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import math
import matplotlib.mlab as mlab
from scipy.stats import norm
import csv

#import csv
yourList = []

csv_file_path = "AlbatrossNew.csv"
with open(csv_file_path) as csvfile:
    f_csv = csv.reader(csvfile)
    index = 0
    for row in f_csv:
        if index>0:
            dis_cache = float(row[0])
            yourList.append(dis_cache)
        index = index + 1


#Guassian distribution fit

x = np.array(yourList)
mu = np.mean(x)
sigma = np.std(x)
num_bins = 300 # the num of cube
n,bins,patches = plt.hist(x, num_bins, density=1, alpha=0.75)
y= norm.pdf(bins, mu, sigma)

plt.grid(True)
plt.plot(bins,y,"r--")
plt.xlabel("value")
plt.ylabel("Probability")
plt.title(str(csv_file_path)+ " Histogram : $\mu$=" + str(round(mu, 2)) + " $\sigma=$" +str(round(sigma, 2)))

plt.show()
