import pygame
import copy

import Things.Thing as Thing
import Things.Person as Person

names = ['Jacob', 'Emily', 'Michael', 'Madison', 'Joshua', 'Emma', 'Matthew', 'Olivia', 'Daniel', 'Hannah', 'Christopher', 'Abigail', 'Andrew', 'Isabella', 'Ethan', 'Samantha', 'Joseph', 'Elizabeth', 'William', 'Ashley', 'Anthony', 'Alexis', 'David', 'Sarah', 'Alexander', 'Sophia', 'Nicholas', 'Alyssa', 'Ryan', 'Grace', 'Tyler', 'Ava', 'James', 'Taylor', 'John', 'Brianna', 'Jonathan', 'Lauren', 'Noah', 'Chloe', 'Brandon', 'Natalie', 'Christian', 'Kayla', 'Dylan', 'Jessica', 'Samuel', 'Anna', 'Benjamin', 'Victoria', 'Nathan', 'Mia', 'Zachary', 'Hailey', 'Logan', 'Sydney', 'Justin', 'Jasmine', 'Gabriel', 'Julia', 'Jose', 'Morgan', 'Austin', 'Destiny', 'Kevin', 'Rachel', 'Elijah', 'Ella', 'Caleb', 'Kaitlyn', 'Robert', 'Megan', 'Thomas', 'Katherine', 'Jordan', 'Savannah', 'Cameron', 'Jennifer', 'Jack', 'Alexandra', 'Hunter', 'Allison', 'Jackson', 'Haley', 'Angel', 'Maria', 'Isaiah', 'Kaylee', 'Evan', 'Lily', 'Isaac', 'Makayla', 'Luke', 'Brooke', 'Tony', 'Nicole', 'Colin', 'Mackenzie', 'Eddie', 'Addison', 'Shaan']
pygame.init()
gameDisplay = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
background_color = (255, 255, 255)

person_color = (128, 128, 128)
number_of_people = len(names)
list_of_people = []
person_statistics = []

for i in range(number_of_people):
    list_of_people.append(Person.Person([person_color], gameDisplay, name=names[i]))
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

t = True
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

    if t and len(person_statistics) == 1:
        print(person_statistics[0][7])
        t = False
    
    pygame.display.update()
    clock.tick(80)

pygame.quit()