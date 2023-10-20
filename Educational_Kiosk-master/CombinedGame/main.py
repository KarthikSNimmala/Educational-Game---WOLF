# Main.py runs the general structure of the game.  Every individual
# screen exists within its own function and generally within its
# own script.

# Imports
import pygame
from pygame import *

from graphics import *
from menus import *
from gameplay import *

def main():
    pygame.init()  ## initializes the pygame, required before using any other pygame functions
    S_WIDTH, S_HEIGHT = pygame.display.get_desktop_sizes()[0]
    screen = pygame.display.set_mode((S_WIDTH, S_HEIGHT)) # Make fullscreen window
    timer = pygame.time.Clock()

    menuGraphics = get_menu_graphics(S_WIDTH, S_HEIGHT)
    worldGraphics = get_world_graphics(S_WIDTH, S_HEIGHT)

    while True:
        mainMenuAction = main_menu(screen,menuGraphics)
        if mainMenuAction == -1:   ## -1 is exit
            return
        elif mainMenuAction == 0:  ## 0 is play
            characterSelection = char_select(screen,menuGraphics)
            if characterSelection == -1:
                return
            else:
                chapterSelection = chapter_select(screen,menuGraphics)
                if chapterSelection == -1:  ## -1 is exit
                    return
                else:
                    result = 1
                    while result != 0:
                        result = play(chapterSelection+1,characterSelection,screen,menuGraphics,worldGraphics,timer)
                        if result == -1:
                            return
                        elif result == 0:
                            pass
                        else:
                            chapterSelection += 1
        elif mainMenuAction == 1:
            if about_screen(screen,menuGraphics) == -1:
                return
        elif mainMenuAction == 2:
            settings_screen()

# Actually run this code.
if __name__ == '__main__':
    main()
