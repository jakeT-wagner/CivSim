from .constants import NOISE_CONSTANT
import numpy as np
from random import random

class Cell:
    def __init__(self, i, j, active, veg_P_ext, elv_P_ext, density_P_ext, color, p_col):
        self.x = int(i / 5)
        self.y = int(j / 5)
        self.color = color
        self.active = active
        self.occupied = False # initalize all cells to unoccupied
        self.p_col = p_col
        self.veg_P_ext = veg_P_ext + np.random.normal(0, NOISE_CONSTANT) # probability of extinction based on vegetation
        self.elv_P_ext = elv_P_ext + np.random.normal(0, NOISE_CONSTANT) # probability of extinction based on elevation
        self.density_P_ext = density_P_ext # probability of extinction based on population sensity
        self.P_ext = self.veg_P_ext + self.elv_P_ext + self.density_P_ext # total probability of extinction
        self.border = True
        self.population = 1000
        
    def becomeOccupied(self,color,p_col):
        self.occupied = True
        self.color = color
        self.p_col = p_col
        
    def becomeExtinct(self):
        self.occupied = False

    def getValidNeighboringCells(self, e):
        d = [] # empty directions array
        i = self.x
        j = self.y
        if (e.cells[i-1][j].active and not e.cells[i-1][j].occupied):
            d.append('u')
        if (e.cells[i+1][j].active and not e.cells[i+1][j].occupied):
            d.append('d')
        if (e.cells[i][j-1].active and not e.cells[i][j-1].occupied):
            d.append('l')
        if (e.cells[i][j+1].active and not e.cells[i][j+1].occupied):
            d.append('r')
        if len(d) <= 1:
            self.border = False
        return d
    
    def checkPopulationDensity(self, e): # search cells in a 5x5 grid for neighbors
        neighbors = 0
        i, j = self.x, self.y
        for k in range(5):
            for l in range(5):
                if (e.cells[i-2][j-2].occupied): 
                    neighbors += 1
        return (neighbors / 96) + np.random.normal(0, NOISE_CONSTANT)
    
        
    def colonizeNeighbor(self, direction, e): 
        i = self.x
        j = self.y
        if (direction == 'u'):
            e.cells[i-1][j].becomeOccupied(self.color, self.p_col)
        elif (direction == 'd'):
            e.cells[i+1][j].becomeOccupied(self.color, self.p_col)
        elif (direction == 'l'):
            e.cells[i][j-1].becomeOccupied(self.color, self.p_col)
        elif (direction == 'r'):
            e.cells[i][j+1].becomeOccupied(self.color, self.p_col)
        self.population += self.population ** 1 + (random()*0.2)
            
    
    def update(self, e): # called each time step if cell is active and populated. Ensemble
        self.P_density_ext = self.checkPopulationDensity(e) 
        self.P_ext = self.veg_P_ext + self.elv_P_ext + self.density_P_ext # update probability of extinction
        #e.cells[self.x][self.y].P_ext = self.P_ext
        if (self.active and self.occupied):
            if (random() < self.p_col):
                potential_directions = self.getValidNeighboringCells(e)
                if (len(potential_directions) > 0):
                    direction = potential_directions[int(random() * len(potential_directions))]
                    self.colonizeNeighbor(direction, e)
            if (random() < self.P_ext) and self.border:
                self.becomeExtinct()