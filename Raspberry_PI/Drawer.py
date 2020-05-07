import pygame
from constants import *

class Drawer():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Image_Width, Image_Height))
        pygame.display.set_caption('trainer')
        pygame.display.update()

    def draw_screen(self,np_image, angle, speed):
        self.screen.fill(WHITE)
        # frame
        self.draw_image(self.screen, np_image, Image_Width, Image_Height)
        # angle
        angle = "%5.2f" % (angle)
        self.draw_text(self.screen, angle, WHITE, 60, Image_Width//2 -60 , 0)
        # speed
        #draw_text(screen, speed, WHITE, 40, Image_Width // 2 - 40, 40)
        pygame.display.update()
        return

    def draw_image(self,screen,  np_image, width, height, x=0 , y=0, format='RGB'):
        pygame_image = pygame.image.frombuffer(np_image, (width, height), format)
        screen.blit(pygame_image, (x, y))
        return

    def draw_text(self,screen, text, color, font_size = 15, x=0 , y=0):
        text = str(text)
        font = pygame.font.Font(None, font_size)
        text_img = font.render(text, True, color)
        screen.blit(text_img, (x , y))
        return