
import pygame
from pygame import *

################################################
#
# This function draws the chapter select screen
# it is called initially then repeatedly when the cursor moves
#
#  Arguments:  (what library it comes from if any) Class/Type name
# (Pygame) Screen screen - the screen, needed because you will be drawing on it
# int poistion - this is the current postion of the cursor, each position corresponds to a button
# (Pygame) Rect size - the size of the screen
# list positionsList - a list of the x coordinates of the buttons
# tuple buttonSize - (length, height) of each button
# tuple cursorSize - (length, height) of the cursor
#
################################################
def drawChapterSelect(screen, position, size, positionsList, buttonSize, cursorSize):

    screen.fill((0, 0, 0))  ## the background is a black screen

    ## the positionList dictates where on the screen the button and cursor are
    ## the button and cursor size dictate how big they are
    ## PositionList, buttonSize, cursorSize, are constants from the function chapterSelectLoop
    ## position is selected by the player in the function chapterSelectLoop
    pygame.draw.rect(screen, (84, 66, 245), pygame.Rect(positionsList[0] - (buttonSize[0] / 2), (size.height / 4), buttonSize[0], buttonSize[1]))  ## button for chapter 1
    pygame.draw.rect(screen, (245, 66, 197), pygame.Rect(positionsList[1] - (buttonSize[0] / 2), (size.height / 4), buttonSize[0], buttonSize[1]))  ## button for chapter 2
    pygame.draw.rect(screen, (69, 245, 66), pygame.Rect(positionsList[2] - (buttonSize[0] / 2), (size.height / 4), buttonSize[0], buttonSize[1]))  ## button for chapter 3
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(positionsList[position] - (cursorSize[0] / 2), (size.height / 4) + (buttonSize[1]), cursorSize[0], cursorSize[1]))  ## the cursor
    pygame.display.update()  ## update the screen


################################################
#
# This function is the loop where the player can select which chapter to play
#
#  Arguments:  (what library it comes from if any) Class/Type name
# (Pygame) Screen screen - the screen, needed to pass to the drawChapterSelect function
# int position - this is an argument becuase the default position is set the chapterSelect function
# (Pygame) Clock timer - the timer for the game, needed to uptick on each loop, this is how the game keeps an internal clock
# (Pygame) Rect size - the size of the screen, to be passed to the drawChapterSelect function
# list positionList - the positions of the buttons, to be passed to the drawChapterSelect function
# tuple buttonSize - the size of the buttons, to be passed to the drawChapterSelect function
# tuple cursorSize - the size of the cursor, to be passed to the drawChapterSelect function
#
################################################
def chapterSelectLoop(screen, position, timer, size, positionsList, buttonSize, cursorSize):

    while True:  ## the player controls the loop until they make a selection
        for e in pygame.event.get():  # retrieve the posted events (custom and keystrokes)
            if e.type == QUIT:  #this is if the X buttton is clicked
                return -1
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:  ## this is if the Escpae button is hit
                    return -1
                elif e.key == K_LEFT and position > 0:  ## move left but stop at the leftmomst button
                    position -= 1  ## position decreases as you move cursor left
                    drawChapterSelect(screen, position, size, positionsList, buttonSize, cursorSize)  # update the screen to show new cursor position
                elif e.key == K_RIGHT and position < 2:  ## move right but stop at the rightmost button
                    position += 1  ## position increases as you move cursor right
                    drawChapterSelect(screen, position, size, positionsList, buttonSize, cursorSize)  # update the screen to show new cursor position
                elif e.key == K_SPACE:  ## Space is the select
                    return position


################################################
#
# This function initializes necessary arguments for the chapter select screen and draws the initial screen before starting the loop for player control
#
#  Arguments:  (what library it comes from if any) Class/Type name
# (Pygame) Screen screen - the screen, needed to pass to the drawChapterSelect and chapterSelectLoop function
# (Pygame) Rect size - the size of the screen, to be passed to the drawChapterSelect function
# (Pygame) Clock timer - the timer for the game, needed to uptick on each loop, this is how the game keeps an internal clock
#
################################################
def chapterSelect(screen, size, timer):

    buttonSize = (96, 32)  ## set button size (currently each screen is laid out in a grid of 32x32 blocks so each button is a 3x1 on the grid)
    cursorSize = (32, 32)  ## set cursor size (currently each screen is laid out in a grid of 32x32 blocks so each button is a 1x1 on the grid)
    positionsList = [(size.width / 4), (size.width / 2), (3 * size.width / 4)] ## set the x coord for each button
                                                                               ## currently each button is automatically set to a quarter of the way down the page
                                                                               ## so the first chapter button is set to a quarter into, the second a half, and the
                                                                               ## last 3/4 way into the page (starting from the left). The cursor's laid to to be
                                                                               ## cenetered underneath the button for each position
    position = 0  ## starting position is the left most button

    drawChapterSelect(screen, position, size, positionsList, buttonSize, cursorSize)  ## draw the initial screen for the chapter select
    position = chapterSelectLoop(screen, position, timer, size, positionsList, buttonSize, cursorSize)  ## start the player controlled loop

    return position  ## return which button was selected
