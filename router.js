const Forecaster = require('./controllers/forecast')


module.exports = function(app) {
	// GET
	app.get('/forecast', Forecaster.findOne);
	app.get('/forecasts', Forecaster.find);
	
	// POST
	app.post('/forecast', Forecaster.addOne);
	
	
}