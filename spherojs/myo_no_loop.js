"use strict";

// connects to the myo script, make sure the path is correct
var spawn = require('child_process').spawn,
    myo = spawn('python3',['-u', './myo-raw/myo.py']);

// create sphero obj
var sphero = require("./spherojs"),
    orb = sphero("/dev/rfcomm0");

orb.connect(function() {
  var heading = 0;

  myo.stdout.on('data', function (data) {
    var pose =  data.toString().substring(0,4),
        stop = orb.roll.bind(orb, 0, heading),
        roll = orb.roll.bind(orb, 60);

    if (pose === "OPEN") {
      roll(heading);
    } else if (pose == "FIST") {
      stop();
    } else if (pose == "WAVI") {
      heading = calculateDegree(heading, 310);
      roll(heading);
    } else if (pose == "WAVO") {
      heading = calculateDegree(heading, 50);
      roll(heading);
    }
    
    console.log("<<< " + pose + " <<<\n");
  });
  
  myo.stderr.on('data', function (data) {
    console.log('stderr: ' + data);
  });
});

function calculateDegree(heading, change) {
  var newDegree = heading+change;

  if (newDegree >= 360) {
    newDegree -= 360;
  }
  return newDegree;
}