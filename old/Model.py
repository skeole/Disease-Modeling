import pygame
import math

import random
import Person

pygame.init()
gameDisplay = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
background_color = (255, 255, 255)

list_of_people = [];
infected = [];
positions = [];
for i in range(80):
    list_of_people.append(Person.Person([(0, 0, 0)], gameDisplay))
    if i == 0:
        list_of_people[i].transmissionfactor = 1
    else:
        list_of_people[i].transmissionfactor = 0
    infected.append(0)
    positions.append((0, 0))

run = True;
pause = False;

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            pause = not pause
    
    if (not pause):
        count = 0
        for dot in list_of_people:
            dot.move()
            infected[count] = dot.transmissionfactor
            positions[count] = (dot.x, dot.y)
            dot.ListOfColors[0] = (0, dot.transmissionfactor * 255, 0)
            count += 1
        count = 0
        for dot in list_of_people:
            dot.update_with_infections(infected, positions, count)
            count += 1
    
    gameDisplay.fill(background_color)
    for dot in list_of_people:
        dot.draw()

    pygame.display.update()
    clock.tick(40)

pygame.quit()
