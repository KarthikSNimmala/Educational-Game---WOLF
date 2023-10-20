import pygame
import math
import random
DAY_LENGTH = 60 # seconds
SEASON_LENGTH = 1 # in-game day/night cycles
FRAMES_PER_SECOND = 30
DEER_BIRTH_TIMES = [0.5*SEASON_LENGTH*DAY_LENGTH*FRAMES_PER_SECOND,0.8*SEASON_LENGTH,DAY_LENGTH*FRAMES_PER_SECOND,1.1*SEASON_LENGTH,DAY_LENGTH*FRAMES_PER_SECOND]
RABBIT_BIRTH_CYCLE = int(4*SEASON_LENGTH*DAY_LENGTH*FRAMES_PER_SECOND/7)

# This module contains all of, and only, the class definitions for the Wolf Adventure game.
# There are no functions in this module (though object methods resemble functions, the use of
# the term 'function' to refer to them is discouraged).

# Most classes have parent classes - the Entity class, which defines a static object that can appear
# on-screen, as in menu objects.  It has two descendants - the Indicator class, which is capable
# of motion, and the Terran class, for in-game-world objects, which will have a different appearance at
# night.  The Terran class makes use of the update() feature.

# At the base of this list is the World class, which is descended from Pygame's Group object
# and contains all objects in the in-game world.

def compress_rect(rec,box):
    return pygame.Rect(int(rec.left+box[0]*rec.width),int(rec.top+box[2]*rec.height),int(rec.width*(box[1]-box[0])),int(rec.height*(box[3]-box[2])))

class Entity(pygame.sprite.Sprite):
    def __init__(self,image,pos,*groups):
        super().__init__(*groups)
        self.image = image 
        self.rect = self.image.get_rect(topleft = pos)
        self.pos = pos

# The indicator entity is the indicator paw used to show what the user
# is selecting in a menu.  Its motion is done by sending it a new position.
class Indicator(Entity):
    def __init__(self,image,pos,*groups):
        super().__init__(image,pos,*groups)
    
    def move(self,newpos):
        self.rect = self.image.get_rect(topleft = newpos)

# The Terran entity is an object in the game's world.  It has at least two
# appearances, day and night, and can be updated at each.
class Terran(Entity):
    def __init__(self,appearance,night_appearance,pos,*groups):
        super().__init__(appearance,pos,*groups)
        self.appearance = appearance
        self.night_appearance = night_appearance
        for each_group in self.groups():
            if isinstance(each_group,World):
                each_group.change_layer(self,self.rect.bottom)
    
    def update(self,why):
        if why == 'day':
            self.image = self.appearance
        elif why == 'night':
            self.image = self.night_appearance
# A non-interactive static decoration object, such as a flower, is a Terran.

class Interactive(Terran):
    def __init__(self,appearance,night_appearance,pos,interactionBox,*groups):
        super().__init__(appearance,night_appearance,pos,*groups)
        self.rect = compress_rect(self.image.get_rect(topleft=pos),interactionBox)
    
    def feel_collision(self):
        print("Player has met with an unspecified interactive object.")

# Prints, along with the hunting mini-game, were removed from the game - but, if
# they are to be returned, the code exists, commented out, marked by the keyword FOOTPRINTS.
# Other code is in graphics.py and worldgeneration.py, code to re-enable the game not written.
#class Print(Interactive): # Appearance should come from dictionary
#    def __init__(self,appearance,pos,animal,*groups):
#        self.animal = animal
#        super().__init__(appearance,appearance,pos,(0.0,1.0,0.0,1.0))

# The Animated entity is an object with a simple looping animation in the
# game's world.  It has two lists of appearances, one for day and night,
# and cycles through each at its own special framerate.
class Animated(Terran):
    def __init__(self,appearance,night_appearance,pos,fps,*groups):
        super().__init__(appearance[0],night_appearance[0],pos,*groups)
        self.appearance = appearance
        self.night_appearance = night_appearance
        self.fps = fps
        self.f = 0
    
    def update(self,why):
        if why == 'day':
            self.image = self.appearance[self.f]
        elif why == 'night':
            self.image = self.night_appearance[self.f]
        elif isinstance(why,int):
            f = math.floor(why * self.fps / FRAMES_PER_SECOND) % len(self.appearance)
            if f != self.f:
                self.f = f 
                if self.image in self.appearance:
                    self.image = self.appearance[f]
                else:
                    self.image = self.night_appearance[f]

class Stream(Animated):
    def __init__(self,appearance,night_appearance,pos,aim,*groups):
        super().__init__(appearance,night_appearance,pos,8,*groups)
        self.aim = aim 
        if len(aim) < 4:
            self.a = int(aim[:2])*math.pi/180 # Angle in radians as float, for straights and sources

    def __str__(self):
        return 'A stream segment of aim ' + self.aim + ' at (' + self.pos[0] + ',' + self.pos[1] + ')'

    # The method "covers" determines whether a point is in the stream.  Was used to keep objects
    # like trees from growing from stream in PrototypeGame.  Rect is used now for efficiency.
    def covers_point(self,point,streamCurveCoefficients): # Curve coefficients come from a dictionary.
        x = point[0] - self.pos[0] # Convert to typical ordinates.
        y = self.pos[1] + self.image.get_height() - point[1]
        if not (0 < x < self.image.get_width() and 0 < y < self.image.get_height()):
            return 'o' # If the point is not in the stream's image, return "o" for outside.
        # For straight streams:
        if self.aim in ['30','45','60']:
            if y < x*math.tan(self.a):
                return 'b' # If beneath the lower bank, return 'b' for below.
            elif y > x*math.tan(self.a) + 50/math.cos(self.a):
                return 'a'# If above the upper bank, return 'a' for above.
            return 'i' # If neither, must be inside - return 'i'.
        # For source lakes:
        elif self.aim[-1] == 's':
            if ((x-self.image.get_width()/2)**2+(y-self.image.get_height()/2)**2)**0.5 < self.image.get_width()/2:
                return "i" # If inside the lake, return 'i'
            elif x > 3*self.image.get_width()/4:
                return "o"
            else:
                if y < x*math.tan(self.a):
                    return "b"
                elif y > x*math.tan(self.a) + 50/math.cos(self.a):
                    return "a"
                return "i"
        # For bends and curves:
        else:
            f, g = streamCurveCoefficients[self.aim]
            if f[0]*x**3 + f[1]*x**2 + f[2]*x + f[3] < y:
                return "a"
            elif y < g[0]*x**3 + g[1]*x**2 + g[2]*x + g[3]:
                return "b"
            return "i"
    
    def covers_rect(self,rect,sCC):
        states = self.covers_point(rect.topleft,sCC) + self.covers_point(rect.topright,sCC) + self.covers_point(rect.bottomleft,sCC) + self.covers_point(rect.bottomright,sCC)
        if "i" in states:
            return True
        elif "a" in states and "b" in states:
            return True 
        return False

class Moving(Animated):
    def __init__(self,appearance,night_appearance,pos,fps,max_speed,max_strength,collision_box,*groups):
        super().__init__(appearance[0],night_appearance[0],pos,fps,*groups)
        self.appearance = appearance
        self.night_appearance = night_appearance
        # Moving objects will not always be animated; as such, the delay between where they
        # would be and where they are must be measured.
        self.behind_frame = 0
        # Initially, all moving things (probably animals) have their highest speed and strength.
        # Both of these properties will be determined in part by species as described in the
        # subclass of each.
        self.max_speed = max_speed
        self.speed = max_speed
        self.max_strength = max_strength
        self.strength = max_strength
        # Because they may not move a whole pixel each frame, exact position is stored as a set of floating points.
        self.float_pos = (float(pos[0]),float(pos[1]))
        self.max_miss_turn = math.pi
        # Initially, animals are alive and not yet eaten.  They face 0 degrees counterclockwise from east.
        self.direction = 0.0
        self.orientation = 0 # Orientations are 0 for east, 1 for north, etc.
        self.dead = False
        self.post_death_age = 0
        # Animals will use rectangular collisions - see obstacles for details.
        self.draw_rect = self.image.get_rect(topleft = self.pos)
        self.collision_box = collision_box
        self.collision_rect = compress_rect(self.image.get_rect(topleft=self.pos),self.collision_box)

    def orient(self): # Figure out orientation (currentmode) from direction.
        if self.direction == -1:
            return 0
        def fix_angle(angle):
            while angle < 0:
                angle += 2*math.pi
            while angle >= 2*math.pi:
                angle -= 2*math.pi
            return angle
        if len(self.appearance) == 4: # Not everyone gets up and down frames yet.
            return fix_angle(self.direction + math.pi/4) // (math.pi/2) # self.direction is counterclockwise from east.
        else:
            return fix_angle(self.direction + math.pi/2) // math.pi

    def posok(self,newpos,obstacles):
        test_rect = self.collision_rect.move(newpos[0]-self.pos[0],newpos[1]-self.pos[1])
        for ob in obstacles:
            if test_rect.colliderect(ob.collision_rect):
                return False 
        return True

    def update(self,why):
        if why == 'day':
            self.image = self.appearance[self.orientation][self.f]
        elif why == 'night':
            self.image = self.night_appearance[self.orientation][self.f]
        elif isinstance(why,int):
            if self.dead:
                return None
            self.orientation = self.orient()
            f = math.floor(why * self.fps / FRAMES_PER_SECOND + self.behind_frame) % len(self.appearance[self.orientation])
            if self.speed != 0 and f != self.f:
                self.f = f 
                if self.image in self.appearance[self.orientation]:
                    self.image = self.appearance[self.orientation][f]
                else:
                    self.image = self.night_appearance[self.orientation][f]
            elif self.speed == 0 and f != self.f:
                self.behind_frame += 1
    
    def transport(self,where):
        self.rect = self.rect.move(int(where[0])-self.pos[0],int(where[1])-self.pos[1])
        self.collision_rect = self.collision_rect.move(int(where[0])-self.pos[0],int(where[1])-self.pos[1])
        self.float_pos = where 
        self.pos = (int(where[0]),int(where[1]))
        for each_group in self.groups():
            if isinstance(each_group,World):
                each_group.change_layer(self,self.rect.bottom)

    def move(self,obstacles,direction):
        if self.dead:
            self.post_death_age += 1
            if self.post_death_age > DAY_LENGTH*FRAMES_PER_SECOND/2:
                self.kill()
            return None
        aim = direction
        x,y = self.float_pos[0] + self.speed*math.cos(direction)/FRAMES_PER_SECOND, self.float_pos[1] - self.speed*math.sin(direction)/FRAMES_PER_SECOND
        while (not self.posok((x,y),obstacles)) and direction < aim + self.max_miss_turn:
            direction += 0.1
            x,y = self.float_pos[0] + self.speed*math.cos(direction)/FRAMES_PER_SECOND, self.float_pos[1] - self.speed*math.sin(direction)/FRAMES_PER_SECOND
        if direction < aim + self.max_miss_turn:
            while direction > math.pi:
                direction -= 2*math.pi
            while direction < -math.pi:
                direction += 2*math.pi
            self.direction = direction
            self.transport((x,y))
    
    def die(self):
        self.dead = True
        self.speed = 0
        self.image = pygame.transform.flip(self.image,False,True)

class Player(Moving):
    def __init__(self,appearance,night_appearance,pos,portrait,*groups):
        super().__init__(appearance,night_appearance,pos,12,960,400,(0.2,0.8,0.6,0.9),*groups)
        self.portrait = portrait
        self.max_miss_turn = math.pi/8
        self.health = 100
    
    def move(self,obstacles,direction):
        if direction != -1:
            super().move(obstacles,direction)

class Rabbit(Moving):
    def __init__(self,appearance,night_appearance,pos,*groups):
        self.direction = 0
        super().__init__(appearance,night_appearance,pos,12,640,50,(0.25,0.75,0.25,0.75),*groups)

    # From a rabbit's perspective, a direction is safe to jump in so long as there are
    # not other animals in that direction inasfar as the rabbit can see (in this case,
    # a section of a circle of radius 400 pixels, width 0.5 radians in either direction
    # from the rabbit's line of sight.)
    def safe(self,animals,direction):
        for animal in animals:
            if not isinstance(animal,Rabbit):
                enemydir = math.atan2(self.pos[1]-animal.pos[1],animal.pos[0]-self.pos[0])
                if -0.5 < enemydir - direction < 0.5:   
                    enemydist = math.sqrt((self.pos[1]-animal.pos[1])**2+(animal.pos[0]-self.pos[0])**2)
                    if enemydist < 400:
                        return False
        return True

    def move(self,obstacles,animals):
        # In the prototypeGame, rabbits changed directions randomly with
        # every frame cycle, as if bouncing randomly.  Since then, I have seen
        # rabbits run in a straight line very well.  As such, rabbits now
        # change direction only between bounces if they observe something unsafe.
        if self.f == 0 and not self.safe(animals,self.direction):
            self.direction = random.random()*2*math.pi
            attempts = 0
            while not self.safe(animals,self.direction) and attempts < 6:
                self.direction = random.random()*2*math.pi
                attempts += 1
            if attempts == 6:
                self.direction = -1 # If rabbit cannot find safe direction, no motion.
        if self.direction != -1:
            super().move(obstacles,self.direction)
        # Heard of rabbits IRL running into briars for safety.  As yet, no
        # briars in the game though, and we'd like rabbits to be the 'easy' prey.
        # The British considered rabbits to be such convenient prey, multiplying quickly
        # and being easy for dogs to catch, that they were introduced to Australia
        # to feed settlers.  This would create a problem.

class Deer(Moving):
    def __init__(self,appearance,night_appearance,pos,*groups):
        self.direction = 0
        super().__init__(appearance,night_appearance,pos,12,800,800,(0.25,0.75,0.25,0.75),*groups)

    def move(self,obstacles,animals):
        # Deer will continue in one direction, turning towards the center of the
        # gap between predators to their left and right.  They can see 500 pixels away.
        directions_to_avoid = []
        for animal in animals:
            if not isinstance(animal,Deer) and not isinstance(animal,Rabbit):
                if math.sqrt((self.pos[0]-animal.pos[0])**2+(self.pos[1]-animal.pos[1])**2) < 500:
                    directions_to_avoid.append(math.atan2(self.pos[1]-animal.pos[1],animal.pos[0]-self.pos[0]))
        if len(directions_to_avoid) > 1:
            directions_to_avoid.sort()
            directions_to_avoid = [directions_to_avoid[-1]-2*math.pi] + directions_to_avoid + [directions_to_avoid[0]+2*math.pi]
            directions_to_avoid.append(self.direction)
            directions_to_avoid.sort()
            point = directions_to_avoid.index(self.direction)
            if point != len(directions_to_avoid) - 1:
                self.direction = ( directions_to_avoid[point-1] + directions_to_avoid[point+1] ) / 2
            else:
                self.direction = ( directions_to_avoid[point-1] + directions_to_avoid[point] ) / 2
        elif len(directions_to_avoid) == 1:
            if directions_to_avoid[0] < math.pi:
                self.direction = directions_to_avoid[0] + math.pi 
            else:
                self.direction = directions_to_avoid[0] - math.pi
        super().move(obstacles,self.direction)

class Bison(Moving):
    def __init__(self,appearance,night_appearance,pos,*groups):
        self.direction = 0
        super().__init__(appearance,night_appearance,pos,12,1440,2000,(0.25,0.75,0.25,0.75),*groups)
    
    # Bison will charge the nearest thing within 500 pixels of them.
    def move(self,obstacles,animals):
        closest_dist = 500
        closest_dir = -1
        for animal in animals:
            if (not isinstance(animal,Bison)) and (not isinstance(animal,Rabbit)) and (not animal.dead):
                enemydist = math.sqrt((self.pos[1]-animal.pos[1])**2+(animal.pos[0]-self.pos[0])**2)
                if enemydist < closest_dist:
                    closest_dist = enemydist
                    closest_dir = math.atan2(self.pos[1]-animal.pos[1],animal.pos[0]-self.pos[0])
        if closest_dir != -1:
            super().move(obstacles,closest_dir)

class Wolf(Moving):
    def __init__(self,appearance,night_appearance,pos,portrait,*groups):
        super().__init__(appearance,night_appearance,pos,12,800,400,(0.2,0.8,0.6,0.9),*groups)
        self.portrait = portrait
        self.health = 100

    def identify(self,animals): # Wolves can tell predators from prey based on
        prey = []               # current strength, which enables them to
        predators = []          # scavenge.  Also, they can smell 1000 pixels away.
        for animal in animals:
            if not isinstance(animal,Wolf) and not isinstance(animal,Player) and math.sqrt((self.pos[1]-animal.pos[1])**2+(animal.pos[0]-self.pos[0])**2) < 1000:
                if animal.strength > self.strength:
                    predators.append(animal)
                else:
                    prey.append(animal)
        return predators, prey

    def move(self,obstacles,animals):
        predators, prey = self.identify(animals)
        if len(predators) > 0: # If predators around, avoid all.
            directions_to_avoid = []
            for predator in predators:
                directions_to_avoid.append(math.atan2(self.pos[1]-predator.pos[1],predator.pos[0]-self.pos[0]))
            if len(directions_to_avoid) == 1: # If one predator, run away.
                direction = directions_to_avoid[0] + math.pi
            else:
                directions_to_avoid.sort() # Otherwise, middle of the widest gap between predators.
                directions_to_avoid.append(directions_to_avoid[0]+2*math.pi)
                gaps = []
                for d in range(len(directions_to_avoid)-1):
                    gaps.append(directions_to_avoid[d+1]-directions_to_avoid[d])
                choice = gaps.index(max(gaps))
                direction = directions_to_avoid[choice] + gaps[choice]/2
        elif len(prey) > 0 and self.health < 60: # If there are prey, and wolf is hungry, aim for the closest.
            distances = []
            for eachprey in prey:
                distances.append((self.pos[0]-eachprey.pos[0])**2+(self.pos[1]-eachprey.pos[1])**2) # Do not take root - just comparing.
            choice = prey[distances.index(min(distances))]
            direction = math.atan2(self.pos[1]-choice.pos[1],choice.pos[0]-self.pos[0])
        else: # If only other wolves, rest.
            direction = -1
            self.health -= 0.005
        if direction != -1:
            self.health -= 0.02
            super().move(obstacles,direction)

class Fox(Moving):
    def __init__(self,appearance,night_appearance,pos,*groups):
        super().__init__(appearance,night_appearance,pos,12,960,200,(0.2,0.8,0.6,0.9),*groups)

    def identify(self,animals): # Fox can tell predators from prey based on
        prey = []               # current strength, which enables them to
        predators = []          # scavenge.  They can smell 600 pixels away.
        for animal in animals:
            if not isinstance(animal,Fox) and math.sqrt((self.pos[1]-animal.pos[1])**2+(animal.pos[0]-self.pos[0])**2) < 600:
                if animal.strength > self.strength:
                    predators.append(animal)
                else:
                    prey.append(animal)
        return predators, prey

    def move(self,obstacles,animals):
        predators, prey = self.identify(animals)
        if len(predators) > 0: # If predators around, avoid all.
            directions_to_avoid = []
            for predator in predators:
                directions_to_avoid.append(math.atan2(self.pos[1]-predator.pos[1],predator.pos[0]-self.pos[0]))
            if len(directions_to_avoid) == 1: # If one predator, run away.
                direction = directions_to_avoid[0] + math.pi
            else:
                directions_to_avoid.sort() # Otherwise, middle of the widest gap between predators.
                directions_to_avoid.append(directions_to_avoid[0]+2*math.pi)
                gaps = [directions_to_avoid[0]+2*math.pi-directions_to_avoid[-1]]
                for d in range(len(directions_to_avoid)-1):
                    gaps.append(directions_to_avoid[d+1]-directions_to_avoid[d])
                choice = gaps.index(max(gaps))
                direction = directions_to_avoid[choice] - gaps[choice]/2
        elif len(prey) > 0: # If there are prey, aim for the closest.
            distances = []
            for eachprey in prey:
                distances.append((self.pos[0]-eachprey.pos[0])**2+(self.pos[1]-eachprey.pos[1])**2) # Do not take root - just comparing.
            choice = prey[distances.index(min(distances))]
            direction = math.atan2(self.pos[1]-choice.pos[1],choice.pos[0]-self.pos[0])
        else: # If only other foxes, rest.
            direction = -1
        if direction != -1:
            super().move(obstacles,direction)

# Objects that impede the player's movement have a special rect.
# A collision box is - in this code - a tuple (a,b,c,d), 0 < a < b < 1,
# 0 < c < d < 1, referring to the portion of the image considered the box.
class Obstacle(Terran):
    def __init__(self,appearance,nightappearance,pos,collision_box,*groups):
        super().__init__(appearance,nightappearance,pos,*groups)
        self.collision_box = collision_box
        self.collision_rect = compress_rect(self.image.get_rect(topleft=self.pos),self.collision_box)

class Rock(Obstacle):
    def __init__(self,appearance,nightappearance,pos,*groups):
        super().__init__(appearance,nightappearance,pos,(0.2,0.8,0.3,0.9),*groups)

class Tree(Obstacle): # The 'appearance' and 'evergreen' states should come from the getTreeGraphics dictionary.
    def __init__(self,appearance,nightappearance,pos,species,evergreen,*groups):
        super().__init__(appearance["summer"][0],nightappearance["summer"][0],pos,(0.4,0.6,0.7,0.9),*groups)
        self.appearance = appearance
        self.night_appearance = nightappearance
        self.type = species
        self.evergreen = evergreen # Collision box for trees is defined here \|/
        self.season = "summer"
        self.fps = 8
        self.f = 0

    def __str__(self):
        return 'A(n) ' + self.type + ' tree at (' + self.pos[0] + ',' + self.pos[1] + ')'
    
    def update(self,why):
        if why in ['winter','autumn'] and not self.evergreen:
            self.season = why
        elif why == 'day':
            self.image = self.appearance[self.season][self.f]
        elif why == 'night':
            self.image = self.night_appearance[self.season][self.f]
        elif isinstance(why,int):
            # Animation of trees is based on a PrototypeGame algorithm which alleges that
            # it is described in a side document somewhere.  Definitely worth looking for where.
            m = 3
            # The expression "math.floor(why * self.fps / FR...OND" refers to how many frames
            # of tree animation the game has preceded through, though the animation's frames repeat
            # in a special pattern.
            t = math.floor(why * self.fps / FRAMES_PER_SECOND) % (8*m)
            # This algorithm assumes a tree animation of length 7, which the middle frame (3) being
            # the default state, and the previous states 0, 1, and 2, and 4, 5, and 6, being reversible
            # animations of the tree moving.  m is the length of those, or the place of the middle frame.
            # The whole animation is of length 8*m.
            if t % (4*m) < 2*m: # If in the first or third quarter of the animation, be middle frame.
                f = m
            elif t < 3*m: # If in the third eighth, go forwards through the second half of the frames.
                f = t - m 
            elif t < 4*m: # If in the fourth eighth, go backwards through them.
                f = 5*m - t 
            elif t < 7*m: # In the seventh eighth, go backwards through the first half of the frames.
                f = 7*m - t
            else:         # In the last eight, go forwards through them.
                f = t-7*m
            if f != self.f: # And update image!
                self.f = f
                if self.image in self.appearance[self.season]:
                    self.image = self.appearance[self.season][self.f]
                else:
                    self.image = self.night_appearance[self.season][self.f]

class Farm(Obstacle): # When in Internet, ensure super() refers to Obstacle!
    def __init__(self,appearance,nightappearance,pos,*groups):
        super().__init__(appearance,nightappearance,pos,(0.0,1.0,0.2,1.0),*groups)
        self.rect = compress_rect(self.image.get_rect(topleft = pos),(-0.3,1.3,-0.3,1.3))

class Den(Interactive):
    def __init__(self,appearance,nightappearance,pos,*groups):
        super().__init__(appearance,nightappearance,pos,(0.25,0.75,0.25,0.75),*groups)
        self.collision_rect = compress_rect(self.image.get_rect(topleft = pos),(0.6,0.8,0.4,0.8))

class World(pygame.sprite.LayeredUpdates):
    def __init__(self,screen_dims,background,nightbackground,streams,forest,rocks,decorations,settlements,animals,player,population_dict,mate=None):
        super().__init__()
        self.S_WIDTH, self.S_HEIGHT = screen_dims
        self.safe_focus_rect = pygame.Rect(screen_dims[0]//2,screen_dims[1]//2,background.get_width()-screen_dims[0],background.get_height()-screen_dims[1])
        self.background = background # Background, which should be scaled to the dimensions of the world.
        self.nightbackground = nightbackground # in its initializer, generateWorld().
        self.width, self.height = self.background.get_width(), self.background.get_height()
        self.currentbackground = self.background
        self.streams = streams # A list of lists of stream segments
        self.forest = forest # A list of trees
        self.rocks = rocks # A list of rocks (really, any obstacles not trees)
        self.decorations = decorations # A list of decoration objects
        self.settlements = settlements # A list of settlement objects
        self.animals = animals # A list of animals, currently excluding the player.
        self.population_dict = population_dict
        
        self.objects = pygame.sprite.Group() # A group of all objects in the world, to be updated for day and night
        self.objects.add(streams,forest,rocks,decorations,settlements,animals)

        self.animates = pygame.sprite.Group() # A group of all animated things, to be updated each tick.
        self.animates.add(streams,forest,animals)

        self.obstacles = pygame.sprite.Group() # A group of all obstacles, against which to check collisions.
        self.obstacles.add(forest,rocks,settlements)

        self.player = player
        self.mate = mate

        self.add(streams,forest,rocks,decorations,settlements,animals)

        self.focus = self.player.rect.center # A coordinate tuple upon which the "camera" focuses.
        self.focus_place = (self.S_WIDTH//2,self.S_HEIGHT//2)
        self.focus_rect = pygame.Rect(self.focus[0]-self.focus_place[0],self.focus[1]-self.focus_place[1],self.S_WIDTH,self.S_HEIGHT)
        
        self.age = 0
    
    def posok(self,test_rect):
        for ob in self.obstacles:
            if test_rect.colliderect(ob.collision_rect):
                return False 
        return True


    def turn(self):
        self.age += 1
        self.animates.update(self.age)
        for animal in self.animals:
            if not isinstance(animal,Player):
                animal.move(self.obstacles,self.animals)
                if pygame.sprite.spritecollideany(animal,self.animals): # Replace this with normal collision box!
                    other = pygame.sprite.spritecollide(animal,self.animals,False)
                    for each in other:
                        if animal.collision_rect.colliderect(each.collision_rect):
                            if animal.max_strength != each.max_strength and each.strength > animal.strength and not(isinstance(each,Player)):
                                animal.strength -= each.strength/10
                                animal.speed -= each.strength/10
                                if (animal.speed < 0 or animal.strength < 0) and not animal.dead:
                                    animal.die()
                                    each.strength = each.max_strength
                                    # Consider re-adding the self.species tag to simplify this?
                                    if isinstance(animal,Rabbit):
                                        self.population_dict['rabbit'] -= 1
                                    elif isinstance(animal,Fox):
                                        self.population_dict['fox'] -= 1
                                    elif isinstance(animal,Deer):
                                        self.population_dict['deer'] -= 1
                                    elif isinstance(animal,Bison):
                                        self.population_dict['bison'] -= 1
                                    elif isinstance(animal,Wolf):
                                        self.population_dict['wolf'] -= 1
                # Code to move animals across the world when they go off the edge.
                if not ( 0 < animal.float_pos[0] < self.width ):
                    if animal.float_pos[0] < 0:
                        animal.transport((animal.pos[0]+self.width,animal.pos[1]))
                    else:
                        animal.transport((animal.pos[0]-self.width,animal.pos[1]))
                    if not self.posok(animal.collision_rect):
                        test_rect = animal.collision_rect.move(0,1)
                        while not self.posok(test_rect):
                            test_rect = test_rect.move(0,1)
                        animal.transport((animal.pos[0],animal.pos[1]+test_rect.bottom-animal.collision_rect.bottom))
                if not ( 0 < animal.float_pos[1] < self.height):
                    if animal.float_pos[1] < 0:
                        animal.transport((animal.pos[0],animal.pos[1]+self.height))
                    else:
                        animal.transport((animal.pos[0],animal.pos[1]-self.height))
                    if not self.posok(animal.collision_rect):
                        test_rect = animal.collision_rect.move(1,0)
                        while not self.posok(test_rect):
                            test_rect = test_rect.move(1,0)
                        animal.transport((animal.pos[0]+test_rect.right-animal.collision_rect.right,animal.pos[1]))

        if self.age % (DAY_LENGTH*FRAMES_PER_SECOND*2) == 0:
            self.objects.update('day')
            self.currentbackground = self.background
        elif self.age % (DAY_LENGTH*FRAMES_PER_SECOND) == 0:
            self.objects.update('night')
            self.currentbackground = self.nightbackground
        if self.age % RABBIT_BIRTH_CYCLE == 0:
            for every_animal in self.animals:
                if isinstance(every_animal,Rabbit) and random.random() > 0.5:
                    test_rect = pygame.Rect(random.randint(0,self.width),random.randint(0,self.height),every_animal.image.get_width(),every_animal.image.get_height())
                    if self.posok(test_rect):
                        self.animals.add(Rabbit(every_animal.appearance,every_animal.night_appearance,test_rect.topleft))
        elif self.age in DEER_BIRTH_TIMES:
            for every_animal in self.animals:
                if isinstance(every_animal,Deer) and random.random() > 0.3:
                    test_rect = pygame.Rect(random.randint(0,self.width),random.randint(0,self.height),every_animal.image.get_width(),every_animal.image.get_height())
                    if self.posok(test_rect):
                        self.animals.add(Deer(every_animal.appearance,every_animal.night_appearance,test_rect.topleft))
        if self.age == 2*SEASON_LENGTH*DAY_LENGTH*FRAMES_PER_SECOND:
            self.forest.update('autumn')
        elif self.age == 3*SEASON_LENGTH*DAY_LENGTH*FRAMES_PER_SECOND:
            self.forest.update('winter')
        if self.focus != self.player.rect.center:
            if self.safe_focus_rect.top < self.player.rect.centery < self.safe_focus_rect.bottom:
                self.focus = (self.focus[0],self.focus[1] + ( self.player.rect.centery - self.focus[1] ) // 2)
            if self.safe_focus_rect.left < self.player.rect.centerx < self.safe_focus_rect.right:
                self.focus = (self.focus[0] + ( self.player.rect.centerx - self.focus[0] ) // 2,self.focus[1])
            self.focus_rect.center = self.focus

    def draw(self, screen): # This method was modified from the original
        # LayeredUpdates draw method, to account for a change in the location to which everything
        # is blitted.  The original can be found at https://github.com/pygame/pygame/blob/main/src_py/sprite.py,
        # line 839 as of 30 October 2022.

        # Include background first
        screen.blit(self.currentbackground,(-self.focus[0]+self.focus_place[0],-self.focus[1]+self.focus_place[1]))
        
        # Commented code was in the original draw method.
        #spritedict = self.spritedict
        #surface_blit = screen.blit
        #dirty = self.lostsprites
        #self.lostsprites = []
        #dirty_append = dirty.append
        #init_rect = self._init_rect
        visible = []
        colliding = []
        for spr in self.sprites():
        #   rec = spritedict[spr]
            if self.focus_rect.colliderect(spr.rect):
                screen.blit(spr.image, spr.rect.move(-self.focus[0]+self.focus_place[0],-self.focus[1]+self.focus_place[1]))
                visible.append(spr)
                if spr.rect.colliderect(self.player.collision_rect):
                    colliding.append(spr)
        #    if rec is init_rect:
        #        dirty_append(newrect)
        #    else:
        #        if newrect.colliderect(rec):
        #            dirty_append(newrect.union(rec))
        #        else:
        #            dirty_append(newrect)
        #            dirty_append(rec)
        #    spritedict[spr] = newrect
        #return dirty
        return visible, colliding

        