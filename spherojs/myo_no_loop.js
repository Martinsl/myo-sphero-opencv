"use strict";

// connects to the myo script, make sure the path is correct
var spawn = require('child_process').spawn,
    myo = spawn('python3',['-u', './myo-raw/myo.py']);

// make sure the spherojs lib path is correct, you can use just spherojs
// if it was installed with npm
var sphero = require("./spherojs"),
    orb = sphero("/dev/rfcomm0");

orb.connect(function() {
  // heading will determine the sphero direction
  var heading = 0;

  myo.stdout.on('data', function (data) {
    var pose =  data.toString().substring(0,4),
        // uses heading to stop without changing direction
        stop = orb.roll.bind(orb, 0, heading),
        // binds a velocity to the roll command
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


function calculateDegree(heading, change) { // Keeps angle between 0-359
  var newDegree = heading+change;

  if (newDegree >= 360) {
    newDegree -= 360;
  }
  return newDegree;
}