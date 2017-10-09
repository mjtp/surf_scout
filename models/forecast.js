const mongoose = require('mongoose');
const Schema = mongoose.Schema;

// Define our model
const forecastSchema = new Schema({
	   spot: {type: String, lowercase: true },
	   country: {type: String, lowercase: true },
	   state: {type: String, lowercase: true },
		latitude: Number,
		longitude: Number,
	   avgwave: Number,
	   maxwave: Number,
		waveheight: Array,
		wavedirection: Array,
		waveperiod: Array,
		winddirection: Array,
		windspeed: Array,
      mindate: String,
      maxdate: String
	   
});

// set to singular so it matches pymongos (mongoose pluralizes)
forecastSchema.set('collection', 'forecast');

// Create the model class
const ModelClass = mongoose.model('forecast', forecastSchema);


// Export the model
module.exports = ModelClass;

