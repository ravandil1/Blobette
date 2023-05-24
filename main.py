import pygame
import sys
from game import Game
from settings import *


# Pygame setup
pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Blobette")
clock = pygame.time.Clock()
game = Game(screen)


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()
    
    game.run()
       
    pygame.display.update()
    clock.tick(60)

    
    


