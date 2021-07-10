"""
------------------------------------------------------------------------------------------
--INTELLIGENT PARTICLE CLOUD MOTION--
authors: Nick Pellegrin and JonJon Gough
date created: March 31, 2021
The purpose of this project is to program "autonomous" particles using a NEAT AI, under their own 
propulsion, to move intelligently in a cloud formation without colliding.  We also 
ultimately aim to allow for the cloud to perform complex maneuvers in a coordinated 
manner, and finally to combine like lego blocks to materialize solid objects in a 
practical sense.

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
import os
import neat




#constants used for the simulation
WIN_WIDTH = 2200
WIN_HEIGHT = 1200
BACKGROUND_COLOR = (30, 30, 30)
gen = 0  #initial

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

    def __init__(self, x, y):
        """
        initializes particle object |
        x = (int) starting x coord |
        y = (int) starting y coord |
        is_leader = (boolean) is particle a leader |
        """

        self.position = np.array([float(x), float(y)])
        self.velocity = (np.random.rand(2) - 0.5)*10      # -5.0 < velocity < 5.0       -> [x, y]
        self.acceleration = (np.random.rand(2) - 0.5)/2   # -0.25 < acceleration < 0.25 -> [x, y]
        self.max_force = 0.3   #default: 0.3
        self.max_speed = 5     #default: 5
        #self.perception = 100  #in pixels, radius of max perception
        self.color = (255, 255, 255)
        self.min_dist = 10  #radius particles should not get closer than
        self.max_dist = 100 #radius particles should not get farther than

    
    def draw(self):
        """
        draws particle on screen at (x, y) |
        returns: none |
        """
        pygame.draw.circle(screen, self.color, (self.position[0], self.position[1]), self.PARTICLE_SIZE, 0)

    
    def edges(self):
        """
        wraps particles around edges of screen for continuity
        """
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
        self.edges()
        self.apply_behavior(cloud)
        self.update()
        self.draw()
        self.acceleration = np.array([0.0, 0.0])  #resets acceleration vector


    def update(self):
        self.position += self.velocity
        self.velocity += self.acceleration


    def get_inputs(self, cloud):
        """
        returns an array containing the distances between
        this particle and all other particles
        """
        inputs = []
        for particle in cloud:
            inputs.append(np.linalg.norm(particle.position - self.position))
        return inputs







"""
------------------------------------------------------------------------------------------
--SIMULATION LOOP--
This file runs the simulation for the fluid and synchronized motion of particles
using pygame to create the simulation, and python object to represent the particles
------------------------------------------------------------------------------------------
"""


def eval_genomes(genomes, config):
    """
    runs the simulation of the current population of
    birds and sets their fitness based on how well they flock
    """
    global gen
    gen += 1

    # start by creating lists holding the genome itself, the
    # neural network associated with the genome and the
    # bird object that uses that network to play
    ge = []
    nets = []
    particles = []
    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        particles.append(Particle(randint(150, 2050), randint(150, 1050)))
        ge.append(genome)


    score = 0

    clock = pygame.time.Clock()

    run = True
    while run and len(particles) > 0:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()


        for x, particle in enumerate(particles):  # give each particle a fitness of 0.1 for each particle in correct range
            inputs = particle.get_inputs() #array of distances between this particle and all other particles
            for i in inputs:
                if i > particle.min_dist and i < particle.max_dist:
                    ge[x].fitness += 0.1
#########################################################################################################################  finish working through function
                
            steering = net[particles.index(particle)]
            particle.move()

            # send bird location, top pipe location and bottom pipe location and determine from network whether to jump or not
            output = nets[birds.index(bird)].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:  # we use a tanh activation function so result will be between -1 and 1. if over 0.5 jump
                bird.jump()




        rem = []
        add_pipe = False
        for pipe in pipes:
            pipe.move()
            # check for collision
            for bird in birds:
                if pipe.collide(bird, win):
                    ge[birds.index(bird)].fitness -= 1
                    nets.pop(birds.index(bird))
                    ge.pop(birds.index(bird))
                    birds.pop(birds.index(bird))

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

        if add_pipe:
            score += 1
            # can add this line to give more reward for passing through a pipe (not required)
            for genome in ge:
                genome.fitness += 5
            pipes.append(Pipe(WIN_WIDTH))

        for r in rem:
            pipes.remove(r)

        for bird in birds:
            if bird.y + bird.img.get_height() - 10 >= FLOOR or bird.y < -50:
                nets.pop(birds.index(bird))
                ge.pop(birds.index(bird))
                birds.pop(birds.index(bird))

        draw_window(WIN, birds, pipes, base, score, gen, pipe_ind)

        # break if score gets large enough
        '''if score > 20:
            pickle.dump(nets[0],open("best.pickle", "wb"))
            break'''


# def run(config_file):
#     """
#     runs the NEAT algorithm to train a neural network to play flappy bird.
#     :param config_file: location of config file
#     :return: None
#     """
#     config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
#                          neat.DefaultSpeciesSet, neat.DefaultStagnation,
#                          config_file)

#     # Create the population, which is the top-level object for a NEAT run.
#     p = neat.Population(config)

#     # Add a stdout reporter to show progress in the terminal.
#     p.add_reporter(neat.StdOutReporter(True))
#     stats = neat.StatisticsReporter()
#     p.add_reporter(stats)
#     #p.add_reporter(neat.Checkpointer(5))

#     # Run for up to 50 generations.
#     winner = p.run(eval_genomes, 50)

#     # show final stats
#     print('\nBest genome:\n{!s}'.format(winner))



def run(config_file):
    #declares and initializes our particles
    particle_list = []
    for i in range(100):
        particle_list.append(Particle(randint(150, 2050), randint(150, 1050)))



    #main simulation loop
    while 1: 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            

        #for i in particle_list:
            #i.draw()
            #i.move( pygame.mouse.get_pos(), particle_list ) 
        
        pygame.display.update()
        #screen.fill(BACKGROUND_COLOR)
        #pygame.time.delay(5)



if __name__ == '__main__':
     # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
    