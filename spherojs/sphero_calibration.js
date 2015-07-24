var sphero = require("sphero");
var orb = sphero("/dev/rfcomm0");

orb.connect(function() {
  orb.color("000000");

  /** Start Manual Calibration */
  
  setTimeout(function() {
    console.log("::START CALIBRATION::");
    orb.startCalibration();
  }, 2000);
  setTimeout(function() {
    console.log("::FINISH CALIBRATION::");
    orb.finishCalibration();
  }, 9000);
  setTimeout(function() {
    orb.disconnect(function() {
      console.log("Now disconnected from Sphero");
    });
    process.stdin.pause();
    process.exit();
  }, 10000);
});