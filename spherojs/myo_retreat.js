"use strict";

// connects to the myo script, make sure the path is correct
var spawn = require('child_process').spawn,
    myo = spawn('python3',['-u', './myo-raw/myo.py']);

// make sure the spherojs lib path is correct, you can use just spherojs
// if it was installed with npm
var sphero = require("./spherojs"),
    orb = sphero("/dev/rfcomm0");

orb.connect(function() {
  // the heading changes the sphero direction
  // 0 is forward, 180 is back, 270 is left and 90 right
  var heading = 0;
  
  // ask the sphero to give collision info,
  // which can be retrieved using orb.on("collision")
  orb.detectCollisions();

  // reads the data coming from the myo script
  myo.stdout.on('data', function (data) {
    var pose =  data.toString().substring(0,4),
        // using heading to stop the sphero
        // without changing its direction
        stop = orb.roll.bind(orb, 0, heading),

        // binds a velocity to the roll command
        roll = orb.roll.bind(orb, 100);

    if (pose === "OPEN") { // goes forward
      roll(heading);
    } else if (pose == "FIST") {
      stop();
    } else if (pose == "WAVI") { // goes left
      heading = calculateDegree(heading, 310);
      roll(heading);
    } else if (pose == "WAVO") { // goes right
      heading = calculateDegree(heading, 50);
      roll(heading);
    } else if (pose == "PINK") { // goes back
      heading = calculateDegree(heading, 180);
      roll(heading);
    }

    console.log("<<< " + pose + " <<<\n");
  });
  
  myo.stderr.on('data', function (data) {
    console.log('stderr: ' + data);
  });

  orb.on("collision", function(data) {
    console.log("collision detected");
    console.log("  data:", data);

    orb.color("red");

    setTimeout(function() {
      orb.color("000000");
    }, 1000);
  });
});

function calculateDegree(heading, change) {
  var newDegree = 0;

  newDegree = heading+change;

  if (newDegree >= 360) {
    newDegree -= 360;
  }
  return newDegree;
}