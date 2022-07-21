import math
import random
import Things.Thing as Thing

class Predator(Thing.Thing):
    def __init__(self, ListOfColors, surface, givenstats=[]):
        super().__init__(ListOfColors, surface, givenstats)
        
        if len(givenstats) == 0:
            self.height = random.random() * 5 + 5
        else:
            self.height = givenstats[3]
    
    def statistics(self):
        temp = super().basic_statistics()
        temp.append(self.height)
        return temp
    
    def tick(self, plant_stats, predator_stats, prey_stats, index):
        super().basic_tick(True)