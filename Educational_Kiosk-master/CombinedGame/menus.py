import pygame
import random
from classes import Entity, Indicator
from dialog import DEFAULT_LARGE_FONT, DEFAULT_TEXT_COLOR, bliterate

#ABOUT_BACKGROUND_COLOR = (240,232,223)
#ABOUT_TEXT_COLOR = (77,34,16)
ABOUT_TEXT_COLOR = (240,232,223)
    # Also in the pallette used to draw wolves:
    # (196, 190, 78)
    # (98, 94, 77)
    # (228, 228, 228)
    # (135, 111, 91)

# Most menus operate on a similar principle - the indicator paw is moved between a set
# of positions by the arrow keys/buttons until the space bar/circle button is selected.
# This method conducts that for a given list of Sprites to appear on a menu, a list
# of positions, and (in the case of grid-like menus) a list of row lengths.
def funda_menu(screen,menuGraphics,sprites,positions_list,row_length=1,default_position=0,usebg=True):
    S_WIDTH, S_HEIGHT = screen.get_width(), screen.get_height()
    p = default_position
    if not (0 <= p < len(positions_list)):
        p = random.randint(0,len(positions_list)-1)
    
    if usebg:
        screen.blit(menuGraphics['background'], (0,0))
    indicator = Indicator(menuGraphics['indicator'],positions_list[p],sprites)
    sprites.draw(screen)
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            # If the 'x' button is selected, end the game.
            if event.type == pygame.QUIT:
                return -1
            elif event.type == pygame.KEYDOWN:
                # If the 'escape' key is hit, end the game.
                if event.key == pygame.K_ESCAPE:
                    return -1
                # If arrow keys are pressed, move within the grid of positions
                # established by the list of positions and the row length
                elif event.key == pygame.K_UP and p > row_length-1:
                    p -= row_length
                elif event.key == pygame.K_DOWN and p < len(positions_list) - row_length:
                    p += row_length
                elif event.key == pygame.K_LEFT and p % row_length != 0:
                    p -= 1
                elif event.key == pygame.K_RIGHT and (p + 1) % row_length != 0:
                    p += 1
                # When the space bar is pressed, return the position as a choice
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    return p
                # If not returning a value, update the display.
                if usebg:
                    screen.blit(menuGraphics['background'], (0,0))
                indicator.move(positions_list[p])
                sprites.draw(screen)
                pygame.display.update()

# The main menu is a menu with three objects, the play button, about button, and settings
# button, and three corresponding positions for the indicator paw to rest.
# The proportions of the objects are determined by their graphics as loaded in graphics.py;
# their locations are determined here, resulting in rectangles that are of fixed proportion
# relative to the screen size.
def main_menu(screen,menuGraphics):
    # Places to put indicator paw
    S_WIDTH, S_HEIGHT = screen.get_width(), screen.get_height()
    positions_list = [(int(3*S_WIDTH/4),int(S_HEIGHT/3)),(int(7*S_WIDTH/12),int(7*S_HEIGHT/12)),
        (int(7*S_WIDTH/12),int(3*S_HEIGHT/4))]

    # Locate buttons
    sprites = pygame.sprite.Group()
    Entity(menuGraphics['play'],(int(S_WIDTH/4),int(S_HEIGHT/4)),sprites)
    Entity(menuGraphics['about'],(int(5*S_WIDTH/12),int(7*S_HEIGHT/12)),sprites)
    Entity(menuGraphics['settings'],(int(5*S_WIDTH/12),int(3*S_HEIGHT/4)),sprites)

    return funda_menu(screen,menuGraphics,sprites,positions_list)

# The character selection menu takes six random wolves from the list of wolves and
# places them in a grid of two rows (length 3).  The method funda_menu here returns
# the grid position (0 is top left, 1 is top center, read like Latin text);
# the whole function char_select returns a number corresponding to the position of 
# the chosen wolf in wolf dictionaries.
def char_select(screen,menuGraphics):
    S_WIDTH, S_HEIGHT = screen.get_width(), screen.get_height()

    # Places to put indicator paw
    positions_list = []
    for y in [int(11*S_HEIGHT/24),int(23*S_HEIGHT/24)]:
        for x in [S_WIDTH/6,S_WIDTH/2,5*S_WIDTH/6]:
            positions_list.append((int(x-S_HEIGHT/24),y))

    # Positions of wolf portraits and name placards
    sprites = pygame.sprite.Group()
    # Pick six random choices from the set of all wolves.
    wolf_choices = random.sample(range(len(menuGraphics['wolf_name_list'])),6)
    w = 0
    for wolf_number in wolf_choices:
        wolf_portrait = menuGraphics['wolf_portrait_'+str(wolf_number)]
        wolf_name_box = DEFAULT_LARGE_FONT.render(menuGraphics['wolf_name_list'][wolf_number],True,DEFAULT_TEXT_COLOR)
        # Each portrait and placard is positioned above the indicator paws' potential locations, positions_list[w]
        Entity(wolf_portrait,(int(positions_list[w][0]+S_HEIGHT/24-wolf_portrait.get_width()/2),int(positions_list[w][1]-S_HEIGHT/3)),sprites)
        Entity(wolf_name_box,(int(positions_list[w][0]+S_HEIGHT/24-wolf_name_box.get_width()/2),int(positions_list[w][1]-S_HEIGHT/3-wolf_name_box.get_height())),sprites)
        w += 1
    
    return wolf_choices[funda_menu(screen,menuGraphics,sprites,positions_list,3,-1)]

def chapter_select(screen,menuGraphics):
    S_WIDTH, S_HEIGHT = screen.get_width(), screen.get_height()

    # Locate indicator paw
    positions_list = [(int(S_WIDTH/6),int(7*S_HEIGHT/12)),(int(S_WIDTH/2),int(7*S_HEIGHT/12)),
        (int(5*S_WIDTH/6),int(7*S_HEIGHT/12))]

    # Locate entities on screen
    sprites = pygame.sprite.Group()
    Entity(menuGraphics['chap1'],(int(S_WIDTH/16),int(S_HEIGHT/4)),sprites)
    Entity(menuGraphics['chap2'],(int(3*S_WIDTH/8),int(S_HEIGHT/4)),sprites)
    Entity(menuGraphics['chap3'],(int(11*S_WIDTH/16),int(S_HEIGHT/4)),sprites)

    return funda_menu(screen,menuGraphics,sprites,positions_list,3)

# The about screen in the combined game, unlike that in the prototype,
# uses funda_menu; as such, it has to have at least one button and location for
# the indicator paw.  This has little effect on the content (besides making it
# easier to know one is returning to the main menu) and means less changes to acommodate buttons.

def about_screen(screen,menuGraphics):
    S_WIDTH, S_HEIGHT = screen.get_width(), screen.get_height()

    sprites = pygame.sprite.Group()
    # Size and place a large rectangle about the left of the screen.
    #plain_rect = pygame.Surface((int(5*S_WIDTH/12),int(11*S_HEIGHT/12)))
    #plain_rect.fill(ABOUT_BACKGROUND_COLOR)
    #print(type(plain_rect))
    #text_rect = Entity(plain_rect,(int(S_WIDTH/24),int(S_HEIGHT/24)),sprites)

    text_rect = Entity(menuGraphics['about_panel'],(int(S_WIDTH/24),int(S_HEIGHT/24)),sprites)
    # Add text onto that sprite's image and only that sprite's image.
    bliterate(text_rect.image,menuGraphics['about_text'],0,0,int(5*S_WIDTH/12),outerbuffer=50,buffer=10,color=ABOUT_TEXT_COLOR)
    # Add a main menu return button
    Entity(menuGraphics['return'],(int(5*S_WIDTH/8),int(2*S_HEIGHT/3)),sprites)
    #Entity(menuGraphics['about_picture'],(int(3*S_WIDTH/4-menuGraphics['about_picture'].get_width()/2),int(S_HEIGHT/12)),sprites)
    # The line above places a picture on the about screen, provided it appears in menuGraphics
    # after a line is uncommented there as well.  Keyword:  POLAROID

    # Only one option for indicator
    positions_list = [(int(3*S_WIDTH/4-S_HEIGHT/24),int(21*S_HEIGHT/24))]

    return funda_menu(screen,menuGraphics,sprites,positions_list)

def settings_screen():
    pass

# Dialog produces a dialog with options and returns the player's choice.
def dialog(screen,menuGraphics,question,options,image=None):
    S_WIDTH, S_HEIGHT = screen.get_width(), screen.get_height()

    BUFFER = 40 # On the sides of image, etc.
    TEXT_BUFFER = 20 # Between lines.
    runningwidth = BUFFER
    runningheight = BUFFER

    sprites = pygame.sprite.Group()
    panelpic = pygame.Surface.copy(menuGraphics['dialog'])
    positions_list = []
    if question != '':
        runningheight = bliterate(panelpic,question,runningwidth,runningheight,S_WIDTH//2-2*BUFFER,justify=True)[0] + BUFFER
    if image != None:
        image = pygame.transform.scale(image,(int(S_WIDTH/4-2*BUFFER),int(S_HEIGHT/3-runningheight-BUFFER)))
        panelpic.blit(image,(S_WIDTH//4+BUFFER,runningheight))
    for option in options:
        opth, optw = bliterate(panelpic,option,runningwidth,runningheight,S_WIDTH//6-2*BUFFER)
        positions_list.append((runningwidth+optw+BUFFER+S_WIDTH//4,int((opth+runningheight)/2-S_HEIGHT/24+S_HEIGHT/6)))
        runningheight += opth + TEXT_BUFFER
    Entity(panelpic,(S_WIDTH//4,S_HEIGHT//6),sprites)

    return funda_menu(screen,menuGraphics,sprites,positions_list,usebg=False)

# Special cases exist for dialog when Akela is speaking
def akela(screen,menuGraphics,text,options=[]):
    if options == []:
        return dialog(screen,menuGraphics,'Akela',[text],menuGraphics['akela'])
    else:
        return dialog(screen,menuGraphics,text,options,menuGraphics['akela'])

# And for when the player is speaking
def selfnote(screen,menuGraphics,text,portrait): # Usually portrait will be framelists[4]
    dialog(screen,menuGraphics,'',[text],portrait)