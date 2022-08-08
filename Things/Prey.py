import math
import random
import Things.Thing as Thing

class Prey(Thing.Thing):
    def __init__(self, ListOfColors, surface, givenstats=[]):
        super().__init__(ListOfColors, surface, givenstats)
        
        self.velocity = 10 + random.random() * 10
        
        self.maxAge = 200 + random.random() * 200
        if len(givenstats) == 0:
            self.height = random.random() * 5 + 5
        else:
            self.height = givenstats[3]
        
        self.nearbyplants = []
        
    def statistics(self):
        temp = super().basic_statistics()
        temp.append(self.height)
        temp.append(self.nearbyplants)
        return temp
    
    def tick(self, plant_stats, predator_stats, prey_stats, index):
        self.Kids = []
        moveNormally = True
        if random.random() > 0.998:
            self.Kids = [[]]
        self.nearbyplants = []
        for i in range(len(plant_stats)):
            if Thing.distance(self.statistics(), plant_stats[i]) < 240:
                self.heading = Thing.direction(self.statistics(), plant_stats[i])
            if Thing.distance(self.statistics(), plant_stats[i]) < 20:
                self.nearbyplants.append(i)
            if index in plant_stats[i][8]:
                moveNormally = False
                self.Alive = False
        
        #motion script at the end so we can decide how we want to change velocity/angle
        super().basic_tick(moveNormally)