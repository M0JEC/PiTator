# PiTator
Python based code for controlling an old CCTV Rotator with a Raspberry Pi.

This project started when I managed to get hold of a cheap ex CCTV Rotator, As it had 'elevation' as well as Azumith I thought it could be converted for working Satelittes. 

This code currently uses 'dead reckoning' to get the position of the rotaor but plan is to use the PiHat (AstroPi) to feedback the heading and tilt of the rotator.

The majority of the code was written by me but with some input from my friend Luke who is a programmer for his work.

The code takes in x (az) and y (ele) data and then controls relays attached to tthe GPIO of the Pi to position the rotator at the correct position.

I also had to think about a few hardware issues to stop accidental left/right and/or up/down dual activation. So that if the Pi outputs 'float' on boot the rotator is not being asked to go in two opposite directions at the same time.

As of 16-11-2015 I have the basic setup now fully working (been in development for quite a long time) there will be some more updates as I add feedback etc to the system.
