var spawn = require('child_process').spawn,
    myo = spawn('python',['-u', './my_spheroStream.py']);

var sphero = require("./spherojs"),
    orb = sphero("/dev/rfcomm0");

orb.connect(function() {
  var heading = 0;

  orb.color("white");

  myo.stdout.on('data', function (data) {
    var pose =  data.toString().substring(0,4),
        stop = orb.roll.bind(orb, 0, heading),
        roll = orb.roll.bind(orb, 40);

    if (pose === "FORW") {
      heading = 0;
      roll(heading);
    } else if (pose == "STOP") {
      stop();
    } else if (pose == "LEFT") { 
      heading = 270;
      roll(heading);
    } else if (pose == "RIGH") {
      heading = 90;
      roll(heading);
    } else if (pose == "BACK") {
      heading = 180;
      roll(heading);
    }
    
    console.log("<<< " + pose + " <<<\n");
  });
  
  myo.stderr.on('data', function (data) {
    console.log('stderr: ' + data);
  });
});