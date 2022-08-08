import math
import random
import Template

class Plant(Template.Template):
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
        temp = super().basic_statistics() #Alive, Kids, messages, age, x, y, size
        temp.append(self.height)
        temp.append(self.numFruit)
        return temp
    
    def tick(self, entity_stats, index1, index2, message=[]):
        self.sent_messages = []
        if len(message) == 0:
            if (random.random() > 0.95) and (self.numFruit < 4):
                self.numFruit += 1
            super().basic_tick(False) #if True, then move normally, if false, then just refulate size/age
            self.ListOfColors = self.initialColors
            self.ListOfPoints = [Template.polygon_for_line((0, 0), (0, 0), self.size, smoothness=self.smoothness)]
            for i in range(self.numFruit):
                self.ListOfColors.append((0, 0, 0))
                self.ListOfPoints.append(Template.polygon_for_line((self.size * math.cos(i / 2.0 * math.pi), self.size * math.sin(i / 2.0 * math.pi)), (self.size * math.cos(i / 2.0 * math.pi), self.size * math.sin(i / 2.0 * math.pi)), 5, smoothness=2))
        else:
            a = True
            for i in message:
                if a:
                    self.sent_messages.append(message[3], message[4], []) #sending the message
                    a = False