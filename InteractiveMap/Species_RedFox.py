#Red Fox Information page

def red_fox_information(): 
    import pygame
    import SpeciesMenu

    #import SendToMain
    print("Red Fox menu is running")

    # initializing the constructor 
    pygame.init() 
  
    # screen resolution 
    res = (1500, 1000) 
  
    # opens up a window 
    screen = pygame.display.set_mode(res) 
  
    # white color 
    color = (255,255,255) 
  
    # button colors 
    color_light = (170,170,170) 
    color_dark = (100,100,100) 

    # mian menu button colors
    mainmenu_color_dark = (0,0,128)
    mainmenu_color_light = (0,0,198)
  
    # stores the width and height of the screen into variables 
    width = screen.get_width() 
    height = screen.get_height() 
  
    # defining fonts 
    title_font = pygame.font.SysFont('Corbel',45, bold = True) 
    heading_font = pygame.font.SysFont('Corbel',25)
    #text_font = pygame.font.SysFont('Corbel', 15)
    #bold_font = pygame.font.SysFont('Corbel', 15, bold = True)

    title = title_font.render('Red Fox' , True , color)

    # Sub-Page Information
    identification_heading = heading_font.render('Identification', True, color)
    traits_heading = heading_font.render('Unique traits, behaviors, and abilities', True, color)
    diet_heading = heading_font.render('Diet', True, color)
    habitat_heading = heading_font.render('Habitat', True, color)
    threats_heading = heading_font.render('Threats', True, color)
    role_heading = heading_font.render('Role in the Ecosystem', True, color)
    status_heading = heading_font.render('Conservation Status', True, color)
    WolfPark_heading = heading_font.render('Red Foxes and Wolf Park', True, color)
    protect_heading = heading_font.render('How can people protect Bison?', True, color)
    main_menu = heading_font.render('Main Menu', True, color)

    while True: 
        for ev in pygame.event.get(): 
          
            if ev.type == pygame.QUIT: 
                pygame.quit() 
              
            #checks if a mouse is clicked 
            if ev.type == pygame.MOUSEBUTTONDOWN: 
              
                #if the mouse is clicked on the first button (Identification)
                if 20 <= mouse[0] <= 750 and 20 <= mouse[1] <= 60: 
                    pygame.quit()
                
                #if the mouse is clicked on the second button (Unique traits, behaviors, and abilities)
                if width/4 <= mouse[0] <= width/4 + 380 and height/4 <= mouse[1] <= height/4 + 40: 
                    pygame.quit()
                
                #if the mouse is clicked on the third button (Diet)
                if width/2 <= mouse[0] <= width/2+150 and height/6 - 100 <= mouse[1] <= height/6 - 60: 
                    pygame.quit()
                
                #if the mouse is clicked on the fourth button (Habitat)
                if 3*width/4 <= mouse[0] <= 3*width/4 + 150 and height/4 - 40 <= mouse[1] <= height/4: 
                    pygame.quit()
                
                #if the mouse is clicked on the fifth button (Threats)
                if width/8 <= mouse[0] <= width/8 + 150 and height/2 + 50 <= mouse[1] <= height/2 + 90: 
                    pygame.quit()
                
                #if the mouse is clicked on the sixth button (Role in the Ecosystem)
                if width/4-100 <= mouse[0] <= width/4+150 and 3*height/4 <= mouse[1] <= 3*height/4 + 40: 
                    pygame.quit()
                
                #if the mouse is clicked on the seventh button (Conservation Status)
                if width/2-70 <= mouse[0] <= width/2+180 and 3*height/4-140 <= mouse[1] <= 3*height/4 -100: 
                    pygame.quit()
                
                #if the mouse is clicked on the eigth button (Red Foxes and Wolf Park)
                if 3*width/4-70 <= mouse[0] <= 3*width/4+180 and height/2-40 <= mouse[1] <= height/2: 
                    pygame.quit()
                
                #if the mouse is clicked on the ninth button (How can people protect red foxes?)
                if 3*width/4 <= mouse[0] <= 3*width/4 + 350 and 3*height/4 <= mouse[1] <= 3*height/4 + 40: 
                    pygame.quit()
                
                #if the mouse is clicked on the tenth button (Go back to main menu)
                if 3*width/4 <= mouse[0] <= 3*width/4 + 150 and 3*height/4+60 <= mouse[1] <= 3*height/4 + 100: 
                    SpeciesMenu.mainmenu_species()
                    #pygame.quit()
                  
        # fills the screen with a color 
        screen.fill((60,25,60)) 
      
        # stores the (x,y) coordinates into the variable as a tuple 
        mouse = pygame.mouse.get_pos()

        screen.blit(title , (width/2 - 100, height/2 -50)) 

        ### -----------------------------------------------------------------------### 
        # if mouse is hovered over first button (Identification) it changes to lighter shade 
        if  20 <= mouse[0] <= 170 and 20 <= mouse[1] <= 60: 
            pygame.draw.rect(screen,color_light,[20,20,150,40])     
        else: 
            pygame.draw.rect(screen,color_dark,[20,20,150,40]) 
        
        # if mouse is hovered over first button (Unique traits, behaviors and abilities) it changes to lighter shade 
        if  width/4 <= mouse[0] <= width/4 + 380 and height/4 <= mouse[1] <= height/4 + 40: 
            pygame.draw.rect(screen,color_light,[width/4, height/4,380,40])     
        else: 
            pygame.draw.rect(screen,color_dark,[width/4, height/4,380,40]) 
        
        # if mouse is hovered over first button (Diet) it changes to lighter shade 
        if  width/2 <= mouse[0] <= width/2+150 and height/6 - 100 <= mouse[1] <= height/6 - 60: 
            pygame.draw.rect(screen,color_light,[width/2, height/6-100,150,40])     
        else: 
            pygame.draw.rect(screen,color_dark,[width/2, height/6-100,150,40]) 
        
        # if mouse is hovered over first button (Habitat) it changes to lighter shade 
        if  3*width/4 <= mouse[0] <= 3*width/4 + 150 and height/4 - 40 <= mouse[1] <= height/4: 
            pygame.draw.rect(screen,color_light,[3*width/4, height/4 - 40,150,40])     
        else: 
            pygame.draw.rect(screen,color_dark,[3*width/4, height/4 - 40,150,40]) 
        
        # if mouse is hovered over first button (Threats) it changes to lighter shade 
        if  width/8 <= mouse[0] <= width/8 + 150 and height/2 + 50 <= mouse[1] <= height/2 + 90: 
            pygame.draw.rect(screen,color_light,[width/8, height/2+50, 150, 40])     
        else: 
            pygame.draw.rect(screen,color_dark,[width/8, height/2+50,150,40]) 
        
        # if mouse is hovered over first button (Role in Ecosystem) it changes to lighter shade 
        if  width/4-100 <= mouse[0] <= width/4+150 and 3*height/4 <= mouse[1] <= 3*height/4 + 40: 
            pygame.draw.rect(screen,color_light,[width/4-100,3*height/4,250,40])     
        else: 
            pygame.draw.rect(screen,color_dark,[width/4-100,3*height/4,250,40]) 
        
        # if mouse is hovered over first button (Conservation Status) it changes to lighter shade 
        if  width/2-70 <= mouse[0] <= width/2+180 and 3*height/4 - 140 <= mouse[1] <= 3*height/4 -100: 
            pygame.draw.rect(screen,color_light,[width/2-70,3*height/4-140,250,40])     
        else: 
            pygame.draw.rect(screen,color_dark,[width/2-70,3*height/4-140,250,40]) 
        
        # if mouse is hovered over first button (Red Fox at Wolf Park) it changes to lighter shade 
        if  3*width/4-70 <= mouse[0] <= 3*width/4+180 and height/2-40 <= mouse[1] <= height/2: 
            pygame.draw.rect(screen,color_light,[3*width/4-70,height/2-40,250,40])     
        else: 
            pygame.draw.rect(screen,color_dark,[3*width/4-70,height/2-40,250,40]) 
        
        # if mouse is hovered over first button (How can people protect Red Foxes?) it changes to lighter shade 
        if  3*width/4 <= mouse[0] <= 3*width/4+350 and 3*height/4 <= mouse[1] <= 3*height/4 + 40: 
            pygame.draw.rect(screen,color_light,[3*width/4,3*height/4,350,40])     
        else: 
            pygame.draw.rect(screen,color_dark,[3*width/4,3*height/4,350,40]) 
        
        # if mouse is hovered over tenth button (Return to Main Menu) it changes to lighter shade 
        if  3*width/4 <= mouse[0] <= 3*width/4 + 150 and 3*height/4 + 60 <= mouse[1] <= 3*height/4 + 100: 
            pygame.draw.rect(screen,mainmenu_color_light,[3*width/4,3*height/4 + 60,150,40])     
        else: 
            pygame.draw.rect(screen,mainmenu_color_dark,[3*width/4,3*height/4 + 60,150,40]) 
        ### -------------------------------------------------------------------- ###

        # superimposing the text onto our button 
        screen.blit(identification_heading , (30, 30))                  
        screen.blit(traits_heading , (width/4 + 10, height/4 + 10))     
        screen.blit(diet_heading , (width/2 + 50, height/6 - 90))       
        screen.blit(habitat_heading , (3*width/4 + 40, height/4 - 30))  
        screen.blit(threats_heading , (width/8 + 40, height/2 + 60))    
        screen.blit(role_heading , (width/4-80, 3*height/4 +10))        
        screen.blit(status_heading , (width/2-45, 3*height/4 -130))     
        screen.blit(WolfPark_heading , (3*width/4-68, height/2 -30))    
        screen.blit(protect_heading , (3*width/4+20, 3*height/4 + 10)) 
        screen.blit(main_menu, (3*width/4 + 5, 3*height/4 + 65))
        
        # updates the frames of the game 
        pygame.display.update() 

