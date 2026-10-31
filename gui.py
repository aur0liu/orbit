#GUI-related stuff (game loops and button class)

import pygame


def init_pygame():
    #initialise pygame
    pygame.init()
    pygame.font.init()

    #create window
    pygame.display.set_caption("ORBIT")
    display = (800, 800)
    window = pygame.display.set_mode(display)

    return window



class TextButton:
    def __init__(self, button_text, pos, font):
        self.x = pos[0]
        self.y = pos[1]   
  
        self.text = button_text
        self.rect = self.text.get_rect(center = (self.x, self.y))

        self.colours = {
            "normal"  : "",
            "hover"   : "",
            "pressed" : "",
        } 

        self.font = font
        self.display_text = self.font.render(self.text, True, self.colours['normal'])

        self.is_clicked = False



    def colour_change(self, mouse_pos):
        if mouse_pos[0] in range(self.rect.left, self.rect.right) and mouse_pos[1] in range(self.rect.top, self.rect.bottom):
            if self.is_clicked == True:
                self.display_text = self.font.render(self.text, True, self.colours['pressed'])
            else:
                self.display_text = self.font.render(self.text, True, self.colours['hover'])




def main_menu(window):
    TITLE_FONT = pygame.font.Font("assets/font/Kanit-Black.ttf" , 100)
    TITLE_COLOUR = (0,0,0,0)

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
        
        
        #mouse_pos = pygame.mouse.get_pos()

        menu_title =  TITLE_FONT.render("ORBIT", True, TITLE_COLOUR)
        title_rect = menu_title.get_rect(center = (400,400))

        window.blit(menu_title, title_rect)