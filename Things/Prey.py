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
        
    def statistics(self):
        temp = super().basic_statistics()
        temp.append(self.height)
        return temp
    
    def tick(self, plant_stats, predator_stats, prey_stats, index):
        self.Kids = []
        moveNormally = True
        if random.random() > 0.9999:
            self.Kids = [[]]
        for i in plant_stats:
            if (Thing.distance(self.statistics(), i) < 80) and (i[7] > 0):
                temp = 0
                self.heading = Thing.direction(self.statistics(), i)
                for j in range(index):
                    if Thing.distance(prey_stats[j], i) < 20:
                        temp += 1
                if temp < i[7] and Thing.distance(self.statistics(), i) < 20:
                    moveNormally = False
                    self.Alive = False
        
        #motion script at the end so we can decide how we want to change velocity/angle
        super().basic_tick(moveNormally)