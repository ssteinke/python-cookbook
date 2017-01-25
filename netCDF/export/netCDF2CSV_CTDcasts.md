# Reading netCDF CTD data with python

The Red Sea Database (RSDB) at KAUST stores CTD data from different instruments (e.g. Sea-Bird or Idronaut CTDs) in netCDF
files. We store all CTD casts for a mission or cruise in one netCDF file.

While netCDF files are supported by several [software products](http://www.unidata.ucar.edu/software/netcdf/software.html),
here are some examples to extract data via python. I suggest to use [panoply](http://www.giss.nasa.gov/tools/panoply/) to have a first look at the netCDF content.

## Requirements
Tested with
* python 2.7
* pandas 0.18.0
* netCDF4 1.2.4

## Structure in CTD netCDF file
The CDL view from Panoply can be used to get an overview. Example:

```
netcdf file:SBE_CTD_August2016_downcast {
  dimensions:
    profile = 21;
    nzMax = 85699;
  variables:
    double Pressure(profile=21, nzMax=85699);
      :long_name = "";
      :units = "db";
      :coordinates = "time lat lon z";

    double Temperature(profile=21, nzMax=85699);
      :long_name = "Temperature";
      :units = "°C";
      :coordinates = "time lat lon z";

    double lat(profile=21);
      :long_name = "latitude";
      :standard_name = "latitude";
      :units = "degrees_north";
      :axis = "Y";
      :_FillValue = 0.0; // double
```

The nc file contains two dimensions:
* profile (all profiles from a mission)
* nzMax (measurements during a cast. The deepest profile in this file contains 85699 measurements)

There are some variables using only dimension *profile* (e.g. latitude). They describe where and when a profile was made and the file contains 21 values for such variables. All other measurements use both dimensions *profile* and *nzMax* (e.g. Temperature). Therefore the file contains a two dimensional array with **profile * nzMax** (21 * 85699) values for Temperature and other variables using both dimensions.


## Reading profile data from netCDF

First we read data with dimension profile to get information about where and when casts where collected:

```python
import netCDF4
import pandas as pd

# use netCDF4 to open file
filename='SBE_CTD_August2016_downcast'
nc = netCDF4.Dataset(filename+'.nc')

# read content for variables with dimension profile
profile_arr = nc.variables['profile'][:]
lat_arr = nc.variables['lat'][:]
lon_arr = nc.variables['lon'][:]
time_var = nc.variables['time']

# read variable time to convert values to a readable unit
time_arr = time_var[:]
dtime = netCDF4.num2date(time_var[:], time_var.units)
```

## Write profile data to CSV file
To write data to a CSV file, we can use pandas:

```python
# make a dictionary with columns:
d = {}
d['profile'] = profile_arr
d['lon'] = lon_arr
d['lat'] = lat_arr
d['time'] = dtime
# convert dictionary to pandas dataframe
df = pd.DataFrame(d)
# give pandas index column a name
df.index.name = 'Index'
# take a look at the first record
print df.head()

# Save data to CSV file
df.to_csv(filename+'.csv')
```

Here is how the data looks:
```
Index,lat,lon,profile,time
0,23.9945,36.9773333333,1,2016-01-20 12:12:20
1,23.9933333333,36.9768333333,2,2016-01-20 14:49:00
...
20,22.3051666667,39.1025,21,2016-01-19 11:34:10
```

## Read cast data from netCDF4 and write data to one CSV per cast

The next example shows how to read measurements and store data in files per cast:

```python
import netCDF4
import pandas as pd

filename='SBE_CTD_August2016_downcast'
nc = netCDF4.Dataset(filename+'.nc')

# read all dimensions and variables
nc_dims = [dim for dim in nc.dimensions]
nc_vars = [var for var in nc.variables]

# loop over all variables and store all with type float64 and two dimensions (profile and nzMax)
castVars = []
for var in nc_vars:
    if var not in nc_dims:
        if len(nc.variables[var].dimensions) == 2:
            if str(nc.variables[var].dtype) == 'float64':
                print 'var with 2 dimensions: ' + var + ' type: '+ str(nc.variables[var].dtype)
                castVars+=[var]

# extract profiles and loop over profiles..
profile_arr = nc.variables['profile'][:]
for i, profile in enumerate(profile_arr):
    # ..for every profile, read profile data for all variables
    d = {}
    for j, var in enumerate(castVars):
        d[var] = nc.variables[var][i,:]
    # convert to pandas dataframe
    df = pd.DataFrame(d)
    # give pandas index column a name
    df.index.name = 'Index'
    # drop all rows with empty data (shallow casts)
    df = df.dropna(how='all', subset=castVars)
    # store cast data in CSV file
    df.to_csv(filename+ '_cast_'+ str(i) +'.csv')
```

Here is how the data looks:
```
Index,Chlorophyll-Fluorescence,Conductivity,NTU,Oxygen,PAR,Potential_Temperature,Pressure,Salinity,Temperature,flag,pH,sigma-E00,z
0,0.0528,5.916297,0.2092,3.8827,164.04,25.7799,8.174,38.8866,25.7817,0.0,8.95,26.0386,8.123
1,0.0528,5.916343,0.2092,3.8788,163.58,25.7779,8.189,38.8887,25.7797,0.0,8.95,26.0408,8.138
...
```
