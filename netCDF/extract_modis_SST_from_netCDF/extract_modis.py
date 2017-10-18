from netCDF4 import Dataset
import numpy as np
import time
import datetime
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import collections


def geo_idx(dd, dd_array):
    """
     search for nearest decimal degree in an array of decimal degrees and return the index.
     np.argmin returns the indices of minium value along an axis.
     so subtract dd from all values in dd_array, take absolute value and find index of minium.
    """
    geo_idx = (np.abs(dd_array - dd)).argmin()
    return geo_idx


def readMonthlyModisData(filename, in_lat, in_lon):
    """
     Read monthly sea surface temperature from single netCDF file, extract data
     from grid for given position and all time slides, return a DataFrame.
    """
    fh = Dataset(filename, mode='r')
    times = fh.variables['time'][:]
    lats = fh.variables['lat'][:]
    lons = fh.variables['lon'][:]

    lat_idx = geo_idx(in_lat, lats)
    lon_idx = geo_idx(in_lon, lons)
    # SST (time, latitude, longitude)
    sstSubset = fh.variables['sst'][:, lat_idx, lon_idx]
    fh.close()

    columns = ['year', 'Jan', 'Feb',
              'Mar', 'Apr', 'May (mean)', 'Jun (mean)', 'Jul (mean)',
               'Aug (mean)', 'Sep (mean)', 'Oct (mean)', 'Nov (mean)',
               'Dec (mean)',
              ]
    data = pd.DataFrame(columns=columns)

    actYear = -1
    actMonth = -1
    yearData = []
    meanData = []
    for i, t in enumerate(times):
        #print t
        dt = datetime.datetime.fromtimestamp(t)
        year = dt.strftime('%Y')
        month = dt.strftime('%m')
        #print 'Working on: '+month+'.'+year
        if actYear < 0:
            actYear = int(year)
        elif actYear != int(year):
            #print 'MeanData.length:'+str(len(meanData))
            #print meanData
            df = pd.DataFrame([[actYear, meanData[0], meanData[1], meanData[2],
                                meanData[3], meanData[4], meanData[5],
                                meanData[6], meanData[7], meanData[8],
                                meanData[9], meanData[10], meanData[11], ]],
                                columns=columns)
            data = data.append(df, ignore_index=True)
            yearData = []
            meanData = []
            actYear = int(year)
        actMonth = int(month)
        sstSlice = sstSubset[i]
        tmp = []
        while len(yearData) < actMonth - 1:
            yearData.append([np.nan])
            meanData.append(np.nan)
        tmp = [sstSlice]
        if len(tmp) == 0:
            yearData.append(np.nan)
            meanData.append(np.nan)
        else:
            yearData.append([tmp])
            meanData.append(np.mean(tmp))

        if i == len(times)-1:
            #print 'write last year'
            while len(yearData) < 12:
                #print 'fill yearData'
                yearData.append([np.nan])
                meanData.append(np.nan)
            df = pd.DataFrame([[actYear, meanData[0], meanData[1], meanData[2],
                                meanData[3], meanData[4], meanData[5],
                                meanData[6], meanData[7], meanData[8],
                                meanData[9], meanData[10], meanData[11],]],
                                columns=columns)
            data = data.append(df, ignore_index=True)
    return data, lats[lat_idx], lons[lon_idx]


# Extract data for different sites
sst_file = '/Users/steinks/data/python/sst/339_RED_SEA_MO_SST_4km_lon33.5-43.5_lat13-28.nc'

# in_lat = 22.370033
# in_lon = 39.060164
in_lat = 22.393
in_lon = 39.061
data, lat, lon = readMonthlyModisData(sst_file, in_lat, in_lon)
data.to_csv('KAEC_lat'+str(lat)+'lon'+str(lon)+'.csv')

in_lat = 22.2227567
in_lon = 38.964500
data, lat, lon = readMonthlyModisData(sst_file, in_lat, in_lon)
data.to_csv('Al_Fahal_S_lat'+str(lat)+'lon'+str(lon)+'.csv')

# in_lat = 22.298300
# in_lon = 39.046317
in_lat = 22.308
in_lon = 39.032
data, lat, lon = readMonthlyModisData(sst_file, in_lat, in_lon)
data.to_csv('Abu_Shoosha_lat'+str(lat)+'lon'+str(lon)+'.csv')

in_lat = 22.138715
in_lon = 38.967578
data, lat, lon = readMonthlyModisData(sst_file, in_lat, in_lon)
data.to_csv('Abu_Shootaf_lat'+str(lat)+'lon'+str(lon)+'.csv')

in_lat = 22.230950
in_lon = 39.029060
data, lat, lon = readMonthlyModisData(sst_file, in_lat, in_lon)
data.to_csv('Fsar_lat'+str(lat)+'lon'+str(lon)+'.csv')

in_lat = 27.273333
in_lon = 35.642283
data, lat, lon = readMonthlyModisData(sst_file, in_lat, in_lon)
data.to_csv('DR7_lat'+str(lat)+'lon'+str(lon)+'.csv')

in_lat = 27.921550
in_lon = 35.187822
data, lat, lon = readMonthlyModisData(sst_file, in_lat, in_lon)
data.to_csv('DR8_lat'+str(lat)+'lon'+str(lon)+'.csv')

# in_lat = 27.681220
# in_lon = 35.442150
in_lat = 27.717
in_lon = 35.435
data, lat, lon = readMonthlyModisData(sst_file, in_lat, in_lon)
data.to_csv('DR12_lat'+str(lat)+'lon'+str(lon)+'.csv')
