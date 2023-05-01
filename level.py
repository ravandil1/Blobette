import pygame
from tile import Tile, StaticTile, Key, Door, Platform, Spikes
from settings import tile_size, screen_width, screen_height
from player import Player
from support import import_csv_layout, import_cut_graphics



class Level:
    def __init__(self,current_level,surface, level_complete, try_again):
       self.reset_level(current_level,surface, level_complete, try_again)
        

    def reset_level(self,current_level,surface, level_complete, try_again):
        # general setup
        self.display_surface = surface
        self.current_level = current_level
        self.level_data  = {
                            'terrain': f'./levels/{current_level}/level_{current_level}_Terrain.csv',
                            'doors': f'./levels/{current_level}/level_{current_level}_Doors.csv',
                            'keys': f'./levels/{current_level}/level_{current_level}_Keys.csv',
                            'player': f'./levels/{current_level}/level_{current_level}_Player.csv',
                            'stop': f'./levels/{current_level}//level_{current_level}_Stop.csv',
                            'platform': f'./levels/{current_level}/level_{current_level}_Platform.csv',
                            'elevator': f'./levels/{current_level}/level_{current_level}_Elevator.csv',
                            'spikes': f'./levels/{current_level}/level_{current_level}_Spikes.csv'}
        self.level_complete = level_complete
        self.try_again = try_again
        
        # audio setup
        self.death_sound = pygame.mixer.Sound('./audio/sfx/death.wav')
        self.open_sound = pygame.mixer.Sound('./audio/sfx/dooropen.wav')

        #background setup
        self.background = pygame.image.load('./graphics/Backgrounds/background.png')
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
        
        try:
            #player setup
            player_layout = import_csv_layout(self.level_data['player'])
            self.player = pygame.sprite.GroupSingle()
            self.player_setup(player_layout)
        except:
            pass

        try:
            #terrain setup
            self.terrain_group = pygame.sprite.Group()
            terrain_layout = import_csv_layout(self.level_data['terrain'])
            self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain', self.terrain_group)
        except:
            pass

        try:
            #platform setup
            self.platform_group = pygame.sprite.Group()
            platform_layout = import_csv_layout(self.level_data['platform'])
            self.platform_sprites = self.create_tile_group(platform_layout, 'platform', self.platform_group)
        except:
            pass

        try:
            #elevator setup
            self.elevator_group = pygame.sprite.Group()
            elevator_layout = import_csv_layout(self.level_data['elevator'])
            self.elevator_sprites = self.create_tile_group(elevator_layout, 'elevator', self.elevator_group)
        except:
            pass

        try:
            #constraint setup
            self.constraint_group = pygame.sprite.Group()
            constraint_layout = import_csv_layout(self.level_data['stop'])
            self.constraint_sprites = self.create_tile_group(constraint_layout, 'stop', self.constraint_group)
        except:
            pass

        try:
            #keys setup
            self.key_group = pygame.sprite.Group()
            keys_layout = import_csv_layout(self.level_data['keys'])
            self.keys_sprites = self.create_tile_group(keys_layout, 'keys', self.key_group)
            self.key_index = 0
        except:
            pass

        try:
            #door setup
            self.door_group = pygame.sprite.Group()
            doors_layout = import_csv_layout(self.level_data['doors'])
            self.door_sprites = self.create_tile_group(doors_layout, 'doors', self.door_group)
        except:
            pass
        try:
            #spikes setup
            self.spikes_group = pygame.sprite.Group()
            spikes_layout = import_csv_layout(self.level_data['spikes'])
            self.spikes_sprites = self.create_tile_group(spikes_layout, 'spikes', self.spikes_group)
        except:
            pass
    
    def clear_groups(self):
        self.player.empty()
        self.terrain_group.empty()
        self.platform_group.empty()
        self.elevator_group.empty()
        self.constraint_group.empty()
        self.key_group.empty()
        self.door_group.empty()
        self.spikes_group.empty()
    
    def create_tile_group(self, layout,type, sprite_group):
        for row_index, row in enumerate(layout):
            for col_index, value in enumerate(row):
                if value != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size
                    
                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('./graphics/terrain/Tiles.png')
                        tile_surface = terrain_tile_list[int(value)]
                        sprite = StaticTile(tile_size,x,y, tile_surface)
                    
                    elif type == 'platform':
                        sprite = Platform(tile_size,x,y, 1, 0)

                    elif type == 'elevator':
                        sprite = Platform(tile_size,x,y, 0, 1)
                    
                    elif type == 'stop':
                        sprite = Tile(tile_size,x,y)

                    elif type == 'keys':
                        sprite = Key(tile_size,x,y)

                    elif type == 'doors':
                        sprite = Door(tile_size,x,y, './graphics/props/door')

                    elif type == 'spikes':
                        sprite = Spikes(tile_size,x,y)
                            
                    sprite_group.add(sprite)
            
        
        return sprite_group

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, value in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if value == '0':
                    sprite = Player((x,y),self.display_surface)
                    self.player.add(sprite)

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x
        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right   
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.rect.y += player.direction.y
        player.apply_gravity()
        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if  player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                    player.direction.x = 0

                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
            
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        

    def key_interaction(self):
        collided_keys = pygame.sprite.spritecollide(self.player.sprite, self.keys_sprites, True)
        if collided_keys:
            self.open_sound.play()
            self.key_index += 1

    def door_interaction(self):
        collided_doors = pygame.sprite.spritecollide(self.player.sprite, self.door_sprites, False)
        if collided_doors and self.key_index == 1:
            self.key_index = 0
            self.level_complete()

    def platform_movement(self):
        for platform in self.platform_sprites.sprites():
            platform.rect.x += platform.direction.x * platform.move_x

    def elevator_movement(self):
        for elevator in self.elevator_sprites.sprites():
            elevator.rect.y += elevator.direction.y * elevator.move_y

    def platform_collision(self):
        player = self.player.sprite
        for platform in self.platform_sprites.sprites():
            if pygame.sprite.spritecollide(platform, self.constraint_sprites, False):
                platform.direction.x *= -1
            
            elif platform.rect.colliderect(player.rect):
                if  player.direction.y > 0:
                    player.rect.bottom = platform.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                    player.direction.x = platform.direction.x
                
                elif player.direction.y < 0:
                    player.rect.top = platform.rect.bottom
                    player.direction.y = 0

    def elevator_collision(self):
        player = self.player.sprite
        for elevator in self.elevator_sprites.sprites():
            if pygame.sprite.spritecollide(elevator, self.constraint_sprites, False):
                elevator.direction.y *= -1
            
            elif elevator.rect.colliderect(player.rect):
                if  player.direction.y > 0:
                    player.rect.bottom = elevator.rect.top
                    player.on_ground = True
                    player.direction.y = elevator.direction.y
                    player.direction.x = 0
                
                elif player.direction.y < 0:
                    player.rect.top = elevator.rect.bottom
                    player.direction.y = 0


    def spikes_collision(self):
        player = self.player.sprite
        for spike in self.spikes_sprites.sprites():
            if spike.rect.colliderect(player.rect):
                self.death_sound.play()
                self.try_again()

    
    def check_death(self):
        if self.player.sprite.rect.top > screen_height:
                self.death_sound.play()
                self.try_again()

    def run(self):
            try:
                #level tiles
                self.display_surface.blit(self.background,(0,0))
                self.terrain_sprites.draw(self.display_surface)
            except:
                pass
            #player
            self.player.update()
            self.player.draw(self.display_surface)
            self.horizontal_movement_collision()
            self.vertical_movement_collision()
            self.check_death()

            try:
                #platforms
                self.platform_sprites.draw(self.display_surface)
                self.platform_movement()
                self.platform_collision()
            except:
                pass

            try:
                #elevators
                self.elevator_sprites.draw(self.display_surface)
                self.elevator_movement()
                self.elevator_collision()
            except:
                pass

            try:    
                #key
                self.keys_sprites.draw(self.display_surface)
                self.key_interaction()
            except:
                pass

            try:
                #door
                self.door_sprites.draw(self.display_surface)
                self.door_interaction()
                self.door_sprites.update(self.key_index)
            except:
                pass
            try:
                #spikes
                self.spikes_sprites.draw(self.display_surface)
                self.spikes_collision()
            except:
                pass    
                
            

        