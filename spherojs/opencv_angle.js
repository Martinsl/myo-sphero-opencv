var spawn = require('child_process').spawn,
    myo = spawn('python',['-u', '../opencv/spheroAngle.py']);

var sphero = require("./spherojs"),
    orb = sphero("/dev/rfcomm0");

orb.connect(function() {
  var heading = 0;

  orb.color("white");

  myo.stdout.on('data', function (data) {
    var angle =  data.toString().substring(0,3),
        stop = orb.roll.bind(orb, 0, heading),
        roll = orb.roll.bind(orb, 60);

    if (angle == "ST") {
      stop();
    } else {
      heading = angle
      roll(heading);
    }

    console.log("<<< " + angle + " <<<\n");
  });
  
  myo.stderr.on('data', function (data) {
    console.log('stderr: ' + data);
  });
});