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
    
    PARTICLE_SIZE = 5     #in pixels
    NEIGHBOR_RADIUS = 10  #in pixels

    def __init__(self, x, y, is_leader):
        """
        initializes particle object |
        x = (int) starting x coord |
        y = (int) starting y coord |
        is_leader = (boolean) is particle a leader |
        """
        self.x = x
        self.y = y
        self.is_leader = is_leader
        self.velocity = [0, 0]
        self.acceleration = [0, 0]

        if self.is_leader: self.color = (255, 0, 0)
        else: self.color = (255, 255, 255)
        self.IMG = pygame.draw.circle(screen, self.color, (self.x, self.y), self.PARTICLE_SIZE, 0)

    
    def get_pos(self):
        """
        returns: current position in form of (x, y)
        """
        return (self.x, self.y)

    
    def draw(self, x, y):
        """
        draws particle on screen at (x, y) |
        returns: none |
        """
        pygame.draw.circle(screen, (255, 0, 0), (x, y), self.PARTICLE_SIZE, 0)
    
   
    def move(self, pos_at, pos_to):
        """
        moves particle |
        pos_at = current location (x_at, y_at) |
        pos_to = desired location (x_to, y_to) |
        returns: none |
        """
        if self.is_leader:
            x_at, y_at = pos_at
            x_to, y_to = pos_to

            dist_vector = [x_to - x_at, y_to - y_at]  # vector starting at 'pos_at' going to to 'pos_to'
            norm = np.linalg.norm(dist_vector)        # finds the norm (magnitude) of dist_vector
            self.velocity =  3*(dist_vector/norm)          # a unit vecotr pointing to destination

            self.x += self.velocity[0]
            self.y += self.velocity[1]
            
            self.draw(self.x, self.y)


    def get_direction(self):
        """
        gets direction of the particle |
        returns: [x, y] |
        """

        return self.velocity
        
        
        
            
        





"""
------------------------------------------------------------------------------------------
--SIMULATION LOOP--

This file runs the simulation for the fluid and synchronized motion of particles
using pygame to create the simulation, and python object to represent the particles

------------------------------------------------------------------------------------------
"""


#declares and initializes our particles
particle_list = []
for i in range(100):
    particle_list.append(Particle(randint(50, 1050), randint(50, 650), True))



#main simulation loop
while 1: 
    # for event in pygame.event.get():
        
    #     if event.type == pygame.QUIT:
    #         sys.exit()

        
    #     if event.type == pygame.MOUSEBUTTONDOWN:
    #         p_1.move( p_1.get_pos(), pygame.mouse.get_pos() )

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()
        

    for i in particle_list:
        i.move( i.get_pos(), pygame.mouse.get_pos() )
        
    
    
    pygame.display.update()
    screen.fill(BACKGROUND_COLOR)
    pygame.time.delay(15)
    



