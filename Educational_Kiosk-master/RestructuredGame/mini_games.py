
import pygame
from pygame import *

from classes import *
from levels import *

################################################
#
# This function builds the level for the hunting mini game. It performs almost exactly like buidlevel from
# gameplay.py but it takes the player as an argument rather than initialzing it in this funtion.
#
#  Arguments:  (what library it comes from if any) Class/Type name
# (Pygame) Sprite player - the player, this gets passed in because it is the player needs to get added to the
#                          new entities made by the camera initialization
#
################################################
def huntGame(player):

    level = small_level  ## using the small level layour right now, this will be changed to a generated level in final development
    platforms = pygame.sprite.Group()  ## the entities that the player can collide with

    level_width = len(level[0]) * TILE_SIZE  ## calculate the width of the world
    level_height = len(level) * TILE_SIZE  ## calculate the height of the world
    entities = CameraAwareLayeredUpdates(player,  pygame.Rect(0, 0, level_width, level_height)) ## initialize the camer, entities is a group
                                                                                                ## of every entity on the screen

## This is a loop that goes through each character in the level argument, and makes an entity depeding on what character it is
    x = y = 0
    for row in level:
        for col in row:
            if col == "P":
                Platform((x, y), platforms, entities)
            if col == "E":
                ExitBlock((x, y), platforms, entities)
            if col == "T":
                TestBlock((x, y), platforms, entities)
            if col == "A":
                AnimalBlock((x, y), platforms, entities)
            x += TILE_SIZE  ## add the TILE_SIZE (32) because every block is 32x32 pix
        y += TILE_SIZE
        x = 0

    return platforms, entities  ## return all relevant data


################################################
#
# This function is the gameplay loop for the hunting mini game, this functions nearly identical to
# gameplay loop. There are a couple lines in the beginning to build the hunting mini game but also
# to save the platforms from the orginal world to return when this mini game ends. Then the new
# platforms for the minigame are set in the player attriutes.
#
#  Arguments:  (what library it comes from if any) Class/Type name
# (Pygame) Screen screen - The screen, needed to update/draw the minigame on screen
# (Pygame) Sprite player - the player
# (Pygame) Clock timer - the timer for the game
#
################################################
def huntGameLoop(screen, player, timer):

    oldPlatforms = player.platforms
    platforms, entities = huntGame(player)
    player.setNewLevel(platforms)

    while True:

        for e in pygame.event.get():
            if e.type == QUIT:
                return
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                return
            if e == KILL_ANIMAL:
                print('Found Animal Block')
                return oldPlatforms  ## return the old platforms so there are proper collisions
                                     ## in the original level

        entities.update()

        screen.fill((0, 0, 0))
        entities.draw(screen)
        pygame.display.update()
        timer.tick(60)
