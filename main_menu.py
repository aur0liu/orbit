import pygame

from button_class import *
from new_sim import *



def main_menu(window, fps, clock):
    TITLE_FONT = pygame.font.Font("assets/font/Kanit-Black.ttf" , 100)
    TITLE_COLOUR = (255,255,255,1)
    BUTTON_FONT = pygame.font.Font("assets/font/Kanit-ExtraLight.ttf" , 25)
    BACKGROUND_COLOUR = (0,3,31,1)

    buttons = []
    new_sim_button = TextButton('new simulation', (200, 250), BUTTON_FONT, new_sim)
    buttons.append(new_sim_button)



    running = True
    while running:

        mouse_pos = pygame.mouse.get_pos()

        window.fill(BACKGROUND_COLOUR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.check_for_input(mouse_pos):
                        button.button_function(window, BACKGROUND_COLOUR)
           

            if event.type == pygame.MOUSEMOTION:
                for button in buttons: 
                    button.colour_change(mouse_pos)

            

        menu_title =  TITLE_FONT.render("ORBIT", True, TITLE_COLOUR)
        title_rect = menu_title.get_rect(topleft = (200,100))

        window.blit(menu_title, title_rect)
        window.blit(new_sim_button.display_text, new_sim_button.rect)

        pygame.display.update()

        clock.tick(fps)