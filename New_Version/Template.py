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

def distance(thing1, thing2): #returns distance between them - not distance between centers
    return math.sqrt((thing1[3] - thing2[3]) * (thing1[3] - thing2[3]) + (thing1[4] - thing2[4]) * (thing1[4] - thing2[4])) - 0.5 * (thing1[5] + thing2[5])

def direction(thing1, thing2): #direction from thing1 to thing2
    if thing1[3] == thing2[3]:
        if thing1[4] < thing2[4]:
            return 3.0 * math.pi / 2.0
        else:
            return math.pi / 2.0
    angle = 0
    if thing1[3] > thing2[3]:
        angle = math.pi
    angle -= math.atan((thing1[4] - thing2[4]) / (thing1[3] - thing2[3]))
    return angle

class Template(object):
    def __init__(self, ListOfColors, surface, givenstats=[]):
        self.Alive = True
        self.Kids = []
        self.sent_messages = []
        self.age = 0
        
        self.initialColors = ListOfColors.copy()
        self.ListOfColors = ListOfColors
        self.surface = surface
        self.angle = 0
        
        self.heading = random.random() * 2 * math.pi
        self.velocity = 0
        
        if len(givenstats) == 0:
            self.x = surface.get_width() * (0.1 + random.random() * 0.8)
            self.y = surface.get_height() * (0.1 + random.random() * 0.8)
            self.size = random.random() * 10 + 20
        else:
            self.x = givenstats[0]
            self.y = givenstats[1]
            self.size = givenstats[2]
        
        self.smoothness = min(max(int(self.size / 5.0) - 1, 2), 4)
        
        self.ListOfPoints = [polygon_for_line((0, 0), (0, 0), self.size, smoothness=self.smoothness)]
    
    def basic_statistics(self):
        return [self.Alive, self.Kids, self.sent_messages, self.age, self.x, self.y, self.size]
    
    def basic_tick(self, moveNormally):
        self.size = max(min(self.size, self.surface.get_height() / 2.0), 0)
        if self.velocity != 0:
            if moveNormally:
                self.heading += (random.random() * 0.4 - 0.2)
            
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