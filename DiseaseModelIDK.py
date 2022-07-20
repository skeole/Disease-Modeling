import pygame
import copy

import Things.Person as Person

pygame.init()
gameDisplay = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
background_color = (255, 255, 255)

person_color = (128, 128, 128)
number_of_people = 100
list_of_people = []
person_statistics = []

for i in range(number_of_people):
    list_of_people.append(Person.Person([person_color], gameDisplay))
    person_statistics.append([])

def update_statistics():
    global person_statistics
    person_statistics = []
    for i in list_of_people:
        person_statistics.append(copy.deepcopy(i.statistics()))

def tick():
    global list_of_people
    for i in range(len(list_of_people)):
        list_of_people[i].tick(person_statistics, i)

    update_statistics()
    
    temp = []
    for i in range(len(list_of_people)):
        if person_statistics[i][0]:
            temp.append(list_of_people[i])
        for j in person_statistics[i][1]:
            temp.append(Person.Person([person_color], gameDisplay, givenstats=j))
    list_of_people = temp.copy()

run = True
pause = False

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            pause = not pause
    
    if (not pause):
        
        #update stats (position, health, age, idrc)
        update_statistics()
        #move, have babies, die
        tick()

    #draw everything
    gameDisplay.fill(background_color)
    
    for i in list_of_people:
        i.draw()

    pygame.display.update()
    clock.tick(30)

pygame.quit()