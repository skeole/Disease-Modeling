import pygame
import copy

import Things.Plant as Plant
import Things.Predator as Predator
import Things.Prey as Prey

pygame.init()
gameDisplay = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
background_color = (255, 255, 255)

#plants, predators, prey
entity_types = [Plant.Plant, Predator.Predator, Prey.Prey]
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
numbers = [1, 0, 3]

list_of_entities = []
entity_statistics = []

for i in range(len(numbers)):
    list_of_entities.append([])
    entity_statistics.append([])
    for j in range(numbers[i]):
        list_of_entities[i].append(entity_types([colors[i]], gameDisplay))
        entity_statistics[i].append([])

def update_statistics():
    global entity_statistics
    for i in range(len(list_of_entities)): #for all the plants, then all the animals, then all the prey
        entity_statistics[i] = []
        for j in i:
            entity_statistics[i].append(copy.deepcopy(j.statistics()))

def tick():
    update_statistics()
    
    for i in range(len(list_of_entities)):
        for j in range(len(list_of_entities[i])):
            j.tick(entity_statistics, i, j)
    
    update_statistics() #who died and new entities
    
    for i in range(len(list_of_entities)):
        temp = []
        for j in range(len(list_of_entities[i])):
            if entity_statistics[i][j][0]:
                temp.append(list_of_entities[i][j])
            for k in entity_statistics[i][j][1]:
                temp.append(entity_types([colors[i]], gameDisplay, givenstats=k))
        list_of_entities[i] = temp.copy()
    
    run = True
    
    while(run):
        update_statistics()
        messages = []
        for i in range(len(list_of_entities)):
            for j in range(len(list_of_entities[i])):
                for k in entity_statistics[i][j][2]:
                    temp = copy.deepcopy(k)
                    temp.append(i)
                    temp.append(j)
                    messages.append(copy.deepcopy(temp)) #message = [entity_type, entity_number, [message_data], coming_from_type, coming_from_number]
        if len(messages) == 0:
            run = False
        else:
            for i in messages:
                list_of_entities[i[0], i[1]].tick(entity_statistics, i[0], i[1], message=i)

run = True
pause = False

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            pause = not pause
    
    if (not pause):
        
        tick()

    #draw everything
    gameDisplay.fill(background_color)
    
    for i in list_of_entities:
        for j in i:
            j.draw()
    
    pygame.display.update()
    clock.tick(25)

pygame.quit()