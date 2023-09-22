# Boid-Flocking
This project uses Pygame to visualize a flocking simulation using the BOID flocking algorithm and a simple physics engine.  
ThThe BOID flocking algorithm primarily consists of three parts:
* **Separation:** given a single agent, we don't want that agent to get too close to other agents.  This function provides a sum of acceleration vectors that point away from its nearest neighboring agents and are inversely proportional to the distance from the neighboring agent.  Essentially, the closer a neighbor is the stronger the acceleration away from that neighbor is.
* **Alignment:** given a group of agents, in order to exhibit flocking behavior we want them to all move in a similar direction.  This function provides an acceleration vector that points in the average direction of its neighbors' direction.  This helps ensure group behavior and some uniformity.
* **Cohesion:** given a group of agents, we want the group to remain together instead of agents splitting off on their own.  This function provides an acceleration vector pointing towards the center of mass of its neighbors.

The above simplee behaviors, when combined, allow for flocking patterns to emerge.  The Three acceleration vectors above are added together with each vector being multiplied by its corresponding weight so we can alter the strength of each of the behaviors, allowing for more fine tuned control of the behavior we want to observe.  Each behavior above also has a perception radius that allows us to alter how large or small we want to make the agents' field of view.

# Boid Flocking Demo
![](https://github.com/nick-pellegrin/Boid-Flocking/blob/master/boid_demo.gif)  

# Future Progress
The next step for this project is to implement a NEAT algorithm to evolve neural networks to control the agents autonomously, this would allow the agents to potentially exhibit more complex and more interesting behaviour and group dynamics.
