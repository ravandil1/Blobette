import pygame
from settings import *
from level import Level
from player import Player
from UI import UI
from menu import Main, Tutorial, Complete, Again, Over






class Game:
    def __init__(self, surface):
        self.surface = surface
        #starting level
        self.current_level = 0
        #starting life
        self.current_health = 3
        #game states
        self.level = Level(self.current_level, self.surface, self.level_complete, self.try_again)
        self.main = Main(self.surface, self.tutorial, self.new_game)
        self.tutorial = Tutorial(self.surface, self.main_menu, self.start_game)
        self.again = Again(self.surface, self.start_game, self.main_menu, self.fail)
        self.over = Over(self.surface, self.start_game, self.main_menu, self.new_game)
        self.complete = Complete(self.surface, self.start_game, self.main_menu, self.change_level)
        #starting state
        self.status = 'menu'
    
        #audio
        self.bg_music = pygame.mixer.music.load('./audio/bg_music.wav')
        pygame.mixer.music.set_volume(0.1)

        #UI
        self.ui = UI(self.surface, self.current_health)
    
    def main_menu(self):
        self.status = 'menu'
    
    def tutorial(self):
        self.status = 'tutorial'

    def level_complete(self):
        self.status = 'complete'

    def start_game(self):
        self.status = 'run'
    
    def change_level(self):
        self.current_level += 1
        if self.current_level > 14:
                self.current_level = 0
                self.current_health = 3
                self.ui.update_health(self.surface, self.current_health)
        self.level.clear_groups()
        self.level.reset_level(self.current_level, self.surface, self.level_complete, self.try_again)
    
    def new_game(self):
        self.current_health = 3
        self.current_level = 0
        self.level.clear_groups()
        self.level.reset_level(self.current_level, self.surface, self.level_complete, self.try_again)
        self.ui.update_health(self.surface, self.current_health)

    def fail(self):
        self.current_health += -1
        self.level.reset_level(self.current_level, self.surface, self.level_complete, self.try_again)
        self.ui.update_health(self.surface, self.current_health)
        self.status = 'run'

    def try_again(self):
        if self.current_health <= 1:
            self.status = 'game over'
        else:
            self.status = 'try again'

    def run(self):
        if self.status == 'run':
            self.level.run()
            self.ui.update()
        elif self.status == 'menu':
            self.surface.fill('black')
            self.main.update()
            pygame.mixer.music.stop()
        elif self.status == 'tutorial':   
            self.surface.fill('black')
            self.tutorial.update()
            pygame.mixer.music.play(loops = - 1)
        elif self.status == 'complete':
            self.surface.fill('black')
            self.complete.update()
        elif self.status == 'try again' and self.current_health > 0:
            self.surface.fill('black')
            self.again.update()
        elif self.status == 'game over':
            pygame.mixer.music.stop()
            self.surface.fill('black')
            self.over.update()