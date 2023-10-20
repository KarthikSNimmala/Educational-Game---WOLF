
import pygame
from pygame import *

################################################
#
# This function draws the character select screen
# it is called initially then repeatedly when the cursor moves
#
#  Arguments:  (what library it comes from if any) Class/Type name
# (Pygame) Screen screen - the screen, needed because you will be drawing on it
# int poistion - this is the current postion of the cursor, each position corresponds to a button
# (Pygame) Rect size - the size of the screen
# list positionsList - a list of the (x, y) coordinates of the buttons
# tuple buttonSize - (length, height) of each button
# tuple cursorSize - (length, height) of the cursor
#
################################################
def drawCharacterSelect(screen, position, size, positionsList, buttonSize, cursorSize):

    screen.fill((0, 0, 0))  ## the background is a black screen

    ## the positionList dictates where on the screen the button and cursor are
    ## the button and cursor size dictate how big they are
    ## PositionList, buttonSize, cursorSize, are constants from the function characterSelectLoop
    ## position is selected by the player in the function characterSelectLoop
    pygame.draw.rect(screen, (84, 66, 245), pygame.Rect(positionsList[0][0] - (buttonSize[0] / 2), positionsList[0][1], buttonSize[0], buttonSize[1]))  ## button for a character (1)
    pygame.draw.rect(screen, (245, 66, 197), pygame.Rect(positionsList[1][0] - (buttonSize[0] / 2), positionsList[1][1], buttonSize[0], buttonSize[1]))  ## button for a character (2)
    pygame.draw.rect(screen, (69, 245, 66), pygame.Rect(positionsList[2][0] - (buttonSize[0] / 2), positionsList[2][1], buttonSize[0], buttonSize[1]))  ## button for a character (3)
    pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(positionsList[3][0] - (buttonSize[0] / 2), positionsList[3][1], buttonSize[0], buttonSize[1]))  ## button for a character (4)
    pygame.draw.rect(screen, (102, 51, 0), pygame.Rect(positionsList[4][0] - (buttonSize[0] / 2), positionsList[4][1], buttonSize[0], buttonSize[1]))  ## button for a character (5)
    pygame.draw.rect(screen, (102, 102, 153), pygame.Rect(positionsList[5][0] - (buttonSize[0] / 2), positionsList[5][1], buttonSize[0], buttonSize[1]))  ## button for a character (6)
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(positionsList[position][0] - (cursorSize[0] / 2), positionsList[position][1] + (buttonSize[1]), cursorSize[0], cursorSize[1])) ## the cursor
    pygame.display.update()  ## update the screen


################################################
#
# This function is the loop where the player can select which character to play as
#
#  Arguments:  (what library it comes from if any) Class/Type name
# (Pygame) Screen screen - the screen, needed to pass to the drawCharacterSelect function
# int position - this is an argument becuase the default position is set the drawCharacterSelect function
# (Pygame) Clock timer - the timer for the game, needed to uptick on each loop, this is how the game keeps an internal clock
# (Pygame) Rect size - the size of the screen, to be passed to the drawCharacterSelect function
# list positionList - the positions of the buttons, to be passed to the drawCharacterSelect function
# tuple buttonSize - the size of the buttons, to be passed to the drawCharacterSelect function
# tuple cursorSize - the size of the cursor, to be passed to the drawCharacterSelect function
#
################################################
def characterSelectLoop(screen, position, timer, size, positionsList, buttonSize, cursorSize):

    while True:  ## the player controls the loop until they make a selection
        for e in pygame.event.get():  ## retrieve the posted events (custom and keystrokes)
            if e.type == QUIT:  # this is if the X button is clicked
                return -1
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:  ## this is if the Escape button is hit
                    return -1
                elif e.key == K_LEFT and position > 0:  ## move left but stop at top left most button (the bottom wraps around to the top right)
                    position -= 1  ## position decreases as you move cursor left
                    drawCharacterSelect(screen, position, size, positionsList, buttonSize, cursorSize)  # update the screen to show new cursor position
                elif e.key == K_RIGHT and position < 5:  ## move right but stop at the bottom right button (the top right wraps around to the bottom left)
                    position += 1  ## position increases as you move cursor right
                    drawCharacterSelect(screen, position, size, positionsList, buttonSize, cursorSize)  # update the screen to show new cursor position
                elif e.key == K_UP and position > 2:  ## move up but stop on the top row
                    position -= 3  ## because the buttons are in rows of 3, decrement by 3 when you move up
                    drawCharacterSelect(screen, position, size, positionsList, buttonSize, cursorSize)  # update the screen to show new cursor position
                elif e.key == K_DOWN and position < 3: ## move down but stop on the bottom row
                    position += 3  ## ecuase the buttons are in rows of 3, increment y 3 when move down
                    drawCharacterSelect(screen, position, size, positionsList, buttonSize, cursorSize)  # update the screen to show new cursor position
                elif e.key == K_SPACE:  ## space is select
                    return position


################################################
#
# This function initializes necessary arguments for the character select screen and draws the initial screen before starting the loop for player control
#
#  Arguments:  (what library it comes from if any) Class/Type name
# (Pygame) Screen screen - the screen, needed to pass to the drawChapterSelect and characterSelectLoop function
# (Pygame) Rect size - the size of the screen, to be passed to the drawCharacterSelect function
# (Pygame) Clock timer - the timer for the game, needed to uptick on each loop, this is how the game keeps an internal clock
#
################################################
def characterSelect(screen, size, timer):

    buttonSize = (96, 64) ## set button size (currently each screen is laid out in a grid of 32x32 blocks so each button is a 3x2 on the grid)
    cursorSize = (32, 32) ## set cursor size (currently each screen is laid out in a grid of 32x32 blocks so each button is a 1x1 on the grid)
    positionsList = [((size.width / 4), (size.height / 4)) , ((size.width / 2), (size.height / 4)), ((3 * size.width / 4), (size.height / 4)),
                        ((size.width / 4), (size.height / 4) + buttonSize[1] + cursorSize[1] + 32) , ((size.width / 2), (size.height / 4) + buttonSize[1] + cursorSize[1] + 32), ((3 * size.width / 4), (size.height / 4) + buttonSize[1] + cursorSize[1] + 32)]
                        ## Because there are two rows, the position list is a list of 6 tuples with the (x, y) coord for top left of each button
                        ## the top row, is a quarter of the way down with enough space for the cursor and an additional 32 pix space until the next row
                        ## the columns are location are at 1/4 in, 1/2 in, and 3/4 in from the left
                        ## cursor is centered underneath each button
    position = 0 ## cursor is initially at the top left button

    drawCharacterSelect(screen, position, size, positionsList, buttonSize, cursorSize)  ## draw the initial screen for the chapter select
    position = characterSelectLoop(screen, position, timer, size, positionsList, buttonSize, cursorSize)  ## start the player controlled loop

    return position  ## return which button was selected
