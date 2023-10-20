
import pygame
from pygame import *

from events import *

import os

SCREEN_SIZE = pygame.Rect((0, 0, 800, 640))  # the size of the screen represented as a Pygame Rect
TILE_SIZE = 32  # the dimension of each square on the 'grid' of the layout
                # currently each

################################################
#
# This class is for the camera, or what the user currently sees on the screen. This is pulled almost entirely from
# Stack overflow so I am not 100% sure how all of this works.
#
#  Atributes:  (what library it comes from if any) Class/Type name
# (Pygame) Sprite target - what the camera is tracking, can be any sprite but will almost always be the player
# (Pygame) Vector cam - the position of the camera
# (Pygame) Rect world_size - the size of the entire world, not just what is on the screen but the entire world
#
################################################
class CameraAwareLayeredUpdates(pygame.sprite.LayeredUpdates):
    def __init__(self, target, world_size):
        super().__init__()
        self.target = target
        self.cam = pygame.Vector2(0, 0)
        self.world_size = world_size
        if self.target:
            self.add(target)

    ## This function is the update function that runs on every tick of the Clock
    ## The important part here is the if self.target, which will move the camera
    ## around the target, keeping it cenetered but stopping on edges of the world
    def update(self, *args):
        super().update(*args)
        if self.target:
            x = -self.target.rect.center[0] + SCREEN_SIZE.width / 2  ## get the new x
            y = -self.target.rect.center[1] + SCREEN_SIZE.height / 2  ## get the new y
            self.cam += (pygame.Vector2((x, y)) - self.cam) * 0.05  ## update the camera coordinates with new x and y
            self.cam.x = max(-(self.world_size.width - SCREEN_SIZE.width), min(0, self.cam.x))  ## these two lines hold
            self.cam.y = max(-(self.world_size.height - SCREEN_SIZE.height), min(0, self.cam.y))  ## the camera still on edges of the world

    ## this function redraws everything in the camera. This function was pulled
    ## straight from Stack Overflow so I am not as sure on how every part of
    ## this works, but it does work
    def draw(self, surface):
        spritedict = self.spritedict
        surface_blit = surface.blit
        dirty = self.lostsprites
        self.lostsprites = []
        dirty_append = dirty.append
        init_rect = self._init_rect ## all these lines is just renaming different ojects and funtions

        for spr in self.sprites() + [self.target]:
            rec = spritedict[spr]
            newrect = surface_blit(spr.image, spr.rect.move(self.cam))
            if rec is init_rect:
                dirty_append(newrect)
            else:
                if newrect.colliderect(rec):
                    dirty_append(newrect.union(rec))
                else:
                    dirty_append(newrect)
                    dirty_append(rec)
            spritedict[spr] = newrect
        return dirty  ## best explanation I can give is it organizes the sprites by what stays on the
                      ## screen and what doesn't and blit those that are but this is just a general
                      ## intuition about it


################################################
#
# This class is for any sprite entitiy. This is just a parent for all other obects on screen
# currently used for Player, Platform, TestBlock, and Animal Block but will be used for all
# other obstacles and interactables in future development
#
#  Atributes:  (what library it comes from if any) Class/Type name
# (Pygame) Color color - what color the block is (will be replaced by image for the sprite in future development)
# tuple pos - the position (top left) of the entity
# (Pygame) Group *groups - kwargs (so you can list as man as you want) of all the different groups that the entity
#                          belongs to, which group dictates when it is updated and what it interacts with
#
################################################
class Entity(pygame.sprite.Sprite):
    def __init__(self, color, pos, *groups):
        super().__init__(*groups)
        self.image = Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft = pos)

################
# A test class for animated objects
class Animate(pygame.sprite.Sprite):
    def __init__(self, images, pos, *groups):
        super().__init__(*groups)
        self.images = images 
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(topleft = pos)
    
    def update(self):
        #print(self.index)
        if self.index == len(self.images) - 1:
            self.index = 0
        else:
            self.index += 1
        self.image = self.images[self.index]

maindirectory = os.path.dirname(os.getcwd())
grassdirectory = os.path.join(maindirectory,"Educational_Kiosk",'PrototypeGame','Animations','Decorations')
grassimageset = []
for i in range(1,8):
    grassimageset.append(pygame.image.load(os.path.join(grassdirectory,"grass000"+str(i)+".png")))

###################
# Class for background b/c camera does not expect one
class Background(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load(os.path.join(maindirectory,"Educational_Kiosk","PrototypeGame","Assets","Map_Background.png"))
        self.rect = self.image.get_rect(topleft = (0,0))

################################################
#
# This class is for the player. The core functions are update and collide, which updates and handles collisions
# with the player. Every other function is utility for moving the player through the game.
#
#  Atributes:  (what library it comes from if any) Class/Type name
# (Pygame) Group platforms - the group of platforms that the player can collide with, changes as player moves between mini-games
# tuple pos - the position (top left) of the entity
# (Pygame) Group *groups - kwargs (so you can list as man as you want) of all the different groups that the entity
#                          belongs to, which group dictates when it is updated and what it interacts with
#
################################################
class Player(Animate):
    def __init__(self, platforms, pos, *groups):
        super().__init__(grassimageset, pos)
        self.vel = pygame.Vector2((0, 0))
        self.platforms = platforms
        self.speed = 8

    ## this function is the update functino for the player, it grabs which keys have been pressed
    ## and changes the velocity (speed and direction) of the player accordingly
    ## then checks for any collisions
    ## any actions that the player could take or any time variable attributes like a steadily
    ## decreasing health would be put in here
    def update(self):
        super().update()
        pressed = pygame.key.get_pressed()
        up = pressed[K_UP]
        down = pressed[K_DOWN]
        left = pressed[K_LEFT]
        right = pressed[K_RIGHT]
        running = pressed[K_SPACE] ## get which keys have/are pressed

        if up:
            self.vel.y = -self.speed
        if down:
            self.vel.y = self.speed
        if left:
            self.vel.x = -self.speed
        if right:
            self.vel.x = self.speed
        if running:
            self.vel *= 1.5  ## adjust the velocity of the player according to which keys are being pressed

        if not (left or right):
            self.vel.x = 0
        if not (up or down):
            self.vel.y = 0  ## stop moving if no keys are pressed

        self.rect.left += self.vel.x  ## move the actual rectangle, or image, of the player as the speed changes
        self.collide(self.vel.x, 0, self.platforms) ## check for collisions in the x direction
        self.rect.top += self.vel.y  ## move the actual rectangle, or image, of the player as the speed changes
        self.collide(0, self.vel.y, self.platforms) ## check for collisions in the y direction

    ## this function is for when the player collides with another entity
    ## every block that the player can collide with is in the platforms group.
    ## for solid platforms, the player isn't allowed to go past the outer bounds
    ## of the platform, keeping it from passing through
    ## to have collisions interactions, like having a dialouge box pop up
    ## you check what kind of block it is with isinstance and then post the
    ## corresponding event to be used in gameplay loops
    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, ExitBlock):
                    pygame.event.post(pygame.event.Event(QUIT))
                if isinstance(p, TestBlock):
                    pygame.event.post(TEST_EVENT)
                    p.kill()
                if isinstance(p, AnimalBlock):
                    pygame.event.post(KILL_ANIMAL)
                    p.kill()
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                if yvel < 0:
                    self.rect.top = p.rect.bottom

    ## this is a utility function to change the position of the player.
    ## it just changes to position of the player to whatever argument you pass
    ## it also resetsthe pygame Vector just as a precaution
    def setPos(self, pos):
        self.rect = self.image.get_rect(topleft = pos)
        self.vel = pygame.Vector2((0, 0))

    ## this is a utility function called when entering a mini game to change the
    ## platforms attribute. This is important because whatever is in this
    ## attribute are what entities the player can collide with so it needs to
    ## be changed moving back and forth between mini games or you'll be passing
    ## through some entities and running into invisibile walls
    def setNewLevel(self, platforms):
        self.vel = pygame.Vector2((0, 0))
        self.platforms = platforms


################################################
#
# All these classes underneath this header are different entities that the player can collide with.
# They are all the same except for the color, they are different classes because in the player collide
# it checks what kind of block the player collided with
#
#  Atributes:  (what library it comes from if any) Class/Type name
# tuple pos - the position (top left) of the entity
# (Pygame) Group *groups - kwargs (so you can list as man as you want) of all the different groups that the entity
#                          belongs to, which group dictates when it is updated and what it interacts with
#
################################################
class Platform(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color('#DDDDDD'), pos, *groups)

class ExitBlock(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color('#0033FF'), pos, *groups)

class TestBlock(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color('#FF0000'), pos, *groups)

class AnimalBlock(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color('#00FF00'), pos, *groups)
