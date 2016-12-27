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
    
