
import pygame
from pygame import *

from classes import *
from mini_games import *

################################################
#
# This function builds the level, or world, for the player. The argument level is list of strings
# where each character in the strings is a 32x32 block. After initializing the player, the camera,
# and the Pygame Groups for the platform, a loop initializes each entity in the level and adds it
# to the appropriate groups
#
#  Arguments:  (what library it comes from if any) Class/Type name
# list level - a list of strings where each character is an entitiy in the level
#
################################################
def buildLevel(level):

    platforms = pygame.sprite.Group()  ## the entities that the player can collide with
    player = Player(platforms, (TILE_SIZE, TILE_SIZE)) ## the player initialized
    bg = Background(platforms)
    level_width = len(level[0]) * TILE_SIZE ## calculate the width of the world
    level_height = len(level) * TILE_SIZE  ## calculate the height of the world
    entities = CameraAwareLayeredUpdates(player, pygame.Rect(0, 0, level_width, level_height))  ## initialize the camer, entities is a group
                                                                                                ## of every entity on the screen
    player.add(entities)                                                                        ## And this should include player!
    bg.add(entities)

    ## This is a loop that goes through each character in the level argument, and makes an entity depeding on what character it is
    x = y = 0
    for row in level:
        for col in row:
            if col == "P":
                Platform((x, y), platforms, entities)
                #print((x, y))
            if col == "E":
                ExitBlock((x, y), platforms, entities)
            if col == "T":
                TestBlock((x, y), platforms, entities)
            if col == "A":
                AnimalBlock((x, y), platforms, entities)
            x += TILE_SIZE  ## add the TILE_SIZE (32) because every block is 32x32 pix
        y += TILE_SIZE
        x = 0

    return platforms, player, level_width, level_height, entities  ## return all relevant data


################################################
#
# This function is the core gameplay loop, this is what runs for the bulk of the game. The for loop
# is for different events that have been posted, mostly by the player colliding with other entities
# The last 5 statments after the for loop are crucial. The entities.update() runs the update funciton
# for every single entity + camera (which moves the camera, moves the player, and any other updates)
# then the next 3 redraws the new sprites on the screen, which have been now updated. The last one
# upticks the timer, this controls how fast events are processed while playing the game and used to
# measure time in the game.
#
#  Arguments:  (what library it comes from if any) Class/Type name
# (Pygame) Group entities - all entites on the screen
# (Pygame) Sprite player - the player
# (Pygame) Clock timer - the timer for the game
#
################################################
def gameplayLoop(screen, entities, player, timer):

    while True:

        for e in pygame.event.get():
            if e.type == QUIT:
                return
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                return
            if e == TEST_EVENT:
                player.setPos((TILE_SIZE, TILE_SIZE))  ## reset the player position
                player.platforms = huntGameLoop(screen, player, timer)  ## enter the mini game loop
                                                                        ## that function returns the platforms of the base world
                                                                        ## so there's no invisibile walls

        entities.update()

        screen.fill((0, 0, 0))
        entities.draw(screen)
        pygame.display.update()
        timer.tick(60)
