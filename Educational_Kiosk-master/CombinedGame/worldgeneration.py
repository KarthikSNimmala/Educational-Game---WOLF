import classes
import pygame
import random
import math
from graphics import WOLF_NAMES, WOLF_FEMALE

# This script contains one function, generate_world, which produces a World object.  It is the
# only function wherein objects of any class in classes.py except for "Entity" and "Indicator"
# are made.  The menuGraphics and worldGraphics dictionaries are passed to this function such
# that the graphics can be sent to these initialized objects.
# Everything in the world is measured in pixels.  The dimensions of the world are determined by
# the dimensions of the background image, and the dimensions of everything in it by the size of
# their graphics.
# World generation is a step-by-step process:  first, streams are added, then rocks, then trees,
# then a human farm and den, and then animals.
def generate_world(screen_dims,menuGraphics,worldGraphics,chapter,character,player=None):

    # STEP 0
    # Get background and world dimensions
    background = worldGraphics["background"]["day"]
    nightbackground = worldGraphics["background"]["night"]
    worldx, worldy = background.get_width(), background.get_height()

    # STEP 1
    # Add streams
    streams = pygame.sprite.Group()
    def pourStream(worldx,worldy,screen_dims,worldGraphics):
        sourcex = random.randint(screen_dims[0],worldx) # Place a random source, pick a direction, and go.
        sourcey = random.randint(screen_dims[1],worldy) # Since dens place near streams IRL, try to have enough stream in world.
        dir = random.choice(['30','45','60'])      # Degrees counterclockwise from east, if going upstream.  All streams flow southwest, as is typical for Indiana.
        riverys = {'30':58,'45':71,'60':100} # Vertical height of the river at crossing, by angle.
                                             # Equals width times the secant of the angle.
        aim = dir+'s'
        classes.Stream(worldGraphics['streams'][aim],worldGraphics['streams_night'][aim],(sourcex,sourcey),aim,streams)
        runningx = sourcex                      # Running x and y are the coordinates of the left
        runningy = sourcey + 200 - riverys[dir] # edge of the north bank as we flow south-west with each segment.

        while runningx > 0 and runningy < worldy:
            if random.random() > 0.25: # Half a chance of changing direction with each.
                newdir = random.choice(['30','45','60']) # Because it might pick the same again.
            else:
                newdir = dir
            if newdir == dir:
                aim = dir
            else:
                aim = '-'.join([dir,newdir])
            classes.Stream(worldGraphics['streams'][aim],worldGraphics['streams_night'][aim],(runningx-worldGraphics['streams'][aim][0].get_width(),runningy),aim,streams)
            runningx -= worldGraphics['streams'][aim][0].get_width()
            runningy += worldGraphics['streams'][aim][0].get_height() - riverys[newdir]
            dir = newdir
    
    # Produce a random number of streams - probably one, possible two or three.
    for i in range(6//random.randint(2,6)):
        pourStream(worldx,worldy,screen_dims,worldGraphics)

    # This method determines whether an object's rectangle appears in the wet part
    # of any stream in the "streams" argument.  The covers_rect method is unique defined
    # for stream objects, see classes.py.
    def dry(rect,streams,sCC):
        for everystream in streams:
            if everystream.covers_rect(rect,sCC):
                return False
        return True
    
    # STEP 2
    # Add rocks
    rocks = pygame.sprite.Group()
    def placeRock(worldx,worldy,streams,worldGraphics,rocktype=None):
        if rocktype == None: # Choose random rock type.
            rocktype = random.choice(list(worldGraphics['rocks']))
        newrock = classes.Rock(worldGraphics["rocks"][rocktype],worldGraphics["rocks_night"][rocktype],(random.randint(0,worldx),random.randint(0,worldy)),rocks)
        # Limestone, it's okay to put in a stream.  Other things, like the "nonrock" bush, should be kept dry.
        while rocktype not in ['Limestone_Night'] and not dry(newrock.rect,streams,worldGraphics['stream_coefficients']):
            newrock.pos = (random.randint(0,worldx),random.randint(0,worldy))
            newrock.rect = newrock.image.get_rect(topleft=newrock.pos)
            newrock.collision_rect = classes.compress_rect(newrock.image.get_rect(topleft=newrock.pos),newrock.collision_box)
    # The number of rocks placed is fifty, give or take up to twenty.  The exponent of 2
    # keeps the number of rocks generally closer to fifty, and can be changed to affect
    # the standard deviation of the number of rocks placed in each game, if that mattered.
    for i in range(50+random.choice([-1,1])*math.floor(random.random()**2*20)):
        placeRock(worldx,worldy,streams,worldGraphics)

    # Rocks are put into an obstacle group now, and the "safe" function defined,
    # to determine areas where other objects can be placed such that they do not
    # collide with rocks.
    obstacles = pygame.sprite.Group()
    obstacles.add(rocks)
    def safe(rect,streams,sCC,obstacles):
        if not dry(rect,streams,sCC):
            return False 
        for ob in obstacles:
            if rect.colliderect(ob.collision_rect):
                return False
        return True

    # STEP 3
    # Add trees
    forest = pygame.sprite.Group() # The group of trees is called "forest" and not "trees."  Legacy from PrototypeGame.
    # The plantTree method places a random tree of given species in a place where it doesn't intersect with
    # obstacles.  The tree is added to both the forest group, and immediately to the obstacles group,
    # so trees cannot collide with each other, though rocks can.
    def plantTree(worldx,worldy,species,streams,worldGraphics):
        newtree = classes.Tree(worldGraphics['trees'][species],worldGraphics['trees_night'][species],(random.randint(0,worldx),random.randint(0,worldy)),species,worldGraphics['trees_bool'][species],forest)
        while not safe(newtree.collision_rect,streams,worldGraphics['stream_coefficients'],obstacles):
            newtree.pos = (random.randint(0,worldx),random.randint(0,worldy))
            newtree.rect = newtree.image.get_rect(topleft=newtree.pos)
            newtree.collision_rect = classes.compress_rect(newtree.image.get_rect(topleft=newtree.pos),newtree.collision_box)
        obstacles.add(newtree)
    # The forestWorld method plants an amount of trees given by treecount, which unlike
    # the amount of rocks does not vary on a bell curve.  It also chooses tree types - if
    # there are more than five types of trees, only 3-5 are chosen.
    def forestWorld(worldx,worldy,streams,worldGraphics):
        treecount = worldx*worldy * random.randint(28,175) // 10000000   # Based on historical forest estimates
        if len(worldGraphics['trees']) > 5: # If we get so far, forests can be unique # and an arbitrary conversion of pixels
            treeTypes = random.sample(treeTypes,random.randint(3,5))     # to real-life units.
        else:
            treeTypes = list(worldGraphics['trees'])
        for t in range(treecount):
            plantTree(worldx,worldy,random.choice(treeTypes),streams,worldGraphics)
    forestWorld(worldx,worldy,streams,worldGraphics)

    # STEP 4
    # Add flowers and grass
    decorations = pygame.sprite.Group()
    def growFlower(worldx,worldy,streams,obstacles,worldGraphics):
        # The growFlower method places some random object from worldGraphics's decor
        # assigned "False" in the "decor_bool" dictionary, that is, any static, not animated, decor.
        species = random.choice(list(worldGraphics['decor_bool']))
        while worldGraphics['decor_bool'][species]:
            species = random.choice(list(worldGraphics['decor_bool']))
        # These static objects are of the "Terran" class, because they have no properties.
        newflower = classes.Terran(worldGraphics['decor'][species],worldGraphics['decor_night'][species],(random.randint(0,worldx),random.randint(0,worldy)),decorations)
        while not safe(newflower.rect,streams,worldGraphics['stream_coefficients'],obstacles):
            newflower.pos = (random.randint(0,worldx),random.randint(0,worldy))
            newflower.rect = newflower.image.get_rect(topleft=newflower.pos)
        # The growGrass method only grows grass, not random animated decor.
    def growGrass(worldx,worldy,streams,obstacles,worldGraphics):
        newgrass = classes.Animated(worldGraphics['decor']['grass'],worldGraphics['decor_night']['grass'],(random.randint(0,worldx),random.randint(0,worldy)),decorations)
        while not safe(newgrass.rect,streams,worldGraphics['stream_coefficients'],obstacles):
            newgrass.pos = (random.randint(0,worldx),random.randint(0,worldy))
            newgrass.rect = newgrass.image.get_rect(topleft=newgrass.pos)
    # The quantities of flowers and grass are also not on a bell curve.
    for i in range(random.randint(30,60)):
        growFlower(worldx,worldy,streams,obstacles,worldGraphics)
    for i in range(random.randint(20,40)):
        growGrass(worldx,worldy,streams,obstacles,worldGraphics)
    
    # Keyword:  FOOTPRINTS.  Code to add prints should be added somewhere around here.

    # STEP 5
    # Add the wolves' den and the farm to the world.
    settlements = pygame.sprite.Group()
    def digDen(worldx,worldy,screen_dims,streams,worldGraphics):
        # Because wolves' dens are typically located near streams, the
        # method attempts to place it above a stream object.  Because the streams
        # are kept in a pygame Group, and not a list as in PrototypeGame, 
        # random.choice(streams) does not work.
        arbpos = (random.randint(screen_dims[0],worldx-screen_dims[0]),random.randint(screen_dims[1],worldy-screen_dims[1]))
        den = classes.Den(worldGraphics['misc']['den'],worldGraphics['misc_night']['den'],arbpos,settlements)
        a = 2
        for s in streams:
            # Instead, every stream segment is iterated through, with a random chance of the den placing
            # over it.  If the den is not near the world's edge, then it is acceptable.
            if random.random() < 6/len(streams) or a == len(streams):
                if screen_dims[0] / 2 < s.rect.left < worldx - screen_dims[0] and screen_dims[1] < s.rect.top < worldy - screen_dims[1]:
                    den.pos = (s.pos[0],s.pos[1] - den.image.get_height()//2)
                    den.rect = den.image.get_rect(topleft=den.pos)
                    if safe(den.rect,streams,worldGraphics['stream_coefficients'],obstacles):
                        return
            a += 1
        # To account for obstacles, they are removed.
        pygame.sprite.spritecollide(den,obstacles,True) # dokill = True (remove all sprites in the way)
        # The Farm object is placed in a random corner of the world, and all objects that collide with it
        # are destroyed.
    def buildFarm(worldx,worldy,worldGraphics):
        farm = classes.Farm(worldGraphics['misc']['farm'],worldGraphics['misc']['farm'],(0,0),settlements)
        if random.random() > 0.5:
            farm.pos = (farm.pos[0],worldy-farm.image.get_height())
        if random.random() > 0.5:
            farm.pos = (worldx-farm.image.get_width(),farm.pos[1])
        farm.rect = farm.image.get_rect(topleft=farm.pos)
        for each_group in [streams,obstacles,decorations]:
            pygame.sprite.spritecollide(farm,each_group,True)
    # There are only one den and one farm.
    digDen(worldx,worldy,screen_dims,streams,worldGraphics)
    buildFarm(worldx,worldy,worldGraphics)
    
    # STEP 6
    # Add non-player animals.
    animals = pygame.sprite.Group()

    # The collides method exists because pygame's built-in collision functions
    # require the .rect attribute, not the .collision_rect.  It checks if an 
    # example pygame Rect object collides with any obstacle.
    def collides(test_rect,obstacles):
        for ob in obstacles:
            if test_rect.colliderect(ob.collision_rect):
                return True
        return False
    # The new_animal_pos method attempts to find a spot in the world where
    # a rectangle of the given width and height does not collide with any obstacle.
    def new_animal_pos(dims,obstacles):
        newpos = (random.randint(screen_dims[0]//2,worldx-screen_dims[0]//2),random.randint(screen_dims[1]//2,worldy-screen_dims[1]//2))
        test_rect = pygame.Rect(newpos[0],newpos[1],dims[0],dims[1])
        attempts = 0
        # It makes six random attempts, and otherwise returns None.
        while collides(test_rect,obstacles) and attempts < 6:
            newpos = (random.randint(screen_dims[0]//2,worldx-screen_dims[0]//2),random.randint(screen_dims[1]//2,worldy-screen_dims[1]//2))
            test_rect = pygame.Rect(newpos[0],newpos[1],dims[0],dims[1])
            attempts += 1
        if attempts < 6:
            return newpos
    
    # The population dictionary begins with all animals at 0 and changes as new animals are added.
    population_dict = {'rabbit':0,'deer':0,'fox':0,'wolf':0,'bison':0}
    DIMS = worldGraphics['animals']['rabbit'][0][0].get_width(), worldGraphics['animals']['rabbit'][0][0].get_height()
    for r in range(random.randint(10,20)):
        newpos = new_animal_pos(DIMS,obstacles)
        if newpos != None:
            classes.Rabbit(worldGraphics['animals']['rabbit'],worldGraphics['animals']['rabbit'],newpos,animals)
            population_dict['rabbit'] += 1
    DIMS = worldGraphics['animals']['deer'][0][0].get_width(), worldGraphics['animals']['deer'][0][0].get_height()
    for d in range(random.randint(5,8)):
        newpos = new_animal_pos(DIMS,obstacles)
        if newpos != None:
            classes.Deer(worldGraphics['animals']['deer'],worldGraphics['animals']['deer'],newpos,animals)
            population_dict['deer'] += 1
    DIMS = worldGraphics['animals']['fox'][0][0].get_width(), worldGraphics['animals']['fox'][0][0].get_height()
    for d in range(random.randint(2,4)):
        newpos = new_animal_pos(DIMS,obstacles)
        if newpos != None:
            classes.Fox(worldGraphics['animals']['fox'],worldGraphics['animals']['fox'],newpos,animals)
            population_dict['fox'] += 1
    DIMS = worldGraphics['animals']['bison'][0][0].get_width(), worldGraphics['animals']['bison'][0][0].get_height()
    for d in range(1):
        newpos = new_animal_pos(DIMS,obstacles)
        if newpos != None:
            classes.Bison(worldGraphics['animals']['bison'],worldGraphics['animals']['bison'],newpos,animals)
            population_dict['bison'] += 1

    # STEP 7
    # Add non-player wolves.
    DIMS = worldGraphics['wolves'][0][0][0].get_width(), worldGraphics['wolves'][0][0][0].get_height()
    for d in range(6-chapter): # Make 4 attempts in the second chapter, 3 in the third.
        newpos = new_animal_pos(DIMS,obstacles)
        if newpos != None:
            name = random.choice(range(len(WOLF_NAMES)))
            while name == character: # Pick a wolf that isn't the player.
                name = random.choice(range(len(WOLF_NAMES)))
            classes.Wolf(worldGraphics['wolves'][name],worldGraphics['wolves'][name],newpos,menuGraphics['wolf_portrait_'+str(name)],animals)
            population_dict['wolf'] += 1
    if chapter == 3:
        name = random.choice(range(len(list(WOLF_FEMALE))))
        while WOLF_FEMALE[list(WOLF_FEMALE)[name]] == WOLF_FEMALE[list(WOLF_FEMALE)[character]]:
            name = random.choice(range(len(list(WOLF_FEMALE))))
        mate = classes.Wolf(worldGraphics['wolves'][name],worldGraphics['wolves'][name],newpos,menuGraphics['wolf_portrait_'+str(name)],animals)
        population_dict['wolf'] += 1

    # STEP 8
    # Add player.
    newpos = (random.randint(screen_dims[0]//2,worldx-screen_dims[0]//2),random.randint(screen_dims[1]//2,worldy-screen_dims[1]//2))
    if player == None:
        player = classes.Player(worldGraphics['wolves'][character],worldGraphics['wolves'][character],newpos,menuGraphics['wolf_portrait_'+str(character)],animals)
    else:
        player.transport(newpos)
    population_dict['wolf'] += 1
    while collides(player.collision_rect,obstacles):
        player.transport((random.randint(screen_dims[0]//2,worldx-screen_dims[0]//2),random.randint(screen_dims[1]//2,worldy-screen_dims[1]//2)))
    
    # STEP 9
    # Make world (possible with mate object)
    if chapter != 3:
        my_world = classes.World(screen_dims,background,nightbackground,streams,forest,rocks,decorations,settlements,animals,player,population_dict)
    else:
        my_world = classes.World(screen_dims,background,nightbackground,streams,forest,rocks,decorations,settlements,animals,player,population_dict,mate)
    
    # STEP 10
    # Arrange world (because of how Pygame group works, this requires the world to be made first.)
    for everything in my_world.objects:
        if not isinstance(everything,classes.Stream):
            my_world.change_layer(everything,everything.rect.bottom)
    
    return my_world