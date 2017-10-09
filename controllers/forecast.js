const Forecast = require('../models/forecast');
var mongoose = require('mongoose');

// Find One
exports.findOne = function(req, res, next) {
	const id = req.headers.id;
	
	if (!id) {
		return res.status(422).send({ error: 'You must provide id'});
	}
	
	Forecast.findOne({_id: id}, function(err, Doc){
		if (err) { return next(err); }
		
		res.json({ Forecast: Doc });
		
	});
};


// Find Multiple
exports.find = function(req, res, next) {
	const min = req.headers.min;
	const max = req.headers.max;
	const cursor = req.headers.cursor;
	
	// Average Wave Range 
	if (min && max && cursor === 'avg') {		
		Forecast.find({'avgwave': { '$gte': min, '$lte': max}}, function(err, Doc){
			if (err) { return next(err); }
			res.json({ Forecasts: Doc });
		}); 
	}
	// Max Wave Range
	if (min && max && cursor === 'max') {		
		Forecast.find({'maxwave': { '$gte': min, '$lte': max}}, function(err, Doc){
			if (err) { console.log(err); return next(err); }
			res.json({ Forecasts: Doc });
		}); 
	}
	// All Documents
	if (!min && !max && !cursor) {		
		Forecast.find({}, function(err, Doc){
			if (err) { return next(err); }
			
			res.json({ Forecasts: Doc });
		})
	}
	
	
}

// Add a Spot to Forecasts
exports.addOne = function(req, res, next) {
	const spot = req.body.spot;
	const country = req.body.country;
	const state = req.body.state;
	const lon = req.body.lon;
	const lat = req.body.lat;
	
	if (!spot || !country || !state || !lon || !lat){
		return res.status(422).send({ error: 'All 3 params required'});
	}
	
	// See if a Spot exist
	Forecast.findOne({spot: spot, country: country, state: state }, function(err, existingForecast){
		if (err) { return next(err); }
	   
		// If a Spot exist, return an error
		if (existingForecast) {
			return res.status(422).send({error: 'Forecast already exists'});
		}	
		
		// If a forecast does not exist create and save
		const forecast = new Forecast({
			spot: spot,
			country: country,
			state: state,
			latitude: lat,
			longitude: lon,
			mindate: 'a date',
			maxdate: 'another date...',
			maxwave: 0.1212,
			avgwave: 0.2121
		});
		
		forecast.save(function(err) {
			if(err) { return next(err); }
			
			// Respond to request with the new doc
			res.json({ forecast });
			
		});		
		
	});
	
	
}





















