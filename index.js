// Main starting point of the application
const express = require('express');
const http = require('http');
const bodyParser = require('body-parser');
const morgan = require('morgan');
const app = express();
const router = require('./router')
const mongoose = require('mongoose');
const axios = require('axios');
const CronJob = require('cron').CronJob;

// DB Setup
mongoose.connect('mongodb://localhost:27017/forecast');



// App Setup
app.use(morgan('combined'));
app.use(bodyParser.json({type: '*/*'}));
router(app)

// Server Setup
const port = process.env.PORT || 3090;
const server = http.createServer(app);
server.listen(port);

console.log('SERVER LISTENING ON ' + port)

// Cron Job
/*
* Runs every weekday (Monday throughSunday)
* at 4:30:00 PM. */
const job = new CronJob({
  cronTime: '00 45 16 * * 1-7',
  onTick: function() {
	  
	  const util = require("util");
	  const spawn = require("child_process").spawn;
	  const process = spawn('python',["./wave_watch/bulk_update.py"]);
	  console.log("About that Time!")
	  
	  process.stdout.on('data',function(chunk){
	      var textChunk = chunk.toString('utf8');// buffer to string
	      console.log(textChunk);
	  });
	  
  },
  start: false
});

job.start();

