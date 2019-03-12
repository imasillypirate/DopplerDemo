import numpy as np
import matplotlib.pyplot as plt
from tkinter import *

#Runs a simulation to demonstrate the doppler shift with user defined speed for the wave and the positions and velocities for the source and observer.
#Works in Python 2.7, for Python 3, there may be a difference in how tkinteris called.
#Written by Richard D Mellinger Jr : imasillypirate@gmail.com
#Last update: 03/04/2019

class circ: #circle object to be used as a wavefront graphically
	def __init__(self,x,y):
		self.r = 0 #radius of circle
		self.x = x
		self.y = y
		self.circ = plt.Circle((x, y), self.r,facecolor='none',edgecolor='k')
		
	def updateCirc(self,r):
		self.r = r
		self.circ = plt.Circle((self.x, self.y), self.r,facecolor='none',edgecolor='k')
		
		
def runSim(dt,vw,vs,psi,vo,poi):
	#Actually launches and runs the simulation. Times can be assumed to be in seconds, distances in meters, and speeds
	#  in m/s, however, the rate of movement will be dependent on the computer and, usually significantly slower.
	#  For example, if dt = 0.005, every time step will be 5/1000 of a second for the time within the simulation,
    #  but it is likely that the computer will take longer than 0.005 s to do the pertinent calculations and display
	#  the results for each step.
	#  One wavefront will be created every other time step. So,if dt = 0.005, the wave period at the source would be 0.01s, 
	#  and the frequency would be 100 Hz.
	#  The area displayed will have an x range of 0 to 5 and a y range of -2 to 4. The top 1.5, however, is mostly covered
	#  by plots for the frequencies.
	#Inputs:
	#    dt = length of time step (usually 0.005, because the value works nicely)
	#    vw = speed of wave
	#    vs = lenght 2 list giving the x then y components of the source velocity
	#   psi = lenght 2 list giving the initial x then y components of the source position
	#    vo = lenght 2 list giving the x then y components of the observer velocity
	#   poi = lenght 2 list giving the initial x then y components of the observer position
	#Output: NONE
	
	plt.ion()

	fig = plt.figure(figsize=(6,6))

	ax3 = fig.add_subplot(111) #main plot
	ax1 = fig.add_subplot(421) #subplot for source frequency
	ax2 = fig.add_subplot(422) #subplot for observed frequency
	
	xsz = [0,5] #Limits of plot in x direction (m)
	ysz = [-2,4] #Limits of plot in y direction (m)

	circs = [] #list to keep circle objects

	xsc = psi[0] #unpack initial positions
	ysc = psi[1]
	xoc = poi[0]
	yoc = poi[1]

	ax1.set_xlim([0,dt*4]) #Constrain size of source frequency plot to show 2 periods
	ax1.set_ylim([-1,1]) 
	ax1.set_title('Source')

	time = np.linspace(0,dt*4,100) #Generate waveform for source frequency subplot
	ysource = [np.sin(np.pi*(1/dt)*k) for k in time]
	ax1.plot(time,ysource)

	wcountKeep = []# A place to keep several previous counts when calculating the observed frequency (for average to smoth output)
	listenRange = 5.0 #The waves that will pass the observer in the next this many turns will be counted
	
	ct = 0 #counter for inside while loop
	
	while True: #Time todo the simulation
		#-------------Update positions
		xsc+=vs[0]*dt
		ysc+=vs[1]*dt
		xoc+=vo[0]*dt
		yoc+=vo[1]*dt
	
		ax3.cla()#clear axes for main plot and observer subplot
		ax2.cla()
		
		ax3.set_xlim([xsz[0],xsz[1]]) #Constrain size of main plot
		ax3.set_ylim([ysz[0],ysz[1]]) 
		ax2.set_xlim([0,dt*4]) #Constrain size of observer subplot
		ax2.set_ylim([-1,1]) 
		ax2.set_title('Observer')
	
		#-------------Plot positions of observer and source
		ax3.plot(xsc,ysc,'ro') #source is red
		ax3.plot(xoc,yoc,'bo') #observer is blue
	
		if ct%2 == 0:#Create 1 new wave every other time step
			circs.append(circ(xsc,ysc))
	
		if len(circs) > 100: #make sure there are never more than 100 circles (delete oldest)
			del circs[0]
			
		wcount = 0#counter for number of wavefronts to pass in the next (listenRange) turns.
		for cir in circs: #for each circle object
			cir.updateCirc(cir.r+dt*vw) #increase the radius by vw*dt
			ax3.add_artist(cir.circ) #display the updated circle
		
			#-----------Determine the observed frequency by counting the number of waves that will pass in the next some amnt of turns
			xtemp = cir.x #write down some stuff about the circle
			ytemp = cir.y 
			rtemp = cir.r 
			centDisp = [1.0*xtemp-1.0*xoc,1.0*ytemp-1.0*yoc] #displacement from observer to circle center
			centDist = np.sqrt((centDisp[0]**2)+(centDisp[1]**2)) # magnitude of centDisp (distance from source to wave origin)
			vorptw = -1*((vo[0]*centDisp[0] + vo[1]*centDisp[1])/centDist) #|v| of observer wrt wave (away from wave og). vo projected into radial direction. Minus sign to make away positive.
			if abs(centDist-rtemp) < listenRange*dt*(vw-vorptw) : # If (the distance between the closest wave edge and the observer) < (the distance the wave will cover in the next listenRange turns in the reference frame of the source)
				wcount+=1 #count this one.
	
		wcountKeep.append(wcount) #keep the value
		y = [np.sin(((np.average(wcountKeep)/listenRange)*(np.pi/dt)*k)) for k in time]#generate the observedwave form (notice average, that's why it lags a bit, but smooths it out).
		#Previous line: y = sin ( (count/number of dt watched)*(2 pi/ period)* t). Notice the period is 2 dt, so  2pi/period = pi/dt
		ax2.plot(time,y)
		
		if len(wcountKeep)>1: #only want to keep a couple count values
			del wcountKeep[0]
	
		fig.canvas.draw()
		fig.canvas.flush_events()
		ct+=1 #update loop count

def getSimVals():
	#extract values from GUI and launch the simulation.

	dt = 0.005 #time steps of 0.005 work pretty well

	vWave = float(waveSpeedF.get()) #wave speed
	vSource = [float(vsxF.get()),float(vsyF.get())] #Source velocity [x,y]
	pSource = [float(psxF.get()),float(psyF.get())] #Source position [x,y]
	vObserver = [float(voxF.get()),float(voyF.get())]#Observer velocity [x,y]
	pObserver = [float(poxF.get()),float(poyF.get())]#Observer position [x,y]
	
	runSim(dt,vWave,vSource,pSource,vObserver,pObserver)
		
def quit1():
	#Exit program nicely
	top.destroy()
	raise SystemExit(0)
		
def mkMain():
	#Create GUI for input

	global waveSpeedF,vsxF,vsyF,psxF,psyF,voxF,voyF,poxF,poyF

	Quit1 = Button(top,text = " Quit ",activeforeground='red',activebackground='gray', command = quit1).grid(row = 9, column = 2) #quit button. Executes quit1()
	run = Button(top,text = " Run ",activeforeground='red',activebackground='gray', command = getSimVals).grid(row = 9, column = 3) #run button. Executes getSimVals()
	
	Label(top,text = 'Wave speed: ').grid(row = 1,column=0) #wave speed
	waveSpeedF = Entry(top,width=6)
	waveSpeedF.insert(10,'20.0') 
	waveSpeedF.grid(row = 1,column=1)
	
	Label(top,text = '         ').grid(row = 2,column=2)
	
	Label(top,text = 'Source velocity: ').grid(row = 3,column=0) #source velocity
	vsxF = Entry(top,width=6) # x value
	vsxF.insert(10,'5.0')
	vsxF.grid(row = 3,column=1)
	Label(top,text = ' , ').grid(row = 3,column=2)
	vsyF = Entry(top,width=6) # y value
	vsyF.insert(10,'0.0')
	vsyF.grid(row = 3,column=3)
	
	Label(top,text = 'Source initial position: ').grid(row = 4,column=0) #source startposition
	psxF = Entry(top,width=6) # x value
	psxF.insert(10,'0.0')
	psxF.grid(row = 4,column=1)
	Label(top,text = ' , ').grid(row = 4,column=2)
	psyF = Entry(top,width=6) # y value
	psyF.insert(10,'0.0')
	psyF.grid(row = 4,column=3)
	
	Label(top,text = '         ').grid(row = 5,column=2)
	
	Label(top,text = 'Observer velocity: ').grid(row = 6,column=0) #observer velocity
	voxF = Entry(top,width=6) # x value
	voxF.insert(10,'0.0')
	voxF.grid(row = 6,column=1)
	Label(top,text = ' , ').grid(row = 6,column=2)
	voyF = Entry(top,width=6) # y value
	voyF.insert(10,'0.0')
	voyF.grid(row = 6,column=3)
	
	Label(top,text = 'Observer initial position: ').grid(row = 7,column=0) #observer start position
	poxF = Entry(top,width=6) # x value
	poxF.insert(10,'2.0')
	poxF.grid(row = 7,column=1)
	Label(top,text = ' , ').grid(row = 7,column=2)
	poyF = Entry(top,width=6) # y value
	poyF.insert(10,'-1.0')
	poyF.grid(row = 7,column=3)
	
	Label(top,text = '       ').grid(row = 8,column=2)

global top

top = Tk()
mkMain() #Create the GUI
top.mainloop()	
	
