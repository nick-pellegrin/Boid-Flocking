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
from random import *



#constants used for the simulation
WIN_WIDTH = 1100
WIN_HEIGHT = 700
BACKGROUND_COLOR = (30, 30, 30)
TOTAL_PIXELS = 0

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
    
    PARTICLE_SIZE = 5  #in pixels

    def __init__(self, x, y):
        """
        initializes particle object |
        x = starting x coord |
        y = starting y coord |
        """
        self.x = x
        self.y = y
        self.IMG = pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.PARTICLE_SIZE, 0)

    
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
        pygame.draw.circle(screen, (255, 255, 255), (x, y), self.PARTICLE_SIZE, 0)
    
   
    def move(self, pos_at, pos_to, index, TOGGLE_X_SIDE, TOGGLE_Y_SIDE):
        """
        moves particle |
        pos_at = current location (x_at, y_at) |
        pos_to = desired location (x_to, y_to) |
        returns: none |
        """
        x_at, y_at = pos_at
        x_to, y_to = pos_to
        x_multiplier = 0
        y_multiplier = 0
        x_box_destination = 0
        y_box_destination = 0

        firstQuarter = TOTAL_PIXELS*0.25
        secondQuarter = TOTAL_PIXELS*0.5
        thirdQuarter = TOTAL_PIXELS*0.75

        if index <= firstQuarter:
            x_box_destination = x_to + (TOGGLE_X_SIDE * index)
            y_box_destination = y_to + firstQuarter
        elif index <= secondQuarter:
            x_box_destination = x_to + firstQuarter
            y_box_destination = y_to + (TOGGLE_Y_SIDE * (index - firstQuarter))
        elif index <= thirdQuarter:
            x_box_destination = x_to + (TOGGLE_X_SIDE * (index - secondQuarter))
            y_box_destination = y_to - firstQuarter
        else:
            x_box_destination = x_to - firstQuarter
            y_box_destination = y_to + (TOGGLE_Y_SIDE * (index - thirdQuarter))

        TOGGLE_X_SIDE = TOGGLE_X_SIDE * -1
        TOGGLE_Y_SIDE = TOGGLE_Y_SIDE * -1


        


        if x_box_destination != x_at and y_box_destination != y_at: #stops loop when particle reaches destination 
            
            slope = (y_box_destination - y_at) / (x_box_destination - x_at) #sets slope (needs to be inverted for vertical movements)
                
            # for more horizontal movement 
            if abs(slope) <= 1:           
                if x_box_destination > x_at:            
                    x_inc = 1              
                    y_inc = slope          
                if x_box_destination < x_at:            
                    x_inc = -1             
                    y_inc = -slope   
            
            # for more vertical movement
            elif abs(slope) > 1:          
                
                # if slope is positive
                if slope > 0:                  
                    if x_box_destination > x_at:            
                        x_inc = 1/slope        
                        y_inc = 1              
                    if x_box_destination < x_at:            
                        x_inc = -1/slope       
                        y_inc = -1     

                # if slope is negative
                if slope < 0:              
                    if x_box_destination > x_at:            
                        x_inc = -1/slope        
                        y_inc = -1              
                    if x_box_destination < x_at:            
                        x_inc = 1/slope       
                        y_inc = 1               
                    

            self.x = x_at + x_inc
            self.y = y_at + y_inc
            x_at = x_at + x_inc
            y_at = y_at + y_inc

            
            self.draw(self.x, self.y)
            #pygame.display.update()
            #pygame.time.delay(1)
        else: self.draw(x_at, y_at)
            
            
        





"""
------------------------------------------------------------------------------------------
--SIMULATION LOOP--

This file runs the simulation for the fluid and synchronized motion of particles
using pygame to create the simulation, and python object to represent the particles

------------------------------------------------------------------------------------------
"""

#declares and initializes our first particle
particleList = []
randomNum = randint(100, 699)
for num in range(0, randomNum):
    particleList.append(Particle(randint(1, 1100), randint(1, 700)))

TOTAL_PIXELS = len(particleList)
TOGGLE_X_SIDE = -1
TOGGLE_Y_SIDE = 1

#main simulation loop
eventCount = 0
while 1: 
    for event in pygame.event.get():
        eventCount += 1
        if event.type == pygame.QUIT:
            sys.exit()

        
        if event.type == pygame.MOUSEBUTTONDOWN: #Will only work with at most 2 clicks in a row - otherwise it will skip ahead and go to wherever you clicked right before the particle reaches its 1st destination
            for num in range(0, 2000):
                for num in range(0, randomNum):
                    particleList[num].move( particleList[num].get_pos(), pygame.mouse.get_pos(), num, TOGGLE_X_SIDE, TOGGLE_Y_SIDE )
                    TOGGLE_X_SIDE =TOGGLE_X_SIDE * -1
                    TOGGLE_Y_SIDE = TOGGLE_Y_SIDE * -1
                
                pygame.display.update()
                screen.fill(BACKGROUND_COLOR)
                #pygame.time.delay(100)
            break

            
            
    pygame.display.update()