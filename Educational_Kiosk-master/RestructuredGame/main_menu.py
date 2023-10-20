
import pygame
from pygame import *

from classes import *

################################################
#
# This function draws the main menu screen
# it is called initially then repeatedly when the cursor moves
#
#  Arguments:  (what library it comes from if any) Class/Type name
# (Pygame) Screen screen - the screen, needed because you will be drawing on it
# int poistion - this is the current postion of the cursor, each position corresponds to a button
# (Pygame) Rect size - the size of the screen
# list positionsList - a list of the y coordinates of the buttons
# tuple buttonSize - (length, height) of each button
# tuple cursorSize - (length, height) of the cursor
#
################################################
def drawMenu(screen, position, size, positionsList, buttonSize, cursorSize):

    screen.fill((0, 0, 0))  ## the background is a black screen

    ## the positionList dictates where on the screen the button and cursor are
    ## the button and cursor size dctate how big they are
    ## PositionList, buttonSize, cursorSize, are constants from the function mainMenu
    ## position is selected by the player in the function menuLoop
    pygame.draw.rect(screen, (84, 66, 245), pygame.Rect((size.width / 2) - (buttonSize[0] / 2), positionsList[0], buttonSize[0], buttonSize[1]))  ## the play button
    pygame.draw.rect(screen, (245, 66, 197), pygame.Rect((size.width / 2) - (buttonSize[0] / 2), positionsList[1], buttonSize[0], buttonSize[1]))  ## the about button
    pygame.draw.rect(screen, (69, 245, 66), pygame.Rect((size.width / 2) - (buttonSize[0] / 2), positionsList[2], buttonSize[0], buttonSize[1]))  ## the exit button
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect((size.width / 2) + (buttonSize[0] / 2), positionsList[position], cursorSize[0], cursorSize[1]))  ## the cursor
    pygame.display.update()  # draw the buttons and cursor on the screen


################################################
#
# This function is the loop where the player can select which option they want from the menu
#
#  Arguments:  (what library it comes from if any) Class/Type name
# (Pygame) Screen screen - the screen, needed to pass to the drawMenu function
# int position - this is an argument becuase the default position is set the mainMenu function
# (Pygame) Clock timer - the timer for the game, needed to uptick on each loop, this is how the game keeps an internal clock
# (Pygame) Rect size - the size of the screen, to be passed to the drawMenu function
# list positionList - the positions of the buttons, to be passed to the drawMenu function
# tuple buttonSize - the size of the buttons, to be passed to the drawMenu function
# tuple cursorSize - the size of the cursor, to be passed to the drawMenu function
#
################################################
def menuLoop(screen, position, timer, size, positionsList, buttonSize, cursorSize):

    while True:  ##  player controls the loop until they make a selection

        for e in pygame.event.get():  # retrieve the posted events (custom and keystrokes)
            if e.type == QUIT:  #this is if the X buttton is clicked
                return -1
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:  ## this is if the Escpae button is hit
                    return -1
                elif e.key == K_UP and position > 0:  ## move up ut stop at the top button
                    position -= 1  ## position decreases as you move cursor up
                    drawMenu(screen, position, size, positionsList, buttonSize, cursorSize)  # update the screen to show new cursor position
                elif e.key == K_DOWN and position < 2:  ## move down but stop at the bottom button
                    position += 1  ## position increases as you move cursor down
                    drawMenu(screen, position, size, positionsList, buttonSize, cursorSize)  # update the screen to show new cursor position
                elif e.key == K_SPACE:  ## Space is the select
                    return position


################################################
#
# This function initializes necessary arguments for the main menu and draws the initial screen before starting the loop for player control
#
#  Arguments:  (what library it comes from if any) Class/Type name
# (Pygame) Screen screen - the screen, needed to pass to the drawMenu and menuLoop function
# (Pygame) Rect size - the size of the screen, to be passed to the drawMenu function
# (Pygame) Clock timer - the timer for the game, needed to uptick on each loop, this is how the game keeps an internal clock
#
################################################
def mainMenu(screen, size, timer):

    buttonSize = (128, 32)  ## set button size (currently each screen is laid out in a grid of 32x32 blocks so each button is a 4x1 on the grid)
    cursorSize = (32, 32)  ## set cursor size (currently each screen is laid out in a grid of 32x32 blocks so each button is a 1x1 on the grid)
    positionsList = [size.height / 4, (size.height / 4) + 64, (size.height / 4) + (64 * 2)] ## set the y coord for each button
                                                                                            ## currently each button automatically centers so no need for x coord
                                                                                            ## the first button is a quarter of the way down the page and each button
                                                                                            ## is laid out to have one button/cursor height's space between them
    position = 0  ## starting poistion is the top button

    drawMenu(screen, position, size, positionsList, buttonSize, cursorSize)  ## draw the initial screen for the menu
    position = menuLoop(screen, position, timer, size, positionsList, buttonSize, cursorSize) ## start the player controlled loop

    return position  ## return which button was selected
