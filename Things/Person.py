import pygame
import math
import random

def polygon_for_line(point_1, point_2, width, smoothness=4):
    radius = float(width)/2
    if point_1[0] == point_2[0]:
        x_min = point_1[0]
        y_min = min(point_1[1], point_2[1])
        x_max = point_1[0]
        y_max = max(point_1[1], point_2[1])
        angle = math.pi/2
    else:
        if point_1[0] < point_2[0]:
            x_min = point_1[0]
            y_min = point_1[1]
            x_max = point_2[0]
            y_max = point_2[1]
        else:
            x_max = point_1[0]
            y_max = point_1[1]
            x_min = point_2[0]
            y_min = point_2[1]
        angle = math.atan((y_max-y_min)/(x_max-x_min))
    
    polygon = []
    
    angle_modifier = -math.pi/2
    for i in range(smoothness+1):
        polygon.append((x_max + radius * math.cos(angle + angle_modifier), y_max + radius * math.sin(angle + angle_modifier)))
        angle_modifier += math.pi/smoothness
    angle_modifier -= math.pi/smoothness
    for i in range(smoothness+1):
        polygon.append((x_min + radius * math.cos(angle + angle_modifier), y_min + radius * math.sin(angle + angle_modifier)))
        angle_modifier += math.pi/smoothness
    
    return polygon

class Person(object):
    def __init__(self, ListOfColors, surface, givenstats=[]):
        self.Alive = True
        self.Kids = []
        self.age = 0
        self.ListOfColors = ListOfColors
        self.surface = surface
        self.angle = 0
        
        self.heading = random.random() * 2 * math.pi
        self.velocity = 10 + random.random() * 10
        
        if len(givenstats) == 0:
            self.x = random.random() * 800
            self.y = random.random() * 800
            self.size = random.random() * 10 + 10
            self.height = random.random() * 5 + 5
        else:
            self.x = givenstats[0]
            self.y = givenstats[1]
            self.size = givenstats[2]
            self.height = givenstats[3]
        
        self.ListOfPoints = [polygon_for_line((0, 0), (0, 0), self.size, smoothness=3)]
    
    def statistics(self):
        return [self.Alive, self.Kids, self.age, self.x, self.y, self.size, self.height]
    
    def tick(self, person_stats, index):
        moveNormally = True
        for i in range(len(person_stats)):
            if i != index:
                if math.sqrt((person_stats[i][3] - self.x) * (person_stats[i][3] - self.x) + (person_stats[i][4] - self.y) * (person_stats[i][4] - self.y)) < float(self.size + person_stats[i][5]) / 2.0:
                    self.Alive = False
        
        if random.random() > 0.9:
            self.size += 1
            self.ListOfPoints = [polygon_for_line((0, 0), (0, 0), self.size, smoothness=3)]

        #motion script at the end
        if moveNormally:
            self.heading += (random.random() * 0.2 - 0.1)
            self.x += self.velocity * math.cos(self.heading)
            self.y -= self.velocity * math.sin(self.heading)
            
            if self.y - float(self.size) / 2.0 < 0:
                self.y = self.size - self.y
                self.heading = 0 - self.heading
            if self.x - float(self.size) / 2.0 < 0:
                self.x = self.size - self.x
                self.heading = math.pi - self.heading
            if self.y + float(self.size) / 2.0 > self.surface.get_height():
                self.y = 2 * self.surface.get_height() - self.y - self.size
                self.heading = 0 - self.heading
            if self.x + float(self.size) / 2.0 > self.surface.get_width():
                self.x = 2 * self.surface.get_width() - self.x - self.size
                self.heading = math.pi - self.heading
            self.age += 1
    
    def update_hitbox(self):
        self.hitbox = []
        for i in self.ListOfPoints: #for every shape in ListOfPoints
            polygon = []
            for j in i:
                point = (self.x+j[0]*math.cos(self.angle)-j[1]*math.sin(self.angle), 
                         self.y+j[0]*math.sin(self.angle)+j[1]*math.cos(self.angle))
                polygon.append(point) #in form [(x1, y1), (x2, y2), ...]
            self.hitbox.append(polygon)
    
    def draw(self):
        self.update_hitbox()
        for i in range(len(self.hitbox)): #for every shape in the hitbox
            pygame.draw.polygon(self.surface, self.ListOfColors[i], self.hitbox[i])