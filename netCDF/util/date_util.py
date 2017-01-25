from netCDF4 import Dataset
from netCDF4 import num2date


# Reading time data from netCDF file:
nc_file = './example.nc'
fh = Dataset(nc_file, mode='r')
times = fh.variables['time'][:]
calendar = fh.variables['time'].calendar
tunits = fh.variables['time'].units
fh.close()

# Converting from int to date
for i, t in enumerate(times):
    print t
    dt = num2date(t, units=tunits, calendar=calendar)
    print dt
