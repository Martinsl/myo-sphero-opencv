# myo-sphero-opencv
Using <br />
https://github.com/orbotix/sphero.js <br />
https://github.com/dzhu/myo-raw

To connect the Sphero to linux:

sudo usermod -aG dialout $USER <br />
hcitool scan <br />
hcitool dev

sudo rfcomm bind hci0 68:86:E7:05:F4:47 <br />
sudo chmod 666 /dev/rfcomm0

To change the python version:

sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1 <br />
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.4 10 <br />
sudo update-alternatives --config python

To install nodejs on raspberry py:

Download version 10.x from http://node-arm.herokuapp.com/
sudo dpkg -i node_0.10.*
