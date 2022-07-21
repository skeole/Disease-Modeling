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

def distance(thing1, thing2):
    return math.sqrt((thing1[3] - thing2[3]) * (thing1[3] - thing2[3]) + (thing1[4] - thing2[4]) * (thing1[4] - thing2[4])) - 0.5 * (thing1[5] + thing2[5])

class Predator(object):
    def __init__(self, ListOfColors, surface, givenstats=[]):
        self.Alive = True
        self.Kids = []
        self.age = 0
        self.ListOfColors = ListOfColors
        self.surface = surface
        self.angle = 0
        
        if len(givenstats) == 0:
            self.x = surface.get_width() * (0.1 + random.random() * 0.8)
            self.y = surface.get_height() * (0.1 + random.random() * 0.8)
            self.size = random.random() * 5 + 5
            self.height = random.random() * 5 + 5
        else:
            self.x = givenstats[0]
            self.y = givenstats[1]
            self.size = givenstats[2]
            self.height = givenstats[3]
        
        self.ListOfPoints = [polygon_for_line((0, 0), (0, 0), self.size, smoothness=2)]
    
    def statistics(self):
        return [self.Alive, self.Kids, self.age, self.x, self.y, self.size, self.height, self.numFruit]
    
    def tick(self, plant_stats, predator_stats, prey_stats, index):
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