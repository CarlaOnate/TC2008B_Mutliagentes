import agentpy as ap
import numpy as np
import random

class Roomba(ap.Agent):
    def setup(self):
        self.location = (0, 0)

    def cleanCell(self):
        if (self.model.floors[self.location[0]][self.location[1]] == 1):
            print('\n \tCLEANED CELL')
            self.model.floors[self.location[0]][self.location[1]] = 0
            self.model.cleanedCells = self.model.cleanedCells + 1

    def move(self):
        direction = random.randint(0, 8)
        self.grid = self.model.grid
        self.random = self.model.random

        if direction == 0: self.grid.move_to(self, (self.location[0]  - 1, self.location[1])) # up
        if direction == 1: self.grid.move_to(self, (self.location[0]  + 1, self.location[1])) # down
        if direction == 2: self.grid.move_to(self, (self.location[0], self.location[1] - 1)) # left
        if direction == 3: self.grid.move_to(self, (self.location[0], self.location[1] + 1)) # right
        if direction == 4: self.grid.move_to(self, (self.location[0] - 1, self.location[1] + 1)) # rigth upward diagonal
        if direction == 5: self.grid.move_to(self, (self.location[0] - 1, self.location[1] - 1)) # left upward diagonal
        if direction == 6: self.grid.move_to(self, (self.location[0] + 1, self.location[1] + 1)) # right downward diagonal
        if direction == 7: self.grid.move_to(self, (self.location[0] + 1, self.location[1] - 1)) # left downward diagonal
        self.location = self.grid.positions[self]

class RoombaModel(ap.Model):    
    def setup(self):
        row = self.p.row
        columns = self.p.columns

        ratioDirtyCells = self.p.ratio_dirty_cells / 100
        ratioCleanCells = (1 - ratioDirtyCells)

        self.agents = ap.AgentList(self, self.p.agents, Roomba)
        self.grid = ap.Grid(self, (row, columns))
        self.floors = np.random.choice([0, 1], size=(row, columns), p=[ratioCleanCells, ratioDirtyCells])
        self.cleanedCells = 0
        self.grid.add_agents(self.agents)
        print(self.floors)

    def step(self):
        self.agents.cleanCell()
        self.agents.move()

    def update(self):
        if not (1 in self.floors):
            self.stop()

    def end(self):
        print('\nFINAL FLOOR => \n', self.floors)
        self.report('cleaned_cells', self.cleanedCells)

# RUN SIMULATION
parameters = {
    'row': 5,
    'columns': 5,
    'agents': 5,
    'ratio_dirty_cells': 50,
    'steps': 100
}

model = RoombaModel(parameters)
results = model.run()

print('\n\n', results.reporters)