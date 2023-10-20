#Bison Information page
import pygame
#import SendToMain


def information(): 
    print("Bison menu is running")

    # initializing the constructor 
    pygame.init() 
  
    # screen resolution 
    res = (1500, 1000) 
  
    # opens up a window 
    screen = pygame.display.set_mode(res) 
  
    # white color 
    color = (255,255,255) 
  
    # light shade of the button 
    color_light = (170,170,170) 
  
    # dark shade of the button 
    color_dark = (100,100,100) 
  
    # stores the width of the screen into a variable 
    width = screen.get_width() 
  
    # stores the height of the screen into a variable 
    height = screen.get_height() 
  
    # defining fonts 
    title_font = pygame.font.SysFont('Corbel',45) 
    heading_font = pygame.font.SysFont('Corbel',25)
    text_font = pygame.font.SysFont('Corbel', 15)
    bold_font = pygame.font.SysFont('Corbel', 15, bold = True)

    title = title_font.render('Bison' , True , color)

    # Bison Identification Information
    identification_heading = heading_font.render('Identification: ', True, color)
    id1 = text_font.render('Bulls can stand up to 6 ft tall and weigh 2800 pounds.', True, color)
    id2 = text_font.render('Cows can stand up to 4-5 ft tall and weigh 1000 pounds.', True, color)
    id3 = text_font.render('Calves are born bright orange, weighing around 30 - 70 lbs when born.', True, color)
    id4 = text_font.render('        -> Wolves are red-green color blind, so this coloration protect baby bison in the green grass.', True, color)
    id5 = text_font.render('Distinctive hump on shoulders.', True, color)
    id6 = text_font.render('Deep brown fur which can grow very long.', True, color)
    id7 = text_font.render('Bison grow a thick coat in the winter that sheds through spring, giving their coat a "patchy" appearance.', True, color)
    id8 = text_font.render('Very large head with a thick skull.', True, color)
    id9 = text_font.render('All bison have short, curved black horns which can grow to be 2ft long; average 12 - 15 inches.', True, color)
    id10 = text_font.render('       -> Males can be identified by more angular "L" shaped horns', True, color)
    id11 = text_font.render('       -> Females can be identified by more curved "C" shaped horns.', True, color)
    
    # Bison unique traits, behaviors, and abilities Information
    traits_heading = heading_font.render('Unique traits, behaviors, and abilities: ', True, color)
    tr1 = text_font.render('Can run up to 35 mph and jump up to 6ft vertically.', True, color)
    tr2 = text_font.render('If threatened, bison hers form a circle around their vulnerable members (young and elderly usually).', True, color)
    tr3 = text_font.render('        -> They will charge at predators.', True, color)
    tr4 = text_font.render("You can determine a bison's emotional state by its tail.", True, color)
    tr5 = text_font.render('        -> If upset, they raise their tail and arch it. If relaxed, it will just hang down.', True, color)
    tr6 = text_font.render('Bison communicate through smells (especially during breeding season), grunts, and snorts.', True, color)
    tr7 = text_font.render("They have excellent haering and smell, but can't see very well.", True, color)
    tr8 = text_font.render('Bison are matriarchal, with one or more lead cows in a herd.', True, color)
    tr9 = text_font.render('        -> Lead cows make decisions for the herd, guiding them to new grazing reas or gathering them together for safety.', True, color)
    tr10 = text_font.render('Bison use their large heads like snow plows to uncover vegetation in the winter.', True, color)
    tr11 = text_font.render('Bison spar by crashing their heads or horns together, but these interactions are rarely fatal.', True, color)

    # Bison Diet Information
    diet_heading = heading_font.render('Diet: ', True, color)
    diet1 = text_font.render('Herbivores', True, color)
    diet2 = text_font.render('Low growing grasses, weeds, leafy plants', True, color)
    diet3 = text_font.render('Bison forage for about 9-11 hours a day.', True, color)
    diet4 = text_font.render('      -> They graze in the morning', True, color)
    diet5 = text_font.render('      -> They rest and ruminate in the afternoon', True, color)
    diet6 = text_font.render('      -> They continue to rest in the evening', True, color)

    # Bison Habitat Information
    habitat_heading = heading_font.render('Habitat: ', True, color)
    habitat1 = text_font.render('Grasslands and prarie', True, color)

    # Bison Threats Information
    threats_heading = heading_font.render('Threats: ', True, color)
    threats1 = text_font.render('Loss of genetic diversity', True, color)
    threats2 = text_font.render('Loss of natural selection forces', True, color)
    threats3 = text_font.render('Habitat destruction', True, color)
    threats4 = text_font.render('Hunting', True, color)

    # Bison Role in the ecosystem Information
    role_heading = heading_font.render('Role in the Ecosystem: ', True, color)
    role1 = bold_font.render('Keystone species - bison play an essential role in maintaining wild grasslands and praries.', True, color)
    role1_1 = text_font.render('        -> As they forage, bison aerate the soil with their hooves, which helps disperse native seeds.', True, color)
    role2 = bold_font.render('They create mosaics in their habitat by selectively grazing in an area.', True, color)
    role2_2 = text_font.render('        -> They feed on grasses which normally outcompete other plants, allowing new plant species to grow.', True, color)
    role3 = bold_font.render('Wallowing', True, color)
    role3_1 = text_font.render('        -> Herds of bison will wallow (roll) in the same areas, creating large depressions in the Earth.', True, color)
    role3_2 = text_font.render('           These fill with rain water and turn into vernal pools (seasonal pools of water), which ', True, color)
    role3_3 = text_font.render('           provide a breeding ground for insects and other wildlife.', True, color)
    role4 = bold_font.render('They are prey for predators, and their carcasses feed scavengers.', True, color)
    role5 = bold_font.render('Bison are ecologically and culturally significant to the history of North America.', True, color)
    
    # Bison Conservation Status Information
    status_heading = heading_font.render('Conservation Status: ', True, color)
    status1 = text_font.render('IUCN: ', True, color)
    status1_1 = bold_font.render('Near threatened', True, color)
    status2 = text_font.render('DOI supports 19 bison herds in 12 states (total: ~11,000 bison over 4.6 million acres.)', True, color)
    status3 = bold_font.render('Named national mammal of the United States in 2016.', True, color)
    status4 = text_font.render('Bison were hunted en masse by European settlers in the 1800s, nearly resulting in total extinction.', True, color)
    status5 = bold_font.render('Wild bison have not been seen in Indiana since 1808', True, color)
    status5_5 = text_font.render("      -> But, they are featured on the state seal and are a significant part of the state's history", True, color)
    status6 = text_font.render('Bison hunting was essential to many indigenous American cultures, and the over-hunting of bison', True, color)
    status6_6 = text_font.render('      in the 19th century by Europeans negatively impacted people as well as the landscape.', True, color)

    # Bison at Wolf Park
    WolfPark_heading = heading_font.render('Bison at Wolf Park: ', True, color)
    WP1 = text_font.render('10 Plains bison (Thelma, Louise, Wonky, Licky, Muscogee, Bonk, Vamchi, Pretty Patrick, Big John, Aretha).', True, color)
    WP1_1 = text_font.render('        This heard is a good size for the habitat at Wolf Park.', True, color)
    WP2 = text_font.render('Our first two bison were given to the park through a permanent loan from Columbian Park Zoo in 1982.', True, color)
    WP3 = text_font.render('This is a non-reproductive herd and all males are castrated to prevent unwanted breeding.', True, color)

    # How can people protect our Bison?
    protect_heading = heading_font.render('How can people protect Bison?', True, color)
    protect1 = text_font.render("Tell our bison's story and talk about the species", True, color)
    protect2 = text_font.render('Support National Parks and public lands that are home to bison.', True, color)
    protect3 = text_font.render('Call your senators, representatives, and state governor if you live in a state with wild bison', True, color)
    protect3_3 = text_font.render('     ask them to protect the species and their habitat.', True, color)

    # Bison Images
    img = pygame.image.load('bisonImage.jpg')
    img = pygame.transform.scale(img, (200, 140))

    while True: 
        for ev in pygame.event.get(): 
          
            if ev.type == pygame.QUIT: 
                pygame.quit() 
              
            #checks if a mouse is clicked 
            if ev.type == pygame.MOUSEBUTTONDOWN: 
              
                #if the mouse is clicked on the first button (Bison)
                if width/2-70 <= mouse[0] <= width/2+70 and 1*height/11 <= mouse[1] <= 1*height/11 + 40: 
                    print("Here")
                    #SendToMain()
                    pygame.quit()
                  
        # fills the screen with a color 
        screen.fill((60,25,60)) 
      
        # stores the (x,y) coordinates into the variable as a tuple 
        mouse = pygame.mouse.get_pos()

        screen.blit(title , (width/20, 1*height/11 + 5)) 

        #Top left section - Identification
        screen.blit(identification_heading, (width/20, 2*height/11 + 5))
        screen.blit(id1, (width/20, 2*height/11 + 30))
        screen.blit(id2, (width/20, 2*height/11 + 50))
        screen.blit(id3, (width/20, 2*height/11 + 70))
        screen.blit(id4, (width/20, 2*height/11 + 90))
        screen.blit(id5, (width/20, 2*height/11 + 110))
        screen.blit(id6, (width/20, 2*height/11 + 130))
        screen.blit(id7, (width/20, 2*height/11 + 150))
        screen.blit(id8, (width/20, 2*height/11 + 170))
        screen.blit(id9, (width/20, 2*height/11 + 190))
        screen.blit(id10, (width/20, 2*height/11 + 210))
        screen.blit(id11, (width/20, 2*height/11 + 230))

        #Top right section - Unique traits and behaviors
        screen.blit(traits_heading, (width/2, 2*height/11 + 5))
        screen.blit(tr1, (width/2, 2*height/11 + 30))
        screen.blit(tr2, (width/2, 2*height/11 + 50))
        screen.blit(tr3, (width/2, 2*height/11 + 70))
        screen.blit(tr4, (width/2, 2*height/11 + 90))
        screen.blit(tr5, (width/2, 2*height/11 + 110))
        screen.blit(tr6, (width/2, 2*height/11 + 130))
        screen.blit(tr7, (width/2, 2*height/11 + 150))
        screen.blit(tr8, (width/2, 2*height/11 + 170))
        screen.blit(tr9, (width/2, 2*height/11 + 190))
        screen.blit(tr10, (width/2, 2*height/11 + 210))
        screen.blit(tr11, (width/2, 2*height/11 + 230))

        #Middle left section - Diet
        screen.blit(diet_heading, (width/20, 5*height/11 + 5))
        screen.blit(diet1, (width/20, 5*height/11 + 30))
        screen.blit(diet2, (width/20, 5*height/11 + 50))
        screen.blit(diet3, (width/20, 5*height/11 + 70))
        screen.blit(diet4, (width/20, 5*height/11 + 90))
        screen.blit(diet5, (width/20, 5*height/11 + 110))
        screen.blit(diet6, (width/20, 5*height/11 + 130))

        #Middle middle section - habitat
        screen.blit(habitat_heading, (width/2, 5*height/11 + 5))
        screen.blit(habitat1, (width/2, 5*height/11 + 30))

        #Middle right section - threats
        screen.blit(threats_heading, (3*width/4, 5*height/11 + 5))
        screen.blit(threats1, (3*width/4, 5*height/11 + 30))
        screen.blit(threats2, (3*width/4, 5*height/11 + 50))
        screen.blit(threats3, (3*width/4, 5*height/11 + 70))
        screen.blit(threats4, (3*width/4, 5*height/11 + 90))

        #Bottom left section - Bisons Role in the Ecosystem
        screen.blit(role_heading, (width/20, 7*height/11 + 5))
        screen.blit(role1, (width/20, 7*height/11 + 30))
        screen.blit(role1_1, (width/20, 7*height/11 + 50))
        screen.blit(role2, (width/20, 7*height/11 + 70))
        screen.blit(role2_2, (width/20, 7*height/11 + 90))
        screen.blit(role3, (width/20, 7*height/11 + 110))
        screen.blit(role3_1, (width/20, 7*height/11 + 130))
        screen.blit(role3_2, (width/20, 7*height/11 + 150))
        screen.blit(role3_3, (width/20, 7*height/11 + 170))
        screen.blit(role4, (width/20, 7*height/11 + 190))
        screen.blit(role5, (width/20, 7*height/11 + 210))

        #Bottom right section - Conservation status
        screen.blit(status_heading, (width/2, 7*height/11 + 5))
        screen.blit(status1, (width/2, 7*height/11 + 30))
        screen.blit(status1_1, (width/2, 7*height/11 + 50))
        screen.blit(status2, (width/2, 7*height/11 + 70))
        screen.blit(status3, (width/2, 7*height/11 + 90))
        screen.blit(status4, (width/2, 7*height/11 + 110))
        screen.blit(status5, (width/2, 7*height/11 + 130))
        screen.blit(status5_5, (width/2, 7*height/11 + 150))
        screen.blit(status6, (width/2, 7*height/11 + 170))
        screen.blit(status6_6, (width/2, 7*height/11 + 190))

        #Bottom left section - Bison at Wolf Park
        screen.blit(WolfPark_heading, (width/20, 9*height/11 + 50))
        screen.blit(WP1, (width/20, 9*height/11 + 70))
        screen.blit(WP1_1, (width/20, 9*height/11 + 90))
        screen.blit(WP2, (width/20, 9*height/11 + 110))
        screen.blit(WP3, (width/20, 9*height/11 + 130))

        #Bottom right section - How can people protect Bison?
        screen.blit(protect_heading, (width/2, 9*height/11 + 50))
        screen.blit(protect1, (width/2, 9*height/11 + 70))
        screen.blit(protect2, (width/2, 9*height/11 + 90))
        screen.blit(protect3, (width/2, 9*height/11 + 110))
        screen.blit(protect3_3, (width/2, 9*height/11 + 130))

        #Photos
        screen.blit(img, (3*width/4, 50))

        # updates the frames of the game 
        pygame.display.update() 

        #print("Bison2")
