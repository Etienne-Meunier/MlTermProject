import numpy as np
import random
from gym_micropolis.envs.corecontrol import MicropolisControl
from gym_micropolis.envs.tilemap import TileMap,zoneFromInt
from gi.repository import Gtk as gtk
from time import sleep
import json

# We only take a few buildings at first
buildings = ['NuclearPowerPlant','Residential','Commercial','Industrial','Road']
class Quimby :

    def __init__(self,map_h,map_w,gen_size,n_population,n_steps_evaluation):
        """
        :param map_h: Maximal height of the map
        :param map_w: Max width
        :param gen_size: lenght of the genome
        :param n_population: number of elements in population
        :param n_steps_evaluation: number of steps for evaluation
        """
        self.map_h =map_h
        self.map_w =map_w
        self.gen_size =gen_size
        self.n_population =n_population
        self.n_steps_evaluation =n_steps_evaluation

        # List of available buildings
        buildings = ['NuclearPowerPlant', 'Residential', 'Commercial', 'Industrial', 'Road']

        # Generate random first generation
        self.genomes = [[[np.random.randint(1, map_h), np.random.randint(1, map_w), random.choice(buildings)] for i in range(gen_size)]for p in range(n_population)]


    def cross_genomes(self,g1,g2) :
        """
        Take 2 genomes and build a new one using crossing
        """
        r = np.random.randint(len(g1))
        return(g1[0:r] + g2[r:])

    def mutate_genome(self,g1) :
        """
         Take a genome and apply a random transformation
        """
        p = np.random.randint(len(g1))
        g1[p] = [np.random.randint(1,self.map_h),np.random.randint(1,self.map_w),random.choice(buildings)]

    def build_city(self,g1,display) :
        """
        Build a city for a given genome an return it
        """
        m = MicropolisControl(self.map_h,self.map_w,display=display)
        m.clearMap()
        # Build
        for b in g1 :
            m.doTool(b[0],b[1],b[2])
        return m

    def evaluate(self,g1,display=False) :
        """
            Build and evaluate a city
        """
        m = self.build_city(g1,display)
        for i in range(self.n_steps_evaluation) :
            m.engine.simTick()
            if display : m.render()
        if display :
            m.win1.destroy()
        pop = m.engine.cityPop
        m.close()
        return pop
    def save_populations(self,path='population_save.json'):
        """
        Save the population in a json file
        :return:
        """
        a = [{'Population': self.populations[i], 'City': self.genomes[i]} for i in range(self.n_population)]
        with open(path, 'w') as fp:
            json.dump(a, fp)

    def evaluate_all(self):
        """
        Launch the Evaluation for all the genome
        :return:
        """
        self.populations = []
        for g in self.genomes:

            self.populations.append(self.evaluate(g, display=False))

