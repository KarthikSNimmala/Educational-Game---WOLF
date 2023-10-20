# Main.py runs the general structure of the game.  Every individual
# screen exists within its own function and generally within its
# own script.

# Imports
import pygame
from pygame import *

from graphics import *
from menus import *
from gameplay import *

from gpiozero import Button

def main():
    BUTTONS = {"GO":Button(2),"DOWN":Button(3),"RIGHT":Button(4),"UP":Button(5),"LEFT":Button(6)}
    
    pygame.init()  ## initializes the pygame, required before using any other pygame functions
    
    screen = pygame.display.set_mode((1800,900)) # Replace this line with next to
    #screen = pygame.display.set_mode((1800,1000),pygame.FULLSCREEN)
    S_WIDTH, S_HEIGHT = screen.get_width(), screen.get_height()
    timer = pygame.time.Clock()

    menuGraphics = get_menu_graphics(S_WIDTH, S_HEIGHT)
    worldGraphics = get_world_graphics(S_WIDTH, S_HEIGHT)

    while True:
        mainMenuAction = main_menu(screen,menuGraphics,BUTTONS)
        if mainMenuAction == -1:   ## -1 is exit
            return
        elif mainMenuAction == 0:  ## 0 is play
            characterSelection = char_select(screen,menuGraphics,BUTTONS)
            if characterSelection == -1:
                return
            else:
                chapterSelection = chapter_select(screen,menuGraphics,BUTTONS)
                if chapterSelection == -1:  ## -1 is exit
                    return
                else:
                    result = 1
                    while result != 0:
                        result = play(chapterSelection+1,characterSelection,BUTTONS,screen,menuGraphics,worldGraphics,timer)
                        if result == -1:
                            return
                        elif result == 0:
                            pass
                        else:
                            chapterSelection += 1
        elif mainMenuAction == 1:
            if about_screen(screen,menuGraphics,BUTTONS) == -1:
                return
        elif mainMenuAction == 2:
            settings_screen()

# Actually run this code.
if __name__ == '__main__':
    main()
