#GUI-related stuff (game loops and button class)

import pygame


class TextButton:
    def __init__(self, button_text, pos, font, button_function):
        self.x = pos[0]
        self.y = pos[1]   
  
        self.text = button_text
        

        self.colours = {
            "normal"  : (230,230,230,1),
            "hover"   : (188, 145, 231, 1),
            "pressed" : (174, 229, 235, 1),
        } 

        self.font = font
        self.display_text = self.font.render(self.text, True, self.colours['normal'])
        self.rect = self.display_text.get_rect(topleft = (self.x, self.y))
        
        self.is_clicked = False

        self.button_function = button_function



    def colour_change(self, mouse_pos):
        if mouse_pos[0] in range(self.rect.left, self.rect.right) and mouse_pos[1] in range(self.rect.top, self.rect.bottom):
            if self.is_clicked == True:
                self.display_text = self.font.render(self.text, True, self.colours['pressed'])
            else:
                self.display_text = self.font.render(self.text, True, self.colours['hover'])
        else:
            self.display_text = self.font.render(self.text, True, self.colours['normal'])


    def check_for_input(self, mouse_pos):
        if mouse_pos[0] in range(self.rect.left, self.rect.right) and mouse_pos[1] in range(self.rect.top, self.rect.bottom):
            return True
        else:
            return False

    




