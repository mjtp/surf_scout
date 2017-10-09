# Import Pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from pprint import pprint
from waves import InterpolateWeather
import datetime
import netCDF4


# NOAA Wave-Watch-3
mydate = datetime.datetime.now().strftime ("%Y%m%d")
url = 'http://nomads.ncep.noaa.gov:9090/dods/wave/nww3/nww3'+mydate+'/nww3'+mydate+'_00z'
file = netCDF4.Dataset(url)
LAT  = file.variables['lat'][:]
LON  = file.variables['lon'][:]
MINIMUM = file.variables['time'].minimum
MAXIMUM = file.variables['time'].maximum
SIGWAVEHEIGHT = file.variables['htsgwsfc'][:,:,:]
WAVEDIRECTION = file.variables['dirpwsfc'][:,:,:]
WAVEMEANPERIOD = file.variables['perpwsfc'][:,:,:]
WINDDIRECTION = file.variables['wdirsfc'][:,:,:]# from which blowing
WINDSPEED = file.variables['windsfc'][:,:,:]
file.close()

# Mongo Client
client = MongoClient('localhost', 27017)

# Database
db = client['forecast']

# Collection and Cursor
collection = db.forecast.find({})

# Store in List (so it is not destroyed after first operation)
forecast = list(collection)

# Get all my Lats and Lons from Mongo
X0 = [i['latitude'] for i in forecast]
Y0 = [i['longitude'] for i in forecast]
ID = [i['_id'] for i in forecast]

# Interpolate for forecast spots
wave_height = InterpolateWeather(SIGWAVEHEIGHT, LON, LAT, X0, Y0, DECRESE=True)
wave_direction = InterpolateWeather(WAVEDIRECTION, LON, LAT, X0, Y0)
wave_period = InterpolateWeather(WAVEMEANPERIOD, LON, LAT, X0, Y0)
wind_direction = InterpolateWeather(WINDDIRECTION, LON, LAT, X0, Y0)
wind_speed = InterpolateWeather(WINDSPEED, LON, LAT, X0, Y0)

# Initialize bulk Operation
bulk = db.forecast.initialize_ordered_bulk_op()

# Limit counter (Bulk limit is 1000, we'll do 500 at a time)
counter = 0

# Bulk update with the interpolated data
for id in ID:
    # Index 
    idx = ID.index(id)
    # Wave height
    wave_array = wave_height[idx]
    # Wave data as strings (Mongo is having trouble with large decimals)
    waves_data = map(str, wave_array)
    # Average Wave Height
    waves_average = float(sum(wave_array) / float(len(wave_array)))
    # Max Wave Height
    waves_max = float(max(wave_array))
    
    waves_dir = map(str, wave_direction[idx])
    
    waves_period = map(str, wave_period[idx])
    
    wind_dir = map(str, wind_direction[idx])
    
    wind_speed = map(str, wind_speed[idx])
    # Find and update
    bulk.find({ '_id': id }).update({ '$set': { 'waveheight': waves_data, 
                                                'mindate': MINIMUM, 
                                                'maxdate': MAXIMUM, 
                                                'avgwave': waves_average, 
                                                'maxwave' : waves_max,
                                                'wavedirection': waves_dir,
                                                'waveperiod': waves_period,
                                                'winddirection': wind_dir,
                                                'windspeed': wind_speed         
                                            } })
    # Increase Counter
    counter += 1
    # If counter modulus 500 is 0 
    if (counter % 500 == 0):
        bulk.execute()
        bulk = db.forecast.initialize_ordered_bulk_op()

if (counter % 500 != 0):
    bulk.execute()


