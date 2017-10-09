import numpy as np
import scipy.interpolate as interpolate
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


def yo(i):
    return i


#--------griddata linear interpolation for missing data in coastlines----------------------------------
def InterpolateWeather(DATA, LON, LAT, X0, Y0, DECRESE=False):
    OUTPUT =[]
    for idx, interval in enumerate(DATA):
        #print(idx, interval)
        data = interval
        array = data
        xx, yy = np.meshgrid(LON,LAT)
        #get only the valid values
        x1 = xx[~array.mask]
        y1 = yy[~array.mask]
        newarr = array[~array.mask]
        #griddata interpolation
        GD1 = interpolate.griddata((x1, y1), newarr.ravel(), (xx, yy), method='nearest')
        #the final grid
        nmask = np.ma.masked_invalid(GD1)
        #reinterpolate for missing values at given coordinates [my spot coordinates]
        #the same way as above
        points = np.array( (xx.flatten(), yy.flatten()) ).T
        values = nmask.flatten()
        Z0 = interpolate.griddata( points, values, (X0,Y0), method='nearest')
        #decrease values by 25%
        if DECRESE == True:
            Z0 = [x-(x*0.25) for x in Z0]
        #append to OUTPUT as a list (not np array)
        OUTPUT.append(Z0)
        #print(Z0) #the waves/data for those points
    #transpose columns to rows for an array per spot
    OUTPUT = [list(i) for i in zip(*OUTPUT)]
    # print(OUTPUT)
    return OUTPUT

