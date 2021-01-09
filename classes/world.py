from .constants import COLORS
from .cell import Cell
from .kingdom import Kingdom
import PIL
from PIL import Image
from random import random
from random import seed 
from datetime import datetime
seed(datetime.now())
class World:
    def __init__(self, veg_im, elv_im, teams):
        self.rows = 205
        self.cols = 155
        self.cell_size = 5
        self.kingdoms = []
        self.cells = []
        self.veg_im = veg_im
        self.elv_im = elv_im
        self.teams = teams
        self.initiate_world()
    
    def create_kingdom(self, color, p_col):
        self.kingdoms.append(Kingdom(color, p_col))
    
    def get_kingdom(self,color):
        for kingdom in self.kingdoms:
            if kingdom.color == color:
                return kingdom 
        return None
    
    def initialize_kingdom(self, color):
        p_col = 0.05 + random()* 0.15
        self.create_kingdom(color, p_col)
        found = False
        kingdom = self.get_kingdom(color)
        while not found:
            row = int(random() * self.rows)
            col = int(random() * self.cols)
            if not self.cells[row][col].occupied and self.cells[row][col].active:
                self.cells[row][col].becomeOccupied(color, p_col)
                kingdom.join_kingdom(self.cells[row][col])
                self.cells[row+1][col+1].becomeOccupied(color,p_col)
                kingdom.join_kingdom(self.cells[row+1][col+1])
                self.cells[row-1][col-1].becomeOccupied(color, p_col)
                kingdom.join_kingdom(self.cells[row-1][col-1])
                self.cells[row-1][col+1].becomeOccupied(color, p_col)
                kingdom.join_kingdom(self.cells[row-1][col+1])
                self.cells[row+1][col-1].becomeOccupied(color,p_col)
                kingdom.join_kingdom(self.cells[row+1][col-1])
                found = True
                             
    def initiate_world(self):
        for row in range(self.rows):
            self.cells.append([])
            for col in range(self.cols):
                self.cells[row].append(0)
        veg_im = Image.open(self.veg_im)
        elv_im = Image.open(self.elv_im)
        for i in range(0, self.rows*self.cell_size,self.cell_size):
            for j in range(0, self.cols*self.cell_size, self.cell_size):
                pix = veg_im.getpixel((i,j))
                elv_pix = elv_im.getpixel((i,j))
                if (not(pix[0] == pix[1] == pix[2] == 255)): # if not an all-white pixel
                    P_ext = 1.0
                    elv_P_ext = 0.0
                    if (pix[0] == 7 and pix[1] == 120 and pix[2] == 11): # Temperate Forest
                        P_ext = 0.12
                    elif (pix[0] == 255 and pix[1] == 128 and pix[2] == 0): # Grassland
                        P_ext = 0.12
                    elif (pix[0] == 255 and pix[1] == 242 and pix[2] == 0): # Desert
                        P_ext = 0.17
                    elif (pix[0] == 0 and pix[1] == 79 and pix[2] == 0): # Tropical Forest
                        P_ext = 0.12
                    elif (pix[0] == 22 and pix[1] == 204 and pix[2] == 250): # Tundra
                        P_ext = 1.0
                    elif (pix[0] == 164 and pix[1] == 252 and pix[2] == 67): # Warm-temperate Forest
                        P_ext = 0.18
                    elif (pix[0] == 128 and pix[1] == 128 and pix[2] == 255): # Boreal Forest
                        P_ext = 1.0
                    elif (pix[0] == 132 and pix[1] == 97 and pix[2] == 37): # Savanna
                        P_ext = 0.08
                    elif (pix[0] == pix[1] == pix[2] == 200):
                        P_ext = 1.0
                    else:
                        P_ext = 1.0

                    if (elv_pix[0] == 203 and elv_pix[1] == 131 and elv_pix[2] == 7):
                        elv_P_ext = 0.05
                    elif (elv_pix[0] == 203 and elv_pix[1] == 41 and elv_pix[2] == 21):
                        elv_P_ext = 0.10
                    elif (elv_pix[0] == 112 and elv_pix[1] == 6 and elv_pix[2] == 6):
                        elv_P_ext = 0.22

                    self.cells[int(i/self.cell_size)][int(j/self.cell_size)] = Cell(i, j, True, P_ext, elv_P_ext, 0.0,0.0,0.2) #active cell with parameters based on vegetation, elevation
                else:
                    self.cells[int(i/self.cell_size)][int(j/self.cell_size)] = Cell(i, j, False, 1.0, 1.0, 1.0,0.0,0.2) # inactive cell
        
        for i in range(self.teams):
            color = COLORS[i]
            self.initialize_kingdom(color)