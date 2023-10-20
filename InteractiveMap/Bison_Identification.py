#Bison Identification sub-page

def bison_id(): 
    import pygame
    import SpeciesMenu
    import Species_Bison
    
    print("Bison identification is running")
    
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
    text_font = pygame.font.SysFont('Corbel', 15)
    bold_font = pygame.font.SysFont('Corbel', 15, bold = True)

    title = title_font.render('Bison: Identifying Characteristics' , True , color)
    home_button = heading_font.render('Main Menu', True, color)
    back_button = heading_font.render('Back to Bison', True, color)

    while True: 
        for ev in pygame.event.get(): 
          
            if ev.type == pygame.QUIT: 
                pygame.quit() 
              
            #checks if a mouse is clicked 
            if ev.type == pygame.MOUSEBUTTONDOWN: 
                #if the mouse is clicked on the back button (Go back to Bison Page)
                if width - 150 <= mouse[0] <= width and height - 100 <= mouse[1] <= height - 60: 
                    Species_Bison.information()
                
                #if the mouse is clicked on the home button (Go back to main menu)
                if width-150 <= mouse[0] <= width and height - 40 <= mouse[1] <= height: 
                    SpeciesMenu.mainmenu_species()
                  
        # fills the screen with a color 
        screen.fill((60,25,60)) 
      
        # stores the (x,y) coordinates into the variable as a tuple 
        mouse = pygame.mouse.get_pos()

        ### -----------------------------------------------------------------------### 
        # if mouse is hovered over the back button (Go back to Bison page) it changes to lighter shade 
        if  width - 150 <= mouse[0] <= width and height - 100 <= mouse[1] <= height - 60: 
            pygame.draw.rect(screen,mainmenu_color_light,[width - 150, height - 100, 150,40])     
        else: 
            pygame.draw.rect(screen,mainmenu_color_dark,[width - 150, height - 100, 150,40]) 
        
        # if mouse is hovered over tenth button (Return to Main Menu) it changes to lighter shade 
        if  width - 150 <= mouse[0] <= width and height - 40 <= mouse[1] <= height: 
            pygame.draw.rect(screen,mainmenu_color_light,[width - 150, height - 40, 150,40])     
        else: 
            pygame.draw.rect(screen,mainmenu_color_dark,[width - 150, height - 40, 150,40]) 
        ### -------------------------------------------------------------------- ###

        # superimposing the text onto our button  
        screen.blit(title, (50,50))  
        screen.blit(back_button , (width - 142, height - 90)) 
        screen.blit(home_button, (width - 132, height - 30))
        
        # updates the frames of the game 
        pygame.display.update() 
