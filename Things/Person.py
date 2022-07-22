import math
import random
import Things.Thing as Thing

class Person(Thing.Thing):
    def __init__(self, ListOfColors, surface, name="G", givenstats=[]):
        super().__init__(ListOfColors, surface, givenstats)
        
        self.velocity = 10 + random.random() * 10
        
        self.name = name
        self.height = 0
        
    def statistics(self):
        temp = super().basic_statistics() #Alive, Kids, age, x, y, size
        temp.append(self.height)
        temp.append(self.name)
        return temp
    
    def tick(self, person_stats, index):
        moveNormally = True
        for i in range(len(person_stats)):
            if i != index:
                if Thing.distance(person_stats[i], self.statistics()) < 0:
                    if (self.size < person_stats[i][5]) or ((self.size == person_stats[i][5]) and (index < i)):
                        self.Alive = False
                    else:
                        self.size += 0.1 * person_stats[i][5]
        
        if random.random() > 0.9:
            self.size += 1
            self.smoothness = min(max(int(self.size / 5.0) - 1, 2), 4)
            self.ListOfPoints = [Thing.polygon_for_line((0, 0), (0, 0), self.size, smoothness=self.smoothness)]

        #motion script at the end so we can decide how we want to change velocity/angle
        super().basic_tick(moveNormally)