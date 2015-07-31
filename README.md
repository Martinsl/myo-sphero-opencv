# myo-sphero-opencv
Using <br />
https://github.com/orbotix/sphero.js <br />
https://github.com/dzhu/myo-raw

To connect the Sphero to linux:

sudo usermod -aG dialout $USER <br />
hcitool scan <br />
hcitool dev

sudo rfcomm bind hci0 68:86:E7:05:F4:47 <br />
sudo chmod 666 /dev/rfcomm0 <br />
To release the sphero: <br />
sudo rfcomm release hci0 <br />

To install nodejs on raspberry py:

Download version 10.x from http://node-arm.herokuapp.com/ <br />
Install with: sudo dpkg -i node_0.10.*

# Myo-raw
Train your poses with the classify_myo.py script, dont forget to train the rest position as well. <br />
Edit the file myo.py (~ line 107) according to the poses you trained. <br />
Copy the *.dat files to the directory with the sphero scripts.

# Spherojs
Make sure the sphero is connected, sometimes during calibration it loses connection and stays on the "calibration mode", be sure the backLed is off after calibrating the sphero. <br />
The example files were added to make it easier to understand the commands. <br />

# Opencv
Depending on the camera the light threshold may differ, you can use the get_hsv.py script to find the correct hsv values.<br />
Start with the whiteSearch.py file, to better understand the masks.
