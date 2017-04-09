# autoMeteorRx
Program to automate the recording of Meteor and other weather satellite signals
autoMeteorRx.py
===============

This program establishes a UDP connection to the predict program and queries it to get the status of Meteor M-N2. When the satellite appears over 
the horizon the program executes the gnuradio soft symbol decoder. When the satellite pass completes (at LOS) the program kills the gnuradio 
program and continues to monitor for next AOS of Meteor M-N2.

To-Do
-----
- probably some other stuff that I haven't though of at the moment!!

Dependencies
------------
Depends on 'predict' for satellite tracking and psutil for killing a running process.

Installation
------------
Install predict via the Ubuntu Software Centre or from http://www.qsl.net/kd2bd/predict.html
Set up QTH etc in predict, if you install from the software centre it is useful to download the tar file from qsl.net as this has a docs directory 
in it which contains a useful pdf reference document.

Edit the tle file in ~homedir/.predict/predict.tle to have the Meteor M-N2 TLE's, i.e.
METEOR-M-2
1 40069U 14037A   15119.13829858  .00000026  00000-0  32820-4 0  9992
2 40069  98.7619 174.2145 0004879 312.5094  47.5671 14.20606131 41804

As I only use predict for Meteor I deleted all other satellites. You must also change the name of the satellite to "METEOR-M-2" to remove any spaces. 

Install psutil:
sudo apt-get install python-psutil

Copy autoMeteorRx.py to any suitable directory.

Edit autoMeteorRx.py and change variables as follows:
	- minrequiredel to the minimum pass elevation you want to record;
	- minrisingel to the elevation that you want to start recording;
	- minsettingel to the elevation that you want to stop recording;
	- cmd2 to the path and name of the gnuradio python program you use;
	- POSTCMD1, POSTCMD2 & POSTCMD3 to execute specific Linux commands after the gnuradio process has been killed (optional)
	
Make autoMeteorRx.py to be executable: chmod +x autoMeteorRx.py

Operation
---------
Start predict in a terminal window in server mode: predict -s
and minimise it and leave running

Start autoMeteorRx in a terminal window: python autoMeteorRx.py

You should see output like below, and this also shows what happens when gnuradio is called and then killed after the pass:

Next AOS/LOS: 1430759248
Last AOS: 1430759248  Sleep 60 seconds...
Current time: 1430758887
Next AOS/LOS: 1430759248
Last AOS: 1430759248  Sleep 60 seconds...
Current time: 1430758948
Next AOS/LOS: 1430759248
Last AOS: 1430759248  Sleep 60 seconds...
Current time: 1430759008
Next AOS/LOS: 1430759248
Last AOS: 1430759248  Sleep 60 seconds...
Current time: 1430759068
Next AOS/LOS: 1430759248
Last AOS: 1430759248  Sleep 60 seconds...
Current time: 1430759128
Next AOS/LOS: 1430759248
Last AOS: 1430759248  Sleep 60 seconds...
Current time: 1430759188
Next AOS/LOS: 1430759248
Last AOS: 1430759248  Sleep 60 seconds...
Current time: 1430759248
Next AOS/LOS: 1430759248
Last AOS: 1430759248
Reset nextaos
Call rx program
Pid= 6747
linux; GNU C++ version 4.8.2; Boost_105400; UHD_003.009.git-186-geb9cfef4

Error: failed to enable realtime scheduling.

(python:6748): Gdk-WARNING **: gdk_window_set_icon_list: icons too large
Using Volk machine: avx_64_mmx
gr-osmosdr v0.1.4-21-gbe9af0fe (0.1.5git) gnuradio 3.7.8git-132-g06a7a77e
built-in source types: file osmosdr fcd rtl rtl_tcp uhd hackrf rfspace 
Using HackRF One with firmware 2014.08.1 

(python:6748): Gtk-CRITICAL **: IA__gtk_widget_event: assertion 'WIDGET_REALIZED_FOR_EVENT (widget, event)' failed

(python:6748): Gtk-CRITICAL **: IA__gtk_widget_event: assertion 'WIDGET_REALIZED_FOR_EVENT (widget, event)' failed

(python:6748): Gtk-CRITICAL **: IA__gtk_widget_event: assertion 'WIDGET_REALIZED_FOR_EVENT (widget, event)' failed

(python:6748): Gtk-CRITICAL **: IA__gtk_widget_event: assertion 'WIDGET_REALIZED_FOR_EVENT (widget, event)' failed

(python:6748): Gtk-CRITICAL **: IA__gtk_widget_event: assertion 'WIDGET_REALIZED_FOR_EVENT (widget, event)' failed

(python:6748): Gtk-CRITICAL **: IA__gtk_widget_event: assertion 'WIDGET_REALIZED_FOR_EVENT (widget, event)' failed
Kill rx program
Process found. Terminating it.
Current time: 1430759695
Next AOS/LOS: 1430764959
Last AOS: 1430764959  Sleep 60 seconds...
Terminated
Current time: 1430759755
Next AOS/LOS: 1430764959
Last AOS: 1430764959  Sleep 60 seconds...


Copyright 2015,2016,2017 Simon Kennedy, G0FCU, g0fcu at g0fcu.com
