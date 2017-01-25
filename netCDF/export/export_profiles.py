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
