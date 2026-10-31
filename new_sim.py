import pygame

from physics import *

def new_sim(window, BACKGROUND_COLOUR):
    running = True
    while running:

        window.fill(BACKGROUND_COLOUR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()


        pygame.display.update()

        


def sim():
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