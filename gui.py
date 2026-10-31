#GUI-related stuff (game loops and button class)

import pygame


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


def get_font(size):
    font = pygame.font.SysFont('Arial', size)
    return font



def main_menu(window):
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
        
        
        mouse_pos = pygame.mouse.get_pos()

        menu_title = get_font(100).render("ORBIT", True, "TITLE_COLOUR")