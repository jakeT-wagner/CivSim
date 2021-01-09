class Kingdom:
    def __init__(self, color, p_col):
        self.cells = []
        self.color = color
        self.p_col = p_col
        self.population = 0
        
    def join_kingdom(self, cell):
        cell.becomeOccupied(self.color, self.p_col)
        self.cells.append(cell)
    
    def get_population(self):
        self.population = 0
        for cell in self.cells:
            self.population += cell.population