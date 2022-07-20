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
    ListOfPoints = []
    hitbox = []
    x = 0
    y = 0
    angle = 0
    
    heading = 0
    velocity = 10
    transmissionfactor = 1.0 #decreases significantly if already infected
    receivingfactor = 0.8 #decreases significantly if already infected
    #transmission %: transmissionfactor1 * transmissionfactor2 * severity?
    already_infected = False;
    currently_infected = False;
    percent_immunity = 0; #decreases based on time_active
    time_active = 50; #will be a %-based system; will depend on vaccine/infected, etc.
    severity = 0; #how likely to have symptoms
    health = 100;
    
    def __init__(self, ListOfColors, surface, border_width=0): #should be a nested list
                            #ex. [[(2, 3), (4, 5)], [(6, 7), (8, 9)]] -> 2 objects with points
                            #2, 3 and 4, 5 for object 1 and 6, 7 and 8, 9 for object 2
        self.ListOfPoints = [polygon_for_line((0, 0), (0, 0), 15, smoothness=3)]
        self.ListOfColors = ListOfColors
        self.surface = surface
        self.border_width = border_width
        self.x = random.random() * surface.get_width()
        self.y = random.random() * surface.get_height()
        self.heading = random.random() * 2 * math.pi
        self.velocity = 10 + 10 * random.random()
    
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
            pygame.draw.polygon(self.surface, self.ListOfColors[i], self.hitbox[i], width=self.border_width)
    
    def move(self):
        self.time_active -= 1;
        self.x += math.cos(self.heading) * self.velocity;
        self.y -= math.sin(self.heading) * self.velocity;
        
        if self.y - 7.5 < 0:
            self.y = 15 - self.y
            self.heading = 0 - self.heading
            self.heading = math.pi * (1 + random.random())
            self.velocity = 10 + 10 * random.random()
        if self.x - 7.5 < 0:
            self.x = 15 - self.x
            self.heading = math.pi - self.heading
            self.heading = math.pi * (1.5 + random.random())
            self.velocity = 10 + 10 * random.random()
        if self.y + 7.5 > self.surface.get_height():
            self.y = 2 * self.surface.get_height() - self.y - 15
            self.heading = 0 - self.heading
            self.heading = math.pi * (random.random())
            self.velocity = 10 + 10 * random.random()
        if self.x + 7.5 > self.surface.get_width():
            self.x = 2 * self.surface.get_width() - self.x - 15
            self.heading = math.pi - self.heading
            self.heading = math.pi * (0.5 + random.random())
            self.velocity = 10 + 10 * random.random()
        # if within list_of_coordinates then chance to be infected is GGG
    
    def update_with_infections(self, infected, positions, count):
        x = 0
        for point in positions:
            if x != count:
                if infected[x] / ((positions[x][0] - self.x) * (positions[x][0] - self.x) + (positions[x][1] - self.y) * (positions[x][1] - self.y)) * self.receivingfactor > 0.001:
                    self.currently_infected = True
                    self.transmissionfactor = 1.0
            x += 1
        self.transmissionfactor *= 0.9