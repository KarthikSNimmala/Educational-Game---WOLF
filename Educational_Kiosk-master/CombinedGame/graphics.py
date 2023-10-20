# This file contains all functions which retrieve graphics files.
# If filenames need to be adjusted to accommodate new graphics, that
# will be done in here somewhere.

# In the first prototype, this code was the first function in world_generation.py and in menu_methods.py
# In the second prototype, there was no such code because there were no graphics.

import pygame
import os
import math

# These methods are used to grab graphics from the relevant directory,
# the relation of which to the working directory is expected to change.

def grab_graphic(*filename): # Still graphics belong in the "Assets" folder.
    return pygame.image.load(os.path.join('PrototypeGame','Assets',*filename))

def grab_animation(*folders): # Animations belong in the "Animations" folder.
    return pygame.image.load(os.path.join('PrototypeGame','Animations',*folders))

def grab_text(filename): # Texts belong in the main folder with the code.
    with open(os.path.join('CombinedGame',filename),'r') as textfile:
        return textfile.read()

def four_digit(number): # Animation frames in Pencil2D are numbered like this.
    num = str(number)
    while len(num) < 4:
        num = '0' + num
    return num

def even_scale(image,height):
    return pygame.transform.scale(image,(int(image.get_width()*height/image.get_height()),int(height)))

# This dictionary lists the wolves' names as they appear in game and in files.
# The use of a dictionary instead of a list allows for Máni to be referred to
# as "Máni" in dialog but as "Mani" in files.

WOLF_NAMES = {"Aspen":"Aspen","Khewa":"Khewa","Máni":"Mani","Nico":"Nico","Sparrow":"Sparrow","Timber":"Timber"}
WOLF_FEMALE = {"Aspen":False,"Khewa":True,"Máni":False,"Nico":False,"Sparrow":True,"Timber":True}
ORIENTATIONS = {0:"_Walking_Right",1:"_Walking_Away",3:"_Walking_Forward"}

# The following dictionary indicates what other species exist in the game, how many
# frames their animations run for, and whether they have four animations as opposed to two.
OTHER_ANIMALS = {"bison":(4,False),"fox":(4,False),"deer":(4,False),"rabbit":(4,False)}
# New animals for which graphics are made can have their graphics added in this dictionary
# to appear, but should ideally have a new class assigned to them.

# This method is used to retrieve all the graphics used in menus (not gameplay).
# Because of the character selection screen, both it and the next method, which
# retrieves gameplay graphics, access the constant wolf name dictionary.

def get_menu_graphics(S_WIDTH,S_HEIGHT):

    menuGraphics = { }

    # Load background, scale to screen size to fill and crop.
    # As this is the only point where some is scaled with cropping, no unique
    # function is defined for that.
    bg = grab_graphic('menu_background.jpg') # Image credit:  Jim Barton, CC 2.0
    bgw, bgh = bg.get_width(), bg.get_height()
    if S_WIDTH / bgw < S_HEIGHT / bgh:
        #print(f"bgw: {bgw}\nS_WIDTH: {S_WIDTH}\nbgh: {bgh}\nS_HEIGHT: {S_HEIGHT}")
        bg = pygame.transform.scale(bg,(int(S_HEIGHT*bgw/bgh),S_HEIGHT))
        bg = bg.subsurface(int(bg.get_width()/2-S_WIDTH/2),0,int(bg.get_width()/2-S_WIDTH/2)+S_WIDTH,S_HEIGHT)
    else:
        bg = pygame.transform.scale(bg,(S_WIDTH,int(S_WIDTH*bgh/bgw)))
        bg = bg.subsurface(0,int(bgh/2-S_HEIGHT/2),S_WIDTH,int(bgh/2-S_HEIGHT/2)+S_HEIGHT)
    bg = pygame.transform.scale(bg,(S_WIDTH,S_HEIGHT))
    menuGraphics['background'] = bg

    # Load buttons and scale to appropriate portions of window.
    # For the main menu
    menuGraphics['play'] = pygame.transform.scale(grab_graphic("Play_Button_New.png"),(int(S_WIDTH/2),int(S_HEIGHT/4)))
    menuGraphics['about'] = pygame.transform.scale(grab_graphic("About_Button_New.png"),(int(S_WIDTH/6),int(S_HEIGHT/12)))
    menuGraphics['settings'] = pygame.transform.scale(grab_graphic("Settings_Button_New.png"),(int(S_WIDTH/6),int(S_HEIGHT/12)))

    # For the about screen
    menuGraphics['about_text'] = grab_text("about.txt")
    menuGraphics['about_panel'] = pygame.transform.scale(grab_graphic("Dialog_Panel_New.png"),(int(5*S_WIDTH/12),int(11*S_HEIGHT/12)))
    menuGraphics['return'] = pygame.transform.scale(grab_graphic("Return_Button_New.png"),(int(S_WIDTH/4),int(S_HEIGHT/6)))
    #menuGraphics['about_picture'] = pygame.transform.scale(grab_graphic("about_picture.jpg"),(int(4*S_HEIGHT/9),int(S_HEIGHT/3)))
    # The line above makes a 3:4 landscape picture to appear on the about screen.  A line in about_screen() must be
    # uncommented as well for it to work.  Keyword:  POLAROID, because I'd like it to be a photograph.

    # For the settings page
    menuGraphics['sound'] = pygame.transform.scale(grab_graphic("sound_effects_label.png"),(int(S_WIDTH/2),int(S_HEIGHT/6)))
    menuGraphics['narration'] = pygame.transform.scale(grab_graphic("narration_label.png"),(int(S_WIDTH/2),int(S_HEIGHT/6)))

    # For the choose your character - wolves' portraits
    w = 0
    menuGraphics['wolf_name_list'] = list(WOLF_NAMES) # To appear above portraits.
    for eachwolf in WOLF_NAMES:
        wolfpic = grab_graphic(WOLF_NAMES[eachwolf]+"_Headshot.png")
        wolfpic = pygame.transform.scale(wolfpic,(int(S_HEIGHT*wolfpic.get_width()/(3*wolfpic.get_height())),int(S_HEIGHT/3)))
        menuGraphics['wolf_portrait_'+str(w)] = wolfpic
        w += 1

    # For the choose your chapter menu
    for c in range(1,4):
        menuGraphics['chap'+str(c)] = pygame.transform.scale(grab_graphic("chap"+str(c)+"_thumb.jpg"),(int(S_WIDTH/4),int(S_HEIGHT/4)))

    # Indicator paws
    indicator = pygame.transform.scale(grab_graphic("indicator_paw.png"),(int(S_HEIGHT/12),int(S_HEIGHT/12)))
    menuGraphics['indicator'] = indicator
    menuGraphics['indicator2'] = pygame.transform.flip(indicator,True,False)

    # For dialogs.  These objects are scaled by the methods of the dialog functions.
    menuGraphics['akela'] = grab_graphic('Akela.png')
    menuGraphics['dialog'] = pygame.transform.scale(grab_graphic("Dialog_Panel_New.png"),(int(S_WIDTH/2),int(S_HEIGHT/2)))

    # For the population meter.
    menuGraphics['pop_meter_blank'] = pygame.transform.scale(grab_graphic("Dialog_Panel_New.png"),(S_WIDTH//6,S_HEIGHT//4))

    return menuGraphics

# This method retrieves all the graphics for objects in the world.  It produces a dictionary
# wherein keys correspond to whole dictionaries of graphics of different objects.
# Currently S_WIDTH and S_HEIGHT are taken as inputs, such that objects (particularly
# animals) can be shrunk down to size; however, it would be better to make them specific sizes.
def get_world_graphics(S_WIDTH,S_HEIGHT):
    
    worldGraphics = {}

    # For the world's backgrounds, worldGraphics['background']
    def getBackGraphics():
        backgroundGraphics = {}
        backgroundGraphics['day'] = grab_graphic("Map_Background_New.png")
        backgroundGraphics['night'] = grab_graphic("Map_Background_New_Night.png")
        return backgroundGraphics
    worldGraphics['background'] = getBackGraphics()

    # For wolves traveling in four directions (left bring the reverse of right, while
    # up and down are unique), worldGraphics['wolves'].  Keys in this dictionary
    # correspond to dictionaries for each wolf in which keys correspond to lists of images,
    # one list for each orientation.
    def getWolfGraphics():
        wolvesGraphics = {}
        for each_wolf in range(len(WOLF_NAMES)):
            wolf = WOLF_NAMES[list(WOLF_NAMES)[each_wolf]]
            wolfGraphics = {2:[]}
            for orient in ORIENTATIONS:
                wolfGraphics[orient] = []
                if orient != 1:
                    for each_frame in range(1,9):
                        wolfGraphics[orient].append(even_scale(grab_animation('Wolves',wolf,wolf+ORIENTATIONS[orient]+four_digit(each_frame)+'.png'),S_HEIGHT/12))
                else:
                    for each_frame in range(1,9):
                        wolfGraphics[orient].append(even_scale(grab_animation('Wolves',wolf,wolf+ORIENTATIONS[orient]+four_digit(each_frame)+'.png'),S_HEIGHT/10))
            for each_frame in range(len(wolfGraphics[0])):
                wolfGraphics[2].append(pygame.transform.flip(wolfGraphics[0][each_frame],True,False))
            wolvesGraphics[each_wolf] = wolfGraphics
        return wolvesGraphics
    worldGraphics['wolves'] = getWolfGraphics()

    # For streams, worldGraphics['streams'], in which keys correspond to lists of images,
    # one for each possible bend in a stream.  Note also worldGraphics['streams_night'].
    # worldGraphics['streams_dims'] contains the dimensions of the images and may not be necessary,
    # especially since one is presumed fixed in the next function.
    def getStreamGraphics():
        streamGraphics = { } # The 'aim' of a stream roughly refers to the
        streamNightGraphics = { } # direction south of the west-axis in which it flows.  Rivers flow south-west, always.
        streamDimensionsByAim = { } # 's' refers to source.
        for aim in ['30','45','60','30s','45s','60s','30-45','45-60','60-30','30-60','60-45','45-30']:
            streamGraphics[aim] = []
            streamNightGraphics[aim] = []
            for i in range(1,4):  # Change length of stream animations here.
                streamGraphics[aim].append(grab_animation('Streams',aim+'000'+str(i)+'.png'))
                streamNightGraphics[aim].append(grab_animation('Streams',aim+'000'+str(i)+'_Night.png'))
            width, height = streamGraphics[aim][0].get_width(), streamGraphics[aim][0].get_height()
            streamDimensionsByAim[aim] = (width,height)
        return streamGraphics, streamNightGraphics, streamDimensionsByAim
    worldGraphics['streams'], worldGraphics['streams_night'], worldGraphics['streams_dims'] = getStreamGraphics()

    # For straight stream segments, banks are mostly straight, and the width of each image
    # is a constant 300, variable height.  For curved segments, which can connect streams of different
    # angle, the images are of a constant square dimension, 300 pixels width and height, and the
    # banks of the stream are fourth-order curves such that the stream before and after them
    # connects smoothly.  The coefficients on these curves are calculated here in worldGraphics['stream_coefficients']
    def getStreamCurveCoefficients(): # The coefficients of curves in stream bends
        def fg(t,w,i,e): # need only be calculated once.  Stream borders are cubic functions meant to be tangent to certain lines at certain points;
            def r(d): # Cool, a fourth-order nested function!                        # this makes the bends line up with the three straight parts.
                return int(d)*math.pi/180 # Converts degree-strings to radians.      # See https://www.desmos.com/calculator/gi2ea0trw1 for demo.
            f = ( (t*math.tan(r(i))+t*math.tan(r(e))+2*w/math.cos(r(e))-2*t)/t**3 , (3*t-3*w/math.cos(r(e))-2*t*math.tan(r(e))-t*math.tan(r(i)))/t**2 , math.tan(r(e)) , w/math.cos(r(e)) )
            g = ( (t*math.tan(r(i))+t*math.tan(r(e))+2*w/math.cos(r(i))-2*t)/t**3 , (3*t-3*w/math.cos(r(i))-2*t*math.tan(r(e))-t*math.tan(r(i)))/t**2 , math.tan(r(e)) , 0 )
            return f, g
        streamCurveCoefficients = { }
        for aim in ['30-45','30-60','45-30','45-60','60-30','60-45']:
            streamCurveCoefficients[aim] = fg(300,50,aim[:2],aim[-2:])
        return streamCurveCoefficients
    worldGraphics['stream_coefficients'] = getStreamCurveCoefficients()

    # For trees, worldGraphics['trees'] and worldGraphics['trees_night'] load all animations.
    # It is presumed by this function that animations have seven frames, as is done in the
    # Tree class; if longer animations were made, both functions should be changed.
    # The dictionary worldGraphics['trees_bool'] indicates whether a tree is evergreen.
    # The keys in worldGraphics['trees'] correspond to dictionaries wherein season
    # names ('summer','autumn','winter') correspond to lists of images, one dictionary
    # for each variety of tree.
    def getTreeGraphics():
        treeGraphics = { } # Dictionary of framelists (one for each season) by type.
        treeNightGraphics = { }
        treeGreenness = { } # Dictionary of whether a tree is evergreen (same image in winter)
        for type in ['White_Oak','Common_Ash']: # List all non-evergreen trees here.
            treeGraphics[type] = {'summer':[],'autumn':[],'winter':[]}
            treeNightGraphics[type] = {'summer':[],'autumn':[],'winter':[]}
            for i in range(1,8):
                treeGraphics[type]["summer"].append(grab_animation('Trees',type+'_Summer000'+str(i)+'.png'))
                treeNightGraphics[type]["summer"].append(grab_animation('Trees',type+'_Summer000'+str(i)+'_Night.png'))
                treeGraphics[type]["autumn"].append(grab_animation('Trees',type+'_Autumn000'+str(i)+'.png'))
                treeNightGraphics[type]["autumn"].append(grab_animation('Trees',type+'_Autumn000'+str(i)+'_Night.png'))
                treeGraphics[type]["winter"].append(grab_animation('Trees',type+'_Winter000'+str(i)+'.png'))
                treeNightGraphics[type]["winter"].append(grab_animation('Trees',type+'_Winter000'+str(i)+'_Night.png'))
            treeGreenness[type] = False
        for type in ['Spruce']: # List all evergreen trees here.
            treeGraphics[type] = {"summer":[]}
            treeNightGraphics[type] = {"summer":[]}
            for i in range(1,8):
                treeGraphics[type]["summer"].append(grab_animation('Trees',type+'000'+str(i)+'.png'))
                treeNightGraphics[type]["summer"].append(grab_animation('Trees',type+'000'+str(i)+'_Night.png'))
            treeGreenness[type] = True
        return treeGraphics, treeNightGraphics, treeGreenness
    worldGraphics['trees'], worldGraphics['trees_night'], worldGraphics['trees_bool'] = getTreeGraphics()

    # worldGraphics['rocks'] and worldGraphics['rocks_night'] are simple dictionaries
    # where values are images, keys types of rocks.
    def getRockGraphics(): # Any static obstacle is a rock.
        rockGraphics = { }
        rockNightGraphics = { }
        for rocktype in ['Limestone_New','nonrock']:
            rockGraphics[rocktype] = grab_graphic(rocktype+'.png')
            rockNightGraphics[rocktype] = grab_graphic(rocktype+'_Night.png')
        return rockGraphics, rockNightGraphics
    worldGraphics['rocks'], worldGraphics['rocks_night'] = getRockGraphics()

    # worldGraphics['decor'] and worldGraphics['decor_night] have both images and lists of images
    # as values; worldGraphics['decor_bool'] has the same keys with Boolean values indicating
    # which have images, which lists.
    def getDecorGraphics():
        decorGraphics = { }
        decorNightGraphics = { }
        decorDynamics = { }
        for dynamictype in ['grass']:
            dynamicLengths = {'grass':7}    # Unlike trees, which all blow in the same wind,
            decorGraphics[dynamictype] = [] # dynamic decorations are allowed to have different lengths of animations.
            decorNightGraphics[dynamictype] = []
            for i in range(1,dynamicLengths[dynamictype]+1):
                decorGraphics[dynamictype].append(grab_animation('Decorations',dynamictype+'000'+str(i)+'.png'))
                decorNightGraphics[dynamictype].append(grab_animation('Decorations',dynamictype+'000'+str(i)+'_Night.png'))
            decorDynamics[dynamictype] = True
        for statictype in ['flower1','flower2','flower3','flower4']:
            decorGraphics[statictype] = grab_graphic('Decorations',statictype+'.png')
            decorNightGraphics[statictype] = grab_graphic('Decorations',statictype+'_Night.png')
            decorDynamics[statictype] = False
        return decorGraphics, decorNightGraphics, decorDynamics
    worldGraphics['decor'], worldGraphics['decor_night'], worldGraphics['decor_bool'] = getDecorGraphics()

    # A decision was made not to use prints in the final game,
    # replacing the hunting mini-game with live hunting, but in case that decision is reversed for
    # any reason, the code remains here, commented out.  All code necessary to return the print
    # graphics and objects to the world is marked with the keyword FOOTPRINT, but no new
    # code to re-implement the hunting mini-game has been written.
    #def getPrintGraphics(S_HEIGHT): # Height is the height of the world, by which prints are scaled.
    #    printGraphics = { } # Prints, large and identifiable for dialogs
    #    printGraphicsSmall = { } # Blitted images in the world
    #    animalTypes = { } # Types by animal - 0 for prey, 1 for mutual, 2 for predator
    #    for animal in ['bison']: # List predators here - bear, moose
    #        printGraphics[animal] = grab_graphic(animal+"_print.png")
    #        printGraphicsSmall[animal] = even_scale(printGraphics[animal],int(S_HEIGHT/15))
    #        animalTypes[animal] = 2
    #    for animal in []: # List neither predator nor prey here - raccoons, foxes
    #        printGraphics[animal] = grab_graphic(animal+"_print.png")
    #        printGraphicsSmall[animal] = even_scale(printGraphics[animal],int(S_HEIGHT/15))
    #        animalTypes[animal] = 1
    #    for animal in ['deer','rabbit']: # List prey here
    #        printGraphics[animal] = grab_graphic(animal+"_print.png")
    #        printGraphicsSmall[animal] = even_scale(printGraphics[animal],int(S_HEIGHT/15))
    #        animalTypes[animal] = 0
    #    return printGraphics, printGraphicsSmall, animalTypes
    #printGraphics, printGraphicsSmall, animalTypes = getPrintGraphics(window_height)

    # For the den and farm objects.  Currently, the values in worldGraphics['misc'] and
    # worldGraphics['misc_night'] are images.
    def getMiscellaneousGraphics():
        miscellaneousGraphics = { }
        miscellaneousNightGraphics = { }
        miscellaneousGraphics['den'] = grab_graphic('Wolf_Den.png')
        miscellaneousNightGraphics['den'] = grab_graphic('Wolf_Den_Night.png')
        miscellaneousGraphics['farm'] = grab_graphic('farm.png')
        miscellaneousNightGraphics['farm'] = grab_graphic('farm_Night.png')
        return miscellaneousGraphics, miscellaneousNightGraphics
    worldGraphics['misc'], worldGraphics['misc_night'] = getMiscellaneousGraphics()

    # For animals which are not wolves, worldGraphics['animals'] has species for keys,
    # dictionaries similar to wolves's for values.  The OTHER_ANIMALS dictionary above
    # is used here, to find how many frames each species's animation has and how many
    # orientations.  Currently, all non-wolves only have two animated orientations.
    def getAnimalGraphics(S_HEIGHT):
        animalGraphics = { }
        for species in OTHER_ANIMALS:
            if OTHER_ANIMALS[species][1]:
                animalGraphics[species] = {0:[],1:[],2:[],3:[]}
                for frame in range(1,OTHER_ANIMALS[species][0]+1):
                    for orient in ORIENTATIONS:
                        animalGraphics[species][orient].append(grab_animation('Animals',species+ORIENTATIONS[orient]+four_digit(frame)+'.png'))
                    animalGraphics[species][2].append(pygame.transform.flip(animalGraphics[species][0][-1],True,False))
            else:
                animalGraphics[species] = {0:[],1:[]}
                for frame in range(1,OTHER_ANIMALS[species][0]+1):
                    animalGraphics[species][0].append(grab_animation('Animals',species+'_right'+four_digit(frame)+'.png'))
                    if species == 'rabbit':
                        animalGraphics[species][0][-1] = even_scale(animalGraphics[species][0][-1],S_HEIGHT/18)
                    elif species == 'deer':
                        animalGraphics[species][0][-1] = even_scale(animalGraphics[species][0][-1],S_HEIGHT/8)
                    elif species == 'fox':
                        animalGraphics[species][0][-1] = even_scale(animalGraphics[species][0][-1],S_HEIGHT/9)
                    elif species == 'bison':
                        animalGraphics[species][0][-1] = even_scale(animalGraphics[species][0][-1],S_HEIGHT/6)
                    animalGraphics[species][1].append(pygame.transform.flip(animalGraphics[species][0][-1],True,False))
        return animalGraphics

    worldGraphics['animals'] = getAnimalGraphics(S_HEIGHT)

    return worldGraphics
        