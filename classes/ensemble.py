from .world import World
from .kingdom import Kingdom
from .cell import Cell
import copy
import PIL
from PIL import Image

class Ensemble:
    def __init__(self, world, image):
        self.world = world
        self.cells = copy.deepcopy(world.cells)
        self.img = image

    def update(self):
        for row in self.cells:
            for cell in row:
                if (cell.occupied):
                    cell.update(self)
        for kingdom in self.world.kingdoms:
            #population doesnt work at this point. The issue is the cells do not update within the kingdom class, but only in the 
            #world class
            kingdom.get_population()
                    
    def outputToFile(self, counter):
        if (counter%100 == 0):
            im = Image.open(self.img)
            fileName = "outputs" + str(counter/100) +".png"
            for i in range(self.world.rows):
                for j in range(self.world.cols):
                    if (self.cells[i][j].occupied):
                        for x in range(5):
                            for y in range(5):
                                im.putpixel( (int(i * 5 + (x-2) ), int(j * 5 + (y-2) ) ), self.cells[i][j].color)

            im.save(fileName)
            im.close()

    def draw(self):
        im = Image.open(self.img)
        im = im.copy()
        for i in range(self.world.rows):
            for j in range(self.world.cols):
                if self.cells[i][j].occupied:
                    for x in range(5):
                        for y in range(5):
                            im.putpixel( (int(i * 5 + (x-2) ), int(j * 5 + (y-2) ) ), self.cells[i][j].color)
        return im 

    def run(self, age, step, st_image, age_text, prog_bar, steps):
            self.update()
            im = self.draw()
            age += 10
            str_age = str(abs(age))
            prog_bar.progress(step / (steps-1))
            if age < 0:
                time_suffix = "BC"
            else:
                time_suffix = "AD"
            age_text.text("Current time: " + str_age + " " + time_suffix)
            st_image.image(im,ouput_format = "JPEG", use_column_width = True)
            return age
        
        