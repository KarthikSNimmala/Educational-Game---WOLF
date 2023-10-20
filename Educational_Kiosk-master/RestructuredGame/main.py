#! /usr/bin/python

import pygame
from pygame import *

from main_menu import *
from classes import *
from gameplay import *
from chapter_select import *
from character_select import *
from levels import *

# Line 13's comment indicates that Robert is able to edit files in the GitHub repo.

################################################
#
# This is the main loop, self explanatory
#
################################################
def main():
    pygame.init()  ## initializes the pygame, required before using any other pygame functions
    screen = pygame.display.set_mode(SCREEN_SIZE.size)  ## initializes the screen, SCREEN_SIZE is a constant in classes.py
    pygame.display.set_caption("Use arrow keys to move!")  ## sets the caption at the top bar of the screen
    timer = pygame.time.Clock()  ## starts the clock, this is needed to start the ticks in the game loops

    menuAction = mainMenu(screen, SCREEN_SIZE, timer)  ## starts the main menu screen, menuAction is a int indicating what was selecting
    if menuAction == -1:   ## -1 is exit
        return
    elif menuAction == 0:  ## 0 is play
        ##  TODO
        # add the about screen as int 1
        chapterSelectAction = chapterSelect(screen, SCREEN_SIZE, timer)  ## starts the chapter select screen, chapterSelectAction is an int indication which chapter
        if chapterSelectAction == -1:  ## -1 is exit
            return
        else:
                ##  TODO
                ## 0 is chapter 1
                ## 1 is chapter 2
                ## 2 is chapter 3

            characterSelectAction = characterSelect(screen, SCREEN_SIZE, timer)  ## starts the character select screen, characterSelectAction is an int indication which character
            if characterSelect == -1:  ## -1 is exit
                return
            else:
                    ##  TODO
                    ## 0-5 are the different wolves, changes appearance

                platforms, player, level_width, level_height, entities = buildLevel(large_level)  ## builds the level using the large_level layout
                                                                                                  ## returns the groups/objects for the platforms, the player, the entities and ints for the level_width and height

                                                                                                  ##  TODO
                                                                                                  ## make the random level generation
                gameplayLoop(screen, entities, player, timer)  ## starts the core gameplay loop



################################################
#
# the boilerplate code to run the main function
# because main.py is designed to be the main file this boilerplate will be the one running in the final design
#
################################################
if __name__ == '__main__':
    main()
