import pygame
from worldgeneration import *
import math
from menus import dialog, akela
from dialog import bliterate
from graphics import WOLF_NAMES
from classes import *

# This file contains one function, play, which is equivalent to one chapter in the game.
# Its inputs are chapter (the integer 1, 2, or 3), character (also a number, corresponding
# to position in the WOLF_NAMES dictionary), screen (the screen object is the display window),
# the menuGraphics and worldGraphics dictionaries (passing them as arguments keeps them from
# needing to be recompiled), the timer object (from main.py, like the screen), and, in cases
# where the user comes from a previous chapter and brings a character with an assigned
# appearance and health, a Player object as player.

# Its output is the Player object, with its new health, speed, etc., if the player 
# chooses to move on to the next chapter.  If the player chooses to return to the main
# menu, the output is the integer 0.  If the close button is clicked, the output is -1.

# The structure of this function is a bit of preamble, wherein the world and certain conditions
# are set-up, and a mainloop, which includes the world's "turn" command (see the end of classes.py)
# and a lot of chapter-dependent condition checks, including all of the dialogue.

def play(chapter,character,screen,menuGraphics,worldGraphics,timer,player=None):

    # Generate the world using the method in world_generation.py:
    S_WIDTH, S_HEIGHT = screen.get_width(), screen.get_height()
    if player == None:
        play_world = generate_world((S_WIDTH,S_HEIGHT),menuGraphics,worldGraphics,chapter,character)
    else:
        play_world = generate_world((S_WIDTH,S_HEIGHT),menuGraphics,worldGraphics,chapter,player=player)
    # A player comes with the world.
    player = play_world.player
    player_name = list(WOLF_NAMES)[character]
    # A mate may be necessary.
    if chapter == 3:
        mate = play_world.mate

    # Set up a group of screen statistics, a health bar (which is a red rectangle in a white one),
    # and a population screen (which uses the "dialog" image and blits populations on it).
    screen_stat_displays = pygame.sprite.Group()
    health_screen = Entity(pygame.Surface((int(S_WIDTH/6+S_WIDTH/150),int(S_HEIGHT/24+S_WIDTH/150))),(int(5*S_WIDTH/6-S_HEIGHT/24-S_WIDTH/300),int(11*S_HEIGHT/12-S_WIDTH/300)),screen_stat_displays)
    health_screen.image.fill((250,250,250))
    pygame.draw.rect(health_screen.image,(250,0,0),pygame.Rect(S_WIDTH//300,S_WIDTH//300,S_WIDTH*player.health/600,S_HEIGHT/24))
    population_screen = Entity(pygame.Surface.copy(menuGraphics['pop_meter_blank']),(0,3*S_HEIGHT//4),screen_stat_displays)
    bliterate(population_screen.image,f"Bison:  {play_world.population_dict['bison']}\n\nDeer:  {play_world.population_dict['deer']}\n\nFoxes:  {play_world.population_dict['fox']}\n\nRabbits:  {play_world.population_dict['rabbit']}\n\nWolves:  {play_world.population_dict['wolf']}",S_WIDTH//48,S_WIDTH//48,S_WIDTH//8)

    # Set up victory conditions for each chapter.
    since_talked = 0
    old_pops = play_world.population_dict.copy()
    # Chapter 1's victory conditions are having met everything in the world.
    if chapter == 1:
        met = {'edge':False,'prey':False,'predator':False,'ignore':False,'human':False}
        staying = False
    # Chapter 2's is finding a wolf or den.  Chapter 3's is a time limit.
    elif chapter == 2:
        seen_wolf = False
    # This function goes through a list of objects (such as that with which the player
    # collides, or those which are visible) and checks for instances of each class in it.
    # It returns a dictionary of a seen object of each kind, so that the object's picture
    # can be used.
    def check_for_animals(visible_list):
        contains = {'prey':False,'predator':False,'ignore':False,'human':False,'wolf':False}
        for each_item in visible_list:
            if isinstance(each_item,Farm):
                contains['human'] = each_item
            elif isinstance(each_item,Bison):
                contains['predator'] = each_item
            elif isinstance(each_item,Fox):
                contains['ignore'] = each_item
            elif isinstance(each_item,Rabbit) or isinstance(each_item,Deer):
                contains['prey'] = each_item
            elif isinstance(each_item,Den) or isinstance(each_item,Wolf):
                contains['wolf'] = each_item
        return contains
    
    # The main loop is here.  Since it is expected to run many times per second, this code
    # is the most in need of being made efficient.
    while True:
        # Check for attempts to exit the game by hitting the close button or escape key.
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return -1
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return -1
        
        # Check which keys (later, buttons) are currently pressed, and find the player's
        # direction accordingly.
        pressed = pygame.key.get_pressed()
        up = pressed[pygame.K_UP]
        down = pressed[pygame.K_DOWN]
        left = pressed[pygame.K_LEFT]
        right = pressed[pygame.K_RIGHT]
        running = pressed[pygame.K_SPACE]
        direction = -1
        if up and not down:
            if right and not left:
                direction = math.pi/4
            elif left:
                direction = 3*math.pi/4
            else:
                direction = math.pi/2
        elif down:
            if right and not left:
                direction = 7*math.pi/4
            elif left:
                direction = 5*math.pi/4
            else:
                direction = 3*math.pi/2
        elif right and not left:
            direction = 0
        elif left:
            direction = math.pi
        else:
            direction = -1
            player.speed = 0
        if direction != -1:
            if running:
                player.speed = player.max_speed
                player.health -= 0.01
            else:
                player.speed = player.max_speed // 2

        # Player is moved
        player.move(play_world.obstacles,direction)

        # World turns
        play_world.turn()
        since_talked += 1
        # World returns list of objects visible on screen, and objects with which the player collides.
        # Since visibility is not important in chapter 3, consider not collecting?
        visible, colliding = play_world.draw(screen)
        # Population meter image re-drawn only when populations change.
        if old_pops != play_world.population_dict:
            old_pops = play_world.population_dict.copy()
            population_screen.image = pygame.Surface.copy(menuGraphics['pop_meter_blank'])
            bliterate(population_screen.image,f"Bison:  {play_world.population_dict['bison']}\n\nDeer:  {play_world.population_dict['deer']}\n\nFoxes:  {play_world.population_dict['fox']}\n\nRabbits:  {play_world.population_dict['rabbit']}\n\nWolves:  {play_world.population_dict['wolf']}",S_WIDTH//48,S_WIDTH//48,S_WIDTH//8)
        # Health bar re-drawn completely, likely a waste of power.
        health_screen.image.fill((250,250,250))
        pygame.draw.rect(health_screen.image,(250,0,0),pygame.Rect(S_WIDTH//300,S_WIDTH//300,S_WIDTH*player.health/600,S_HEIGHT/24))
        
        # Update display, move time.
        screen_stat_displays.draw(screen)
        pygame.display.update()
        timer.tick(FRAMES_PER_SECOND)

        # Check everything the player is touching:
        for touched_obj in colliding:
            # At least, animals besides the player itself.
            if isinstance(touched_obj,Moving) and not isinstance(touched_obj,Player):
                # If the player encounters a wolf (and did not just sniff it), sniff it.
                if isinstance(touched_obj,Wolf):
                    if since_talked > 60:
                        dialog(screen,menuGraphics,"*sniff*",["*sniff*"],touched_obj.portrait)
                        since_talked = 0
                # If the player encounters a stronger creature (bison), player is dead.
                elif touched_obj.strength > player.strength:
                    dialog(screen,menuGraphics,"YOU DIED",["Return to main menu"])
                    return 0
                # Otherwise it is a weaker creature - if the player is in good health,
                # do not attack, because wolves do not hunt for sport.
                elif player.health > 60:
                    if since_talked > 60:
                        dialog(screen,menuGraphics,"I'm not hungry enough to attack this animal.",["Leave it"],touched_obj.image)
                        # If it's dead, get rid of it from the screen with .kill().
                        if touched_obj.dead:
                            touched_obj.kill()
                # Otherwise, player may eat the animal.
                else:
                    player.health = 100
                    touched_obj.die()
        # For most dialogues, victory conditions, etc., check the current chapter.
        # Whether it is more efficient to check the chapter every frame than to have three separate files
        # is unclear; however, the differences in each set of victory conditions make setting them up outside
        # the loop (perhaps as one of three unique objects, each with a check_victory method?) seem difficult.
        if chapter == 1:
            if play_world.age == 1:
                akela(screen,menuGraphics,f"Welcome to the world, {player_name}!",['Press the red button to continue.'])
                akela(screen,menuGraphics,"I am Akela, leader of this pack.  We wolves form packs to help us survive.")
                needs_control = akela(screen,menuGraphics,"Would you like a demonstration of the game's controls?",['No, thank you.','Yes, please!'])
                if needs_control == 1:
                    akela(screen,menuGraphics,f"Sure thing, {player_name}!")
                    akela(screen,menuGraphics,"Use the arrow buttons to move around.")
            elif play_world.age == 150 and needs_control:
                akela(screen,menuGraphics,"Hold the red button to run at your top speed.")
                since_talked = 0
            elif play_world.age == 300 and needs_control:
                akela(screen,menuGraphics,"Explain health bar.")
                since_talked = 0
            elif since_talked > 180:
                contains = check_for_animals(visible)
                if not met['predator'] and contains['predator']:
                    akela(screen,menuGraphics,"Look out!")
                    dialog(screen,menuGraphics,"That's a bison.  They can trample a wolf.",["Wow, I'll look out, then."],contains['predator'].image)
                    met['predator'] = True
                    since_talked = 0
                elif not met['human'] and contains['human']:
                    akela(screen,menuGraphics,"Be careful!")
                    dialog(screen,menuGraphics,"Humans live nearby.",["Remark about humans."],contains['human'].image)
                    met['human'] = True
                    since_talked = 0
                elif not met['ignore'] and contains['ignore']:
                    akela(screen,menuGraphics,"Do you see that?")
                    dialog(screen,menuGraphics,"Those won't hurt us if we leave them alone - so we do.",["Okay"],contains['ignore'].image)
                    met['ignore'] = True
                    since_talked = 0
                elif not met['edge'] and not play_world.safe_focus_rect.collidepoint(player.rect.centerx,player.rect.centery):
                    akela(screen,menuGraphics,"Be careful not to venture beyond the pack's territory.")
                    met['edge'] = True
                    since_talked = 0
                elif (not staying) and met['predator'] and met['prey'] and met['human'] and met['ignore'] and met['edge']:
                    akela(screen,menuGraphics,"You've learned everything a pup should know.")
                    since_talked = 0
                    choice = dialog(screen,menuGraphics,"What do you want to do?",['Form my own pack!','Stay with this pack for the rest of the year.','Return to the main menu.'],player.portrait)
                    if choice == 0:
                        return player
                    elif choice == 1:
                        akela(screen,menuGraphics,"That's quite natural.  Most wolves don't leave the pack until they're two years old.")
                        staying = True
                    elif choice == 2:
                        return 0
                elif contains['prey'] and (not met['prey'] or player.health < 60):
                    akela(screen,menuGraphics,"Looks like you found some food.")
                    since_talked = 0
                    if player.health > 60:
                        dialog(screen,menuGraphics,"Do you want to hunt it?",["No, I'm not hungry."],contains['prey'].image)
                    else:
                        if dialog(screen,menuGraphics,"Do you want to hunt it?",["No, I'm not hungry.","Yes, I am hungry."],contains['prey'].image):
                            akela(screen,menuGraphics,"Then I will call the pack.")
                            for each_animal in play_world.animals:
                                if isinstance(each_animal,Wolf):
                                    maybe_pos = (each_animal.pos[0]/3+2*player.pos[0]/3,each_animal.pos[1]/3+2*player.pos[1]/3)
                                    if play_world.posok(each_animal.collision_rect.move(maybe_pos[0]-each_animal.pos[0],maybe_pos[1]-each_animal.pos[1])):
                                        each_animal.transport(maybe_pos)
                    met['prey'] = True
                if play_world.age == 4*SEASON_LENGTH*DAY_LENGTH*FRAMES_PER_SECOND:
                    if staying:
                        akela(screen,menuGraphics,"You're a year old, and have learned very much.")
                    else:
                        akela(screen,menuGraphics,"You're a year old, having survived your first winter.")
                    choice = dialog(screen,menuGraphics,"Do you want to leave the pack?",['Yes, I will form my own pack!','No, I want to stay.','Return to the main menu.'],player.portrait)
                    if choice == 0:
                        return player
                    elif choice == 1:
                        akela(screen,menuGraphics,"Okay, you can stay with our pack another year.")
                    elif choice == 2:
                        return 0
                elif play_world.age == 8*SEASON_LENGTH*DAY_LENGTH*FRAMES_PER_SECOND:
                    akela(screen,menuGraphics,"You're two years old now.  It's time you found a mate and formed your own pack.")
                    choice = dialog(screen,menuGraphics,"What would you like to do?",["Form my own pack!","Return to the main menu."],player.portrait)
                    if choice == 0:
                        return player
                    else:
                        return 0
        elif chapter == 2:
            if play_world.age == 1:
                akela(screen,menuGraphics,"On behalf of the pack, I wish you well in your search for a new family.")
                akela(screen,menuGraphics,"You'll be hunting alone now, until you find your new den.")
                dialog(screen,menuGraphics,"Akela",["Dens look like this, and are usually found near water."],worldGraphics['misc']['den'])
                since_talked = 0
            elif not seen_wolf and check_for_animals(visible)["wolf"]:
                if since_talked > 30:
                    dialog(screen,menuGraphics,"",['Hey, I think I see something!'],check_for_animals(visible)["wolf"].image)
                    seen_wolf = True 
                    since_talked = 0
            elif seen_wolf and check_for_animals(colliding)["wolf"]:
                obj = check_for_animals(colliding)['wolf']
                if isinstance(obj,Den):
                    dialog(screen,menuGraphics,"",["Friendly howling"],player.portrait)
                    dialog(screen,menuGraphics,"",["Friendly howling back"],menuGraphics['wolf_portrait_'+str(random.choice(range(len(menuGraphics['wolf_name_list']))))])
                else:
                    dialog(screen,menuGraphics,"",["*friendly howling* Would you like to join our pack?"],obj.portrait)
                choice = dialog(screen,menuGraphics,"What do you want to do?",["Join this pack!","Return to the main menu."],player.portrait)
                if choice == 0:
                    return player
                else:
                    return 0
            elif play_world.age == 4*SEASON_LENGTH*DAY_LENGTH*FRAMES_PER_SECOND:
                dialog(screen,menuGraphics,"",["Winter came and went, and I never found a new pack.  I guess I'm a lone wolf forever."],player.portrait)
                dialog(screen,menuGraphics,"",['Return to main menu'])
        else:
            if play_world.age == 1:
                dialog(screen,menuGraphics,"Good morning, mate.",["*friendly howls*"],mate.portrait)
                dialog(screen,menuGraphics,"Describe chapter 3 objectives",["Look up Grace's dialogue when Internet connection better."],play_world.mate.portrait)
            if play_world.age == 4*SEASON_LENGTH*DAY_LENGTH*FRAMES_PER_SECOND:
                dialog(screen,menuGraphics,"YOU WIN",['Return to main menu'])
                return 0
                


            
