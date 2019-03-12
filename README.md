# DopplerDemo
Python code to visually demonstrate the Doppler effect


The code requires Python 2.7, tkinter, matplotlib, and numpy.

You can also download a .zip file containing a .exe for windows machines from here: https://www.dropbox.com/s/q0a7f1611jhw4y0/DopplerDemo.zip
Just unzip it, open the directory, and double click DopplerDemo.exe. As long as your antivirus doesn't freak out, it should launch the program.


The user defines the source velocity, the observer velocity, the wave speed, and the starting locations of both the source and observer. The source sends out circles to simulate wave peaks as it moves, and the wave form is shown in the upper left-hand corner of the screen. The circles passing the observer are counted up and used to create the wave form as observed by the observer, which is displayed in the upper right-hand corner. 

Everything is calculated in SI units, with time steps of 0.005 seconds, all the positions in meters from the origin (left side of the screen, just more than halfway down), and the speeds and velocities in meters per second... but most computers will take much longer than 0.005 s to calculate each time step... So the units wouldn't make much sense. I decided to leave off the units on the prompt and advise users to treat them as relative values (this one is twice as large as that one, for example). 

The source wave, which is presented in the upper left-hand corner is a sine wave with a frequency of one cycle every 2 time steps (which, if we use units, would correspond to 100 Hz).

The observed wave, which is displayed in the upper right-hand corner during the simulation, is determined by counting the number of rings which will pass the observer in the next 5 turns, divided by 5, which is why the timing isn't perfect and it wobbles a bit in some situations. This part isn't perfect, but remember, this is for demonstrations, not for science.

Please feel free to email me with questions: imasillypirate@gmail.com
