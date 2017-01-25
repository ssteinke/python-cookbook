# Convert integer times from netCDF to datetime

NetCDF files often use integers to store dates and timestamps. The corresponding unit indicates how to convert the integer to timestamps, e.g. 'seconds since 1970-01-01 00:00:00 UTC'. Example time used in netCDF files:

```
int time(time=174);
  :axis = "T";
  :calendar = "gregorian";
  :units = "seconds since 1970-01-01 00:00:00 UTC";
```

[date_util.py](./date_util.py) shows an example how to read times and convert them using netCDF4.num2date.

Example outputs:
```
1473930000
2016-09-15 09:00:00
1476565200
2016-10-15 21:00:00
1479200400
2016-11-15 09:00:00
1481835600
2016-12-15 21:00:00
```

For more infos see: http://unidata.github.io/netcdf4-python/#netCDF4.num2date
