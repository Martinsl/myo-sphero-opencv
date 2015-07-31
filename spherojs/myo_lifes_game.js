"use strict";

// connects to the myo script, make sure the path is correct
var spawn = require('child_process').spawn,
    myo = spawn('python3',['-u', './myo-raw/myo.py']);

// make sure the spherojs lib path is correct, you can use just spherojs
// if you installed it with npm
var sphero = require("./spherojs"),
    orb = sphero("/dev/rfcomm0");

orb.connect(function() {
  // heading will determine the sphero direction
  var heading = 0,
      totalLifes = 5;
  
  // user can call script with a second argument to set the number of lifes
  if (totalLifes = process.argv[2]) {
    console.log(totalLifes)
  }
  var lifes = totalLifes,
      lifeColor = colorGradtoHex(totalLifes, lifes);

  orb.color(lifeColor);
  orb.detectCollisions();

  myo.stdout.on('data', function (data) {
    var pose =  data.toString().substring(0,4),
        // uses heading to stop without changing direction
        stop = orb.roll.bind(orb, 0, heading),
        // binds a velocity to the roll command
        roll = orb.roll.bind(orb, 80);

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
    } else if (pose == "PINK") {
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

    lifes--;
    if (lifes < 0) {
      process.stdin.pause();
      process.exit();
    }
    // set sphero to the new color
    lifeColor = colorGradtoHex(totalLifes, lifes);
    setTimeout(function() {
      orb.color(lifeColor);
    }, 100);
  });
});

// keeps angle between 0-359
function calculateDegree(heading, change) {
  var newDegree = 0;

    newDegree = heading+change;


  if (newDegree >= 360) {
    newDegree -= 360;
  }
  return newDegree;
}

function colorGradtoHex(totalLifes, lifes) {
  var red = 0,
      green = 0,
      blue = 0,
      hex = 0;

  red = (5 - lifes) * (255 / totalLifes);
  green = lifes * (255 / totalLifes);
  hex = red * 65536 + green * 256;
  return hex;
}