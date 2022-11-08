import agentpy as ap
import numpy as np
import random

def countDirtyCells(grid):
    dirtyCells = 0
    for row in grid:
        for col in row:
            if col == 1: dirtyCells += 1
    return dirtyCells

class Roomba(ap.Agent):
    def setup(self):
        self.location = (1, 1)
        self.movements = 0

    def cleanCell(self):
        if (self.model.floors[self.location[0]][self.location[1]] == 1):
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
        
        if self.location != self.grid.positions[self]: self.movements += 1
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
        self.totalSteps = 0
        self.grid.add_agents(self.agents)
        self.dirtyCells = countDirtyCells(self.floors)
        
    def step(self):
        self.agents.cleanCell()
        self.agents.move()
        self.totalSteps += 1

    def update(self):
        if not (1 in self.floors):
            self.stop()

    def end(self):
        dirtyCellsReamining = countDirtyCells(self.floors)
        if self.dirtyCells != 0:
            percentageDirtyCells = (dirtyCellsReamining * 100) / self.dirtyCells
        else:
            percentageDirtyCells = 0
        self.report('cleaned_cells', percentageDirtyCells)
        self.report('num_agents', self.agents.__len__())
        self.report('min_moves', min(self.agents.movements))
        self.report('max_moves', max(self.agents.movements))
        self.report('total_steps', self.totalSteps)
        self.report('size', str(self.p.row) + ' * ' + str(self.p.columns))

# RUN SIMULATION
def printResult(results):
    agentNum = 1
    print('\n\n Movements => ')
    for agent in results.reporters.agents[0]:
        print('Agent ', agentNum, ': ', agent)
        agentNum += 1
    print('% DIRTY CELLS REMAINING', results.reporters.cleaned_cells)

variedParameters = {
    'row': ap.IntRange(5, 40),
    'columns': ap.IntRange(5, 40),
    'agents': ap.IntRange(1, 20),
    'ratio_dirty_cells': ap.IntRange(10, 100),
    'steps': 100
}

fixedParams = {
    'row': 10,
    'columns': 10,
    'agents': 5,
    'ratio_dirty_cells': 20,
    'steps': 100
}

""" model = RoombaModel(fixedParams)
results = model.run()
printResult(results) """

# FIRST SIMULATION:
# Size remains and ratio while number of agents varies

def runSimulation_1():
    print('\n------------- SIMULATION 1 -----------------')
    parameters = {
        'row': 20,
        'columns': 20,
        'agents': ap.IntRange(1, 20),
        'ratio_dirty_cells': 20,
        'steps': 5000
    }
    sample = ap.Sample(parameters, n=5)
    exp = ap.Experiment(RoombaModel, sample, iterations=10)
    results1 = exp.run()
    results1.save()
    results1 = ap.DataDict.load('RoombaModel')
    print(results1.reporters, '\n\n')

    # DATA SUMMARY
    averageCellsCleaned = sum(results1.reporters['cleaned_cells']) / results1.reporters['cleaned_cells'].__len__()
    averageMinMoves = sum(results1.reporters['min_moves']) / results1.reporters['min_moves'].__len__()
    averageMaxMoves = sum(results1.reporters['max_moves']) / results1.reporters['max_moves'].__len__()
    print('AVERAGE DIRTY CELLS REMAINING => ', averageCellsCleaned)
    print('AVERAGE MIN MOVEMENTS => ', averageMinMoves)
    print('AVERAGE MAX MOVEMENTS => ', averageMaxMoves)
    #     print('TOTAL_STEPS', results1.reporters['total_steps'])
    print('\n\n')

def runSimulation_2():
    print('\n------------- SIMULATION 2 -----------------')
    parameters = {
        'row': 60,
        'columns': 60,
        'agents': ap.IntRange(1, 20),
        'ratio_dirty_cells': 20,
        'steps': 5000
    }
    sample = ap.Sample(parameters, n=5)
    exp = ap.Experiment(RoombaModel, sample, iterations=10)
    results1 = exp.run()
    results1.save()
    results1 = ap.DataDict.load('RoombaModel')
    print(results1.reporters, '\n\n')

    # DATA SUMMARY
    averageCellsCleaned = sum(results1.reporters['cleaned_cells']) / results1.reporters['cleaned_cells'].__len__()
    averageMinMoves = sum(results1.reporters['min_moves']) / results1.reporters['min_moves'].__len__()
    averageMaxMoves = sum(results1.reporters['max_moves']) / results1.reporters['max_moves'].__len__()
    print('AVERAGE DIRTY CELLS REMAINING => ', averageCellsCleaned)
    print('AVERAGE MIN MOVEMENTS => ', averageMinMoves)
    print('AVERAGE MAX MOVEMENTS => ', averageMaxMoves)
    #     print('TOTAL_STEPS', results1.reporters['total_steps'])
    print('\n\n')

def runSimulation_3():
    print('\n------------- SIMULATION 3 -----------------')
    parameters = {
        'row': 20,
        'columns': 20,
        'agents': ap.IntRange(1, 50),
        'ratio_dirty_cells': 20,
        'steps': 5000
    }
    sample = ap.Sample(parameters, n=5)
    exp = ap.Experiment(RoombaModel, sample, iterations=10)
    results1 = exp.run()
    results1.save()
    results1 = ap.DataDict.load('RoombaModel')
    print(results1.reporters, '\n\n')

    # DATA SUMMARY
    averageCellsCleaned = sum(results1.reporters['cleaned_cells']) / results1.reporters['cleaned_cells'].__len__()
    averageMinMoves = sum(results1.reporters['min_moves']) / results1.reporters['min_moves'].__len__()
    averageMaxMoves = sum(results1.reporters['max_moves']) / results1.reporters['max_moves'].__len__()
    print('AVERAGE DIRTY CELLS REMAINING => ', averageCellsCleaned)
    print('AVERAGE MIN MOVEMENTS => ', averageMinMoves)
    print('AVERAGE MAX MOVEMENTS => ', averageMaxMoves)
    #     print('TOTAL_STEPS', results1.reporters['total_steps'])
    print('\n\n')

def runSimulation_4():
    print('\n------------- SIMULATION 4 -----------------')
    parameters = {
        'row': 60,
        'columns': 60,
        'agents': ap.IntRange(1, 50),
        'ratio_dirty_cells': 20,
        'steps': 5000
    }
    sample = ap.Sample(parameters, n=5)
    exp = ap.Experiment(RoombaModel, sample, iterations=10)
    results1 = exp.run()
    results1.save()
    results1 = ap.DataDict.load('RoombaModel')
    print(results1.reporters, '\n\n')

    # DATA SUMMARY
    averageCellsCleaned = sum(results1.reporters['cleaned_cells']) / results1.reporters['cleaned_cells'].__len__()
    averageMinMoves = sum(results1.reporters['min_moves']) / results1.reporters['min_moves'].__len__()
    averageMaxMoves = sum(results1.reporters['max_moves']) / results1.reporters['max_moves'].__len__()
    print('AVERAGE DIRTY CELLS REMAINING => ', averageCellsCleaned)
    print('AVERAGE MIN MOVEMENTS => ', averageMinMoves)
    print('AVERAGE MAX MOVEMENTS => ', averageMaxMoves)
    #     print('TOTAL_STEPS', results1.reporters['total_steps'])
    print('\n\n')

# RUN ALL SIMULATIONS
print('\n \t -- EXPERIMENTOS CON AGENTES DE 1 A 20 -- \n')
runSimulation_1()
runSimulation_2()
print('\n \t -- EXPERIMENTOS CON AGENTES DE 1 A 50 -- \n')
runSimulation_3()
runSimulation_4()