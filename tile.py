import pygame
from support import import_folder

class Tile(pygame.sprite.Sprite):
    def __init__(self,size,x,y):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.rect = self.image.get_rect(topleft = (x,y))

class StaticTile(Tile):
    def __init__(self,size,x,y,surface):
        super().__init__(size,x,y)
        self.image = surface

class Key(StaticTile):
    def __init__(self,size,x,y):
        super().__init__(size,x,y,pygame.image.load('./graphics/Props/Keys/key.png').convert_alpha())
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft = (x,offset_y))

class Platform(StaticTile):
    def __init__(self,size,x,y, move_x, move_y):
        
        super().__init__(size,x,y,pygame.image.load('./graphics/Props/platform.png').convert_alpha())
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_x = move_x
        self.move_y = move_y
        self.direction = pygame.math.Vector2(1,1)

class Spikes(StaticTile):
    def __init__(self,size,x,y):
        super().__init__(size,x,y,pygame.image.load('./graphics/traps/spikes.png').convert_alpha())
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft = (x,offset_y))


class AnimatedTile(Tile):
    def __init__(self, size,x,y,path):
        super().__init__(size,x,y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
    
    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
    
    def update(self):
        self.animate()

class Door(AnimatedTile):
    def __init__(self,size,x,y,path):
        
        super().__init__(size,x,y,path)
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft = (x,offset_y))
    
    def animate(self, index):
        if self.frame_index > len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(index)]

    def update(self, index):
        self.animate(index)


    
    
        