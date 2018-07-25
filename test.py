import pygame, sys
from pygame.locals import *

white = 255, 255, 255
black = 0, 0, 0

pygame.init()

screen = pygame.display.set_mode((600, 500))
myfront = pygame.font.Font(None, 60)
textImage = myfront.render("Hello Pygame", True, black)

while True:
    for event in pygame.event.get():
        if event.type in (QUIT, KEYDOWN):
            sys.exit()
    screen.fill(white)
    screen.blit(textImage, (100, 100))
    pygame.display.update()