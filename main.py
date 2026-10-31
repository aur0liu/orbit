import json
import pygame

from physics import *
from gui     import *




#user input        
bodies = []
more = True
while more:

    sim_type = input("Would you like to choose a default system or create a custom system? (any key for default, c for custom) ")

    if sim_type == 'c':
        bodyType = input("Would you like to choose a default body or create a custom body? (any key for default, c for custom) ")

        if bodyType == 'c':
            name = input("Name your body: ")
            mass = input("Input mass: ")
            x = float(input("Input x position: "))
            y = float(input("Input y position: "))
            radius = input("Input radius: ")
            colour = input("Input colour: ") #need input validation

            body = Body(name, mass, x, y, 0, 0, radius, 50, colour)

        else:
            print("Default bodies:")
            with open("default_data.json", "r") as f:
                default_data = json.load(f)
                print(default_data)

            i = 1
            for body in default_data['bodies']:
                print(f'{i}. {body['name']} (mass = {body['mass']}, radius = {body['radius']})')
                i += 1

            chosen_index = int(input("Enter number of chosen body: "))
            chosen_body = default_data['bodies'][chosen_index - 1]
            print(chosen_body)

            x = float(input("Input x position: "))
            y = float(input("Input y position: "))

            body = Body(chosen_body['name'], 
                chosen_body['mass'],
                x,y,
                0,0,50,50,
                chosen_body['colour']
            )
            print(body.mass, body.name)

        bodies.append(body)

        continu = input("Would you like to add another body y/n? ")

        if continu == "n":
            more = False

        else:
            more = True

    else:
        with open("default_data.json", "r") as f:
            default_data = json.load(f)

        i = 1
        for system in default_data['systems']:
            print(f'#{i} {system['name']}')

            for body in system['bodies']:
                print(f'    - {body['name']}, initial position = [{body['x']}, {body['y']}]')

            i += 1
            
        chosen_index = int(input("Enter number of chosen system: "))
        chosen_system = default_data['systems'][chosen_index - 1]

        for body in chosen_system['bodies']:   

            corresponding_body = default_data['bodies'][body['name']]

            next_body = Body(body['name'], 
                corresponding_body['mass'],
                body['x'],body['y'],
                0,0,
                corresponding_body['radius'],
                50,
                corresponding_body['colour']
            )

            print(next_body)

            bodies.append(next_body)


        more = False


#initialise pygame and create window
window = init_pygame()

main_menu(window)


#build and format data
bodies = initial_velocity(bodies, G)

#window loop
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            quit()

    start_index = 0

  

    for body in bodies: 

        euler_gravitation(body, bodies, G, dt)




    pygame.display.flip()
            