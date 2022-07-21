import math
import random
import Things.Thing as Thing

class Plant(Thing.Thing):
    def __init__(self, ListOfColors, surface, givenstats=[]):
        super().__init__(ListOfColors, surface, givenstats)
        
        if len(givenstats) == 0:
            self.height = random.random() * 5 + 5
        else:
            self.height = givenstats[3]
        
        self.numFruit = 0
        for i in range(3):
            if random.random() > 0.5:
                self.numFruit += 1
    
    def statistics(self):
        temp = super().basic_statistics() #Alive, Kids, age, x, y, size
        temp.append(self.height)
        temp.append(self.numFruit)
        return temp
    
    def tick(self, plant_stats, predator_stats, prey_stats, index):
        if (random.random() > 0.95) and (self.numFruit < 4):
            self.numFruit += 1
        for i in prey_stats:
            if (Thing.distance(self.statistics(), i) < 20) and (self.numFruit > 0):
                self.numFruit -= 1
        
        super().basic_tick(False)
        
        self.ListOfColors = self.initialColors
        self.ListOfPoints = [Thing.polygon_for_line((0, 0), (0, 0), self.size, smoothness=self.smoothness)]
        for i in range(self.numFruit):
            self.ListOfColors.append((0, 0, 0))
            self.ListOfPoints.append(Thing.polygon_for_line((self.size * math.cos(i / 2.0 * math.pi), self.size * math.sin(i / 2.0 * math.pi)), (self.size * math.cos(i / 2.0 * math.pi), self.size * math.sin(i / 2.0 * math.pi)), 5, smoothness=2))