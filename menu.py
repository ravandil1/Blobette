import pygame
from settings import screen_width, screen_height

class Buttons:
    def __init__(self,surface,image,x,y, scale):
        self.surface = surface
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.click = False
        
    def draw(self):
        action = False
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.click == False:
                self.click = True
                action = True
        if pygame.mouse.get_pressed()[2] == 0:
            self.click = False


        self.surface.blit(self.image, (self.rect.x, self.rect.y))
        return action        

class Main:
    def __init__(self, surface, tutorial, reset):
        self.surface = surface
        self.tutorial = tutorial
        self.reset = reset
        self.start_img = pygame.image.load("./graphics/Buttons/Start/Start1.png").convert_alpha()
        self.start_button = Buttons(self.surface, self.start_img, 400, 200, 3)
        self.quit_img = pygame.image.load("./graphics/Buttons/Quit/Quit1.png").convert_alpha()
        self.quit_button = Buttons(self.surface, self.quit_img, 400, 240, 3)
        
    def draw(self):
        self.start_button.draw()
        self.quit_button.draw()
        if self.start_button.draw():
            self.reset()
            self.tutorial()
        elif self.quit_button.draw():
            pygame.quit()
    
    def update(self):
        self.draw()

class Tutorial:
    def __init__(self, surface, menu, start):
        self.surface = surface
        self.text = pygame.image.load("./graphics/Tutorial/tutorial.png")
        self.menu = menu
        self.start = start
        self.start_img = pygame.image.load("./graphics/Buttons/Start/Start1.png").convert_alpha()
        self.start_button = Buttons(self.surface, self.start_img, 200, 600, 3)
        self.menu_img = pygame.image.load("./graphics/Buttons/Main/Main1.png").convert_alpha()
        self.menu_button = Buttons(self.surface, self.menu_img, 600, 600, 3)

    def draw(self):
        self.surface.blit(self.text, (0, 0))
        self.start_button.draw()
        self.menu_button.draw()
        if self.start_button.draw():
            self.start()
        elif self.menu_button.draw():
            self.menu()

    def update(self):
        self.draw()

class Complete:
    def __init__(self, surface, start, menu, level):
        self.surface = surface
        self.font = pygame.font.Font('./font/Pixeltype.ttf', 50)
        self.complete_level = self.font.render('Level complete', False, 'White')
        self.start = start
        self.menu = menu
        self.level = level
        self.resume_img = pygame.image.load("./graphics/Buttons/Resume/Resume1.png").convert_alpha()
        self.resume_button = Buttons(self.surface, self.resume_img, 200, 400, 3)
        self.menu_img = pygame.image.load("./graphics/Buttons/Main/Main1.png").convert_alpha()
        self.menu_button = Buttons(self.surface, self.menu_img, 400, 400, 3)
        self.quit_img = pygame.image.load("./graphics/Buttons/Quit/Quit1.png").convert_alpha()
        self.quit_button = Buttons(self.surface, self.quit_img, 600, 400, 3)

    def draw(self):
        self.surface.blit(self.complete_level, (screen_width //2 - 150, screen_height // 2 - 50))
        self.resume_button.draw()
        self.menu_button.draw()
        self.quit_button.draw()
        if self.resume_button.draw():
            self.level()
            self.start()
        elif self.menu_button.draw():
            self.menu()
        elif self.quit_button.draw():
            pygame.quit()

    def update(self):
        self.draw()

class Again:
    def __init__(self, surface, start, menu, fail):
        self.surface = surface
        self.font = pygame.font.Font('./font/Pixeltype.ttf', 50)
        self.complete_level = self.font.render('Try again', False, 'White')
        self.start = start
        self.menu = menu
        self.fail = fail
        self.resume_img = pygame.image.load("./graphics/Buttons/Resume/Resume1.png").convert_alpha()
        self.resume_button = Buttons(self.surface, self.resume_img, 200, 400, 3)
        self.menu_img = pygame.image.load("./graphics/Buttons/Main/Main1.png").convert_alpha()
        self.menu_button = Buttons(self.surface, self.menu_img, 400, 400, 3)
        self.quit_img = pygame.image.load("./graphics/Buttons/Quit/Quit1.png").convert_alpha()
        self.quit_button = Buttons(self.surface, self.quit_img, 600, 400, 3)

    def draw(self):
        self.surface.blit(self.complete_level, (screen_width //2 - 150, screen_height // 2 - 50))
        self.resume_button.draw()
        self.menu_button.draw()
        self.quit_button.draw()
        if self.resume_button.draw():
            self.fail()
            self.start()
        elif self.menu_button.draw():
            self.menu()
        elif self.quit_button.draw():
            pygame.quit()

    def update(self):
        self.draw()

class Over:
    def __init__(self, surface, start, menu, reset):
        self.surface = surface
        self.font = pygame.font.Font('./font/Pixeltype.ttf', 50)
        self.complete_level = self.font.render('Game Over', False, 'White')
        self.start = start
        self.menu = menu
        self.reset = reset
        self.start_img = pygame.image.load("./graphics/Buttons/Start/Start1.png").convert_alpha()
        self.start_button = Buttons(self.surface, self.start_img, 200, 400, 3)
        self.menu_img = pygame.image.load("./graphics/Buttons/Main/Main1.png").convert_alpha()
        self.menu_button = Buttons(self.surface, self.menu_img, 400, 400, 3)
        self.quit_img = pygame.image.load("./graphics/Buttons/Quit/Quit1.png").convert_alpha()
        self.quit_button = Buttons(self.surface, self.quit_img, 600, 400, 3)

    def draw(self):
        self.surface.blit(self.complete_level, (screen_width //2 - 150, screen_height // 2 - 50))
        self.start_button.draw()
        self.menu_button.draw()
        self.quit_button.draw()
        if self.start_button.draw():
            self.reset()
            self.start()
            pygame.mixer.music.play(loops = - 1)
        elif self.menu_button.draw():
            self.menu()
        elif self.quit_button.draw():
            pygame.quit()

    def update(self):
        self.draw()