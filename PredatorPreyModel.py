import pygame
import copy

import Things.Plant as Plant
import Things.Predator as Predator
import Things.Prey as Prey

pygame.init()
gameDisplay = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
background_color = (255, 255, 255)

plant_color = (255, 0, 0)
number_of_plants = 2
list_of_plants = []
plant_statistics = []

predator_color = (0, 255, 0)
number_of_predators = 0
list_of_predators = []
predator_statistics = []

prey_color = (0, 0, 255)
number_of_prey = 20
list_of_prey = []
prey_statistics = []

for i in range(number_of_plants):
    list_of_plants.append(Plant.Plant([plant_color], gameDisplay))
    plant_statistics.append([])

for i in range(number_of_predators):
    list_of_predators.append(Predator.Predator([predator_color], gameDisplay))
    predator_statistics.append([])

for i in range(number_of_prey):
    list_of_prey.append(Prey.Prey([prey_color], gameDisplay))
    prey_statistics.append([])

def update_statistics():
    for i in range(len(list_of_plants)):
        plant_statistics[i] = copy.deepcopy(list_of_plants[i].statistics())
    for i in range(len(list_of_predators)):
        predator_statistics[i] = copy.deepcopy(list_of_predators[i].statistics())
    for i in range(len(list_of_prey)):
        prey_statistics[i] = copy.deepcopy(list_of_prey[i].statistics())

def tick():
    global list_of_plants, list_of_predators, list_of_prey
    for i in range(len(list_of_plants)):
        list_of_plants[i].tick(plant_statistics, predator_statistics, prey_statistics, i)

    for i in range(len(list_of_predators)):
        list_of_predators[i].tick(plant_statistics, predator_statistics, prey_statistics, i)

    for i in range(len(list_of_prey)):
        list_of_prey[i].tick(plant_statistics, predator_statistics, prey_statistics, i)

    update_statistics()
    
    temp = []
    for i in range(len(list_of_plants)):
        if plant_statistics[i][0]: #0 = if plant is alive
            temp.append(list_of_plants[i])
        for j in plant_statistics[i][1]:
            temp.append(Plant.Plant([plant_color], gameDisplay, givenstats=j))
            plant_statistics.append([])
    list_of_plants = temp.copy()
    
    temp = []
    for i in range(len(list_of_predators)):
        if predator_statistics[i][0]: #0 = if plant is alive
            temp.append(list_of_predators[i])
        for j in predator_statistics[i][1]:
            temp.append(Predator.Predator([predator_color], gameDisplay, givenstats=j))
            predator_statistics.append([])
    list_of_predators = temp.copy()
    
    temp = []
    for i in range(len(list_of_prey)):
        if prey_statistics[i][0]: #0 = if plant is alive
            temp.append(list_of_prey[i])
        for j in prey_statistics[i][1]:
            temp.append(Prey.Prey([prey_color], gameDisplay, givenstats=j))
            prey_statistics.append([])
    list_of_prey = temp.copy()

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
    
    for i in list_of_plants:
        i.draw()
    
    for i in list_of_predators:
        i.draw()
    
    for i in list_of_prey:
        i.draw()

    pygame.display.update()
    clock.tick(10)

pygame.quit()