"""
------------------------------------------------------------------------------------------

--INTELLIGENT PARTICLE CLOUD MOTION--

authors: Nick Pellegrin and JonJon Gough
date created: March 31, 2021

The purpose of this project is to program "autonomous" particles, under their own 
propulsion, to move intelligently in a cloud formation without colliding.  We also 
ultimately aim to allow for the cloud to perform complex maneuvers in a coordinated 
manner, and finally to combine like lego blocks to materialize solid objects in a 
practical sense.

(for development):

    1. (done)  move particle in a straight line towards destination
    2. (done)  depending on destination, make velocity of particle universal for steep/shallow motion

    1. ()  allow velocity of single particle to correlate to distance it must travel
    2. ()  add acceleration/decceleration mechanics when starting/ending path of motion
    3. ()  allow particles to fluidly change direction while in motion

    1. ()  when multiple particles are in motion, prevent collisions between particles 
    2. ()  add random forces to account for real world situations
    3. ()  allow for path corrections for groups of particles due to random forces

    1. ()  add ability to combine to create solid shapes

    1. ()  add capability to perform more complex maneuvers (might require 3D simulation)

Contents of python file:

    -imports
    -global constants and init of pygame
    -----------------------------------------
    -Particle class
    -----------------------------------------
    -simulation loop


------------------------------------------------------------------------------------------
"""


import pygame
import sys
import math
from random import *
import numpy as np



#constants used for the simulation
WIN_WIDTH = 1100
WIN_HEIGHT = 700
BACKGROUND_COLOR = (30, 30, 30)

#initializes the module packages and the screen
pygame.init()
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
screen.fill(BACKGROUND_COLOR)


"""
------------------------------------------------------------------------------------------
--PARTICLE CLASS--

This is the python object used to represent a single particle.
Contains the instructions for the movement mechanics of a single particle.

------------------------------------------------------------------------------------------
"""
      

class Particle:
    
    PARTICLE_SIZE = 2    #in pixels

    def __init__(self, x, y, is_leader):
        """
        initializes particle object |
        x = (int) starting x coord |
        y = (int) starting y coord |
        is_leader = (boolean) is particle a leader |
        """
        #leader follows mouse, non-leader exhibits flocking behavior
        self.is_leader = is_leader  
        self.position = np.array([float(x), float(y)])
        self.velocity = (np.random.rand(2) - 0.5)*10      # -5.0 < velocity < 5.0       -> [x, y]
        self.acceleration = (np.random.rand(2) - 0.5)/2   # -0.25 < acceleration < 0.25 -> [x, y]
        self.max_force = 0.3   #default: 0.3
        self.max_speed = 5     #default: 5
        #self.perception = 100  #in pixels, radius of max perception
        self.alignment_perception = 70
        self.cohesion_perception = 150
        self.separation_perception = 100
        self.alignment_strength = 1
        self.cohesion_strength = 0.7
        self.separation_strength = 1

    
    def draw(self):
        """
        draws particle on screen at (x, y) |
        returns: none |
        """
        if self.is_leader: self.color = (255, 0, 0)
        else: self.color = (255, 255, 255)
        pygame.draw.circle(screen, self.color, (self.position[0], self.position[1]), self.PARTICLE_SIZE, 0)


    def avoid_edges(self, width, height, margin):
        acceleration = np.zeros(2)
        x, y = self.position
        if x < margin:
            acceleration[0] = (margin - x) / margin
        elif x > width - margin:
            acceleration[0] = (width - margin - x) / margin
        if y < margin:
            acceleration[1] = (margin - y) / margin
        elif y > height - margin:
            acceleration[1] = (height - margin - y) / margin
        self.acceleration = acceleration * self.max_force
    
    def edges(self):
        if self.position[0] > WIN_WIDTH:
            self.position[0] = 0
        elif self.position[0] < 0:
            self.position[0] = WIN_WIDTH
        if self.position[1] > WIN_HEIGHT:
            self.position[1] = 0
        elif self.position[1] < 0:
            self.position[1] = WIN_HEIGHT


    def move(self, pos_to, cloud):
        """
        moves particle |
        pos_at = current location (x_at, y_at) |
        pos_to = desired location (x_to, y_to) |
        returns: none |
        """
        if self.is_leader:
            x_at = self.position[0]
            y_at = self.position[1]
            x_to, y_to = pos_to
            dist_vector = [x_to - x_at, y_to - y_at]  # vector starting at 'pos_at' going to to 'pos_to'
            norm = np.linalg.norm(dist_vector)        # finds the norm (magnitude) of dist_vector
            self.velocity = dist_vector/norm          # a unit vecotr pointing to destination
            self.position += self.velocity
            self.draw()
        else:
            # self.edges()
            self.avoid_edges(WIN_WIDTH, WIN_HEIGHT, 50)
            self.apply_behavior(cloud)
            self.update()
            self.draw()
            self.acceleration = np.array([0.0, 0.0])  #resets acceleration vector


    def update(self):
        self.position += self.velocity
        self.velocity += self.acceleration


    def apply_behavior(self, cloud):
        """
        governs particle flock behavior |
        cloud = list of particles |
        returns: none |
        """
        alignment = self.align(cloud) * self.alignment_strength
        cohesion = self.cohesion(cloud) * self.cohesion_strength
        separation = self.separation(cloud) * self.separation_strength
        self.acceleration += alignment
        self.acceleration += cohesion
        self.acceleration += separation


    def align(self, cloud):
        """
        steers the particle in the average direction of all the particles in its perceptinon radius |
        cloud = list of particles |
        returns: steering vector [x, y] |
        """
        steering = np.array([0.0, 0.0])
        total = 0
        for particle in cloud:
            if np.linalg.norm(particle.position - self.position) < self.alignment_perception:
                steering += particle.velocity
                total += 1
        if total > 0:
            steering /= total
            steering = (steering / np.linalg.norm(steering)) * self.max_speed
            steering = steering - self.velocity
        if np.linalg.norm(steering) > self.max_force:
            steering = (steering/np.linalg.norm(steering)) * self.max_force
        return steering
    

    def cohesion(self, cloud):
        """
        steers particles towards the center of mass of all particles within its perception radius  |
        cloud = list of particles |
        returns: steering vector [x, y] |
        """
        steering = np.array([0.0, 0.0])
        total = 0
        for particle in cloud:
            if np.linalg.norm(particle.position - self.position) < self.cohesion_perception:
                steering += particle.position
                total += 1
        if total > 0:
            steering /= total
            steering = steering - self.position
            if np.linalg.norm(steering) > 0:
                steering = (steering / np.linalg.norm(steering)) * self.max_speed
            steering = steering - self.velocity
        if np.linalg.norm(steering) > self.max_force:
            steering = (steering/np.linalg.norm(steering)) * self.max_force
        return steering

    
    def separation(self, cloud):
        """
        steers particles away from other particles, inversely proportional to dist between particles  |
        cloud = list of particles |
        returns: steering vector [x, y] |
        """
        steering = np.array([0.0, 0.0])
        total = 0
        for particle in cloud:
            if particle != self and np.linalg.norm(particle.position - self.position) < self.separation_perception:
                difference = self.position - particle.position
                difference /= np.linalg.norm(particle.position - self.position)
                steering += difference
                total += 1
        if total > 0:
            steering /= total
            if np.linalg.norm(steering) > 0:
                steering = (steering / np.linalg.norm(steering)) * self.max_speed
            steering = steering - self.velocity
        if np.linalg.norm(steering) > self.max_force:
            steering = (steering/np.linalg.norm(steering)) * self.max_force
        return steering
    
    
        
        
        
            
        





"""
------------------------------------------------------------------------------------------
--SIMULATION LOOP--

This file runs the simulation for the fluid and synchronized motion of particles
using pygame to create the simulation, and python object to represent the particles

------------------------------------------------------------------------------------------
"""


#declares and initializes our particles
particle_list = []
for i in range(50):
    particle_list.append(Particle(randint(150, 950), randint(150, 550), False))



#main simulation loop
while 1: 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in particle_list:
                if i.cohesion_perception == 150:
                    i.cohesion_perception = 1000
                    i.alignment_strength = 0
                    i.separation_strength = 0
                elif i.cohesion_perception == 1000:
                    i.cohesion_perception = 150
                    i.alignment_strength = 1
                    i.separation_strength = 1


    
    for i in particle_list:
        i.move( pygame.mouse.get_pos(), particle_list ) 
    
    pygame.display.update()
    screen.fill(BACKGROUND_COLOR)
    #pygame.time.delay(5)
    



