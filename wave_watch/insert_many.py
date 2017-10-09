# Import Pymongo
from pymongo import MongoClient

# Client
client = MongoClient('localhost', 27017)

# Database
db = client['forecast']

# Collection
forecast = db.forecast

forecasts = [
		{
		"spot":"brisbane",
        "country": "australia",
        "state": " ",
		"latitude": -28.011730,
		"longitude": 153.436424,
        "avgwave": 3, 
        'maxwave' : 3,
		"waveheight": [1, 2, 3],
		"wavedirection": [1, 2],
		"waveperiod": [1, 2],
		"winddirection": [1, 2],
		"windspeed": [1, 2],
        "mindate": "1/1/1",
        "maxdate": "1/7/8"
        
	   },
		{
		"spot":"jupiter inlet",
        "country": "united states",
        "state": "florida",
		"latitude": 26.954413,
		"longitude": -79.929465,
        "avgwave": 3,
        'maxwave' : 3,
		"waveheight": [1, 2, 3],
		"wavedirection": [1, 2],
		"waveperiod": [1, 2],
		"winddirection": [1, 2],
		"windspeed": [1, 2],
        "mindate": "1/1/1",
        "maxdate": "1/7/8"
	   }
   ]
         

forecasts_ids = forecast.insert_many(forecasts).inserted_ids

print(forecasts_ids)

