from time import time
from tkinter import X
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import math
import copy
import csv

#  Read the planet details and simulation parameters from file.
#  Implement the Beeman integration scheme to update the position and velocity of the
# planets and the sun at each time step.
#  Show the orbit of the planets as they move around the sun in a graphical display.
#  Calculate and print the orbital periods of the planets in Earth years (you may also
# write them to file if you wish, but this is not required).
#  Regularly write out to a file the total energy of the system, i.e. the sum of kinetic and
# gravitational potential energy.

# simulation of planets
# file with total energy
# planet data saved

class celestial_body(): 
    def __init__(self, mass, velocity, acceleration, position, name):
        self.mass = mass
        self.velocity = velocity
        self.acceleration = acceleration
        self.oldAcceleration = 0
        self.futureAcceleration = 0
        self.nextPos = 0
        self.position = position
        self.name = name

class controller():

    def __init__(self):
        self.bodies = []
        self.time = 0
        self.oldplace = []
        self.energies = {}
    def stringToList(self, string):
        parts = list(string.split(","))

    def read_planets(self):
        with open('planets.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    c.bodies.append(
                        celestial_body(float (row[0]),
                        np.array([float(row[1]),float(row[2])]),
                        np.array([float(row[3]),float(row[4])]),
                        np.array([float(row[5]),float(row[6])]),
                        row[7]))

                    line_count += 1

    # def write_planets(self):
    #     with open('planets.csv', mode='w', newline="") as f:
    #         writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #         writer.writerow(['mass', 'velocity', 'acceleration', 'position', 'name'])
    #         for i in self.bodies:
    #             writer.writerow([i.mass, i.velocity, i.acceleration, i.position, i.name])

    def animate(self, b):
        G = 6.67408*(10**-11)
        timestep = 86400
        self.time += 1
        for i in self.bodies: #### updated acceleration
            totalForce = np.array([0,0])
            for x in self.bodies:
                if i != x:
                    ##########################################################IMPOIRTANT
                    mass = i.mass * x.mass
                    r = x.position - i.position
                    rMag = np.linalg.norm(r)
                    rHat = r/np.linalg.norm(r)
                    # print(abs(np.linalg.norm(r))**2)
                    force = ((G * mass)/(rMag**2)) * rHat
                    totalForce = force + totalForce
                    # print(force)

            i.oldAcceleration = i.acceleration
            i.acceleration = totalForce / i.mass
            # print(i.acceleration)

        for i in self.bodies: #### updated position
            # nextP = i.position + (i.velocity*timestep) + (((1/6)*(timestep**2)) ((4*i.acceleration) - i.oldAcceleration))
            nextP1 = i.position
            # print(nextP1)

            nextP2 = i.velocity*timestep
            # print(nextP2)
            nextP3 = (1/6)*(timestep**2)
            # print(nextP3)
            nextP4 = (4*i.acceleration) - i.oldAcceleration
            # print(nextP4)
            nextP = nextP1 + nextP2 + (nextP3*nextP4)
            i.nextPos = nextP
            # print(i.position)
            # print(nextP)

        for i in self.bodies: #updates future acceleration
            totalForce = np.array([0,0])
            for x in self.bodies:
                if i != x:
                    ##########################################################IMPOIRTANT
                    mass = i.mass * x.mass
                    r = x.nextPos - i.nextPos
                    rMag = np.linalg.norm(r)
                    rHat = r/np.linalg.norm(r)
                    # print(abs(np.linalg.norm(r))**2)
                    force = ((G * mass)/(rMag**2)) * rHat
                    totalForce = force + totalForce
                    # print(force)

            # i.oldAcceleration = i.acceleration
            i.futureAcceleration = totalForce / i.mass

        for i in self.bodies: # future velocity
            p1 = i.velocity
            p2 = (1/6)*timestep
            p3 = (2*i.futureAcceleration) + 5*i.acceleration - i.oldAcceleration
            futureV = p1 + (p2 * p3)
            # if i.position[1] < 0 and i.nextPos[1] > 0:
                # print(str(i.name) + " has a period of: " + str(self.time))
            i.position = i.nextPos
            i.velocity = futureV
        KE = 0
        for i in self.bodies: #total kinetic for next step
            KE += (1/2)*(i.mass)*(np.linalg.norm(i.velocity)**2)
            # print(i.name)
            # print(KE)
        
        res = [(a, b) for idx, a in enumerate(self.bodies) for b in self.bodies[idx + 1:]]

        PE = 0
        # printing result 
        for i in res:
            distance = i[0].position - i[1].position
            # print(np.linalg.norm(distance))
            PE += (G*i[0].mass*i[1].mass)/abs(np.linalg.norm(distance))
        PE = PE/2
        # print("PE" + str(PE))
        # print("KE" + str(KE))
        # print(KE + PE)
        self.energies[self.time] = KE + PE
        if self.time == 1000:
            with open('energies.csv', mode='w', newline="") as f:
                writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(['time', 'energy'])
                for i, x in self.energies.items():
                    writer.writerow([i, x])

        # print(self.bodies[1].position[0])
        # print(self.bodies[1].position[1]) 
        for i in range(len(self.patches)):
            self.patches[i].center = (self.bodies[i].position[0],self.bodies[i].position[1])
        
        return self.patches

        


    def initializeGUI(self):
        # create plot elements
        fig = plt.figure()
        ax = plt.axes()
        self.patches = []
        # create circle of radius 0.1 centred at initial position and add to axes
        for i in self.bodies:
            self.patches.append(plt.Circle((i.position[0], i.position[1]), 5000000000, color = 'g', animated = True))
        for i in self.patches:
            ax.add_patch(i)

        # set up the axes
        ax.axis('scaled')
        ax.set_xlim(-400000000000, 400000000000)
        ax.set_ylim(-400000000000, 400000000000)
        # ax.set_xlabel('x (rads)')
        # ax.set_ylabel('sin(x)')

        # create the animator
        self.anim = FuncAnimation(fig, self.animate, frames = 100 , repeat = True, interval = 1, blit = True)

        # show the plot
        plt.show()
    
c = controller()
c.read_planets()
# c.write_planets()
# print(c.bodies[0].velocity + 1)
c.initializeGUI()
# c.animate(1)

