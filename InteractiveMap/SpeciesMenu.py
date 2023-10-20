# Import libraries
import pygame  

# Import relavent user defined files
import Species_Bison
import Species_RedFox
import Species_GrayFox
import Species_Turtle
import Species_GrayWolf

def mainmenu_species(): 
    ## DEFINTIONS
    # Initializing the constructor 
    pygame.init() 
    
    # Screen and window information
    res = (1500, 1000)                          # screen resolution 
    screen = pygame.display.set_mode(res)       # opens up a window 
    width = screen.get_width()                  # stores the width of the screen into a variable 
    height = screen.get_height()                # stores the height of the screen into a variable 
  
    # Text and font definitions
    color = (255,255,255)                        # text has color white
    smallfont = pygame.font.SysFont('Corbel',35) # defining a font  
  
    # rendering text for each species for later use
    Bison       = smallfont.render('Bison' , True , color)
    RedFox      = smallfont.render('Red Fox' , True , color)
    GrayFox     = smallfont.render('Gray Fox' , True , color) 
    Turtle      = smallfont.render('Turtle' , True , color)
    GrayWolf    = smallfont.render('Gray Wolf' , True , color)

    # load species icon images
    icon_bison          = pygame.image.load('Icon-Bison.png')
    icon_bison_gray     = pygame.image.load('Icon-Bison-Grayscale.png')
    icon_redfox         = pygame.image.load('Icon-RedFox.png')
    icon_redfox_gray    = pygame.image.load('Icon-RedFox-Grayscale.png')
    icon_grayfox        = pygame.image.load('Icon-GrayFox.png')
    icon_grayfox_gray   = pygame.image.load('Icon-GrayFox-Grayscale.png')
    icon_turtle         = pygame.image.load('Icon-Turtle.png')
    icon_turtle_gray    = pygame.image.load('Icon-Turtle-Grayscale.png')
    icon_graywolf       = pygame.image.load('Icon-GrayWolf.png')
    icon_graywolf_gray  = pygame.image.load('Icon-GrayWolf-Grayscale.png')
    
    ## RUNNING THE GAME
    while True: 
        for ev in pygame.event.get(): #DEFINE EVENT ACTIONS ACCORDING TO TYPE
          
            if ev.type == pygame.QUIT: 
                pygame.quit() 
              
            #checks if a mouse is clicked 
            if ev.type == pygame.MOUSEBUTTONDOWN: 
              
                #if the mouse is clicked on the first button (Bison), OPEN SPECIES PAGE
                if width/4-70 <= mouse[0] <= width/4+70 and 1*height/11 <= mouse[1] <= 1*height/11 + 100: 
                    Species_Bison.information()
            
                #if the mouse is clicked on the second button (Red Fox), OPEN SPECIES PAGE
                if width/3-70 <= mouse[0] <= width/3+70 and 7*height/11 <= mouse[1] <= 7*height/11 + 100: 
                    Species_RedFox.red_fox_information()
            
                #if the mouse is clicked on the third button (Gray Fox), OPEN SPECIES PAGE
                if width/3+70 <= mouse[0] <= width/3+210 and 6*height/11 <= mouse[1] <= 6*height/11 + 80: 
                    Species_GrayFox.information()
            
                #if the mouse is clicked on the fourth button (Turtle), OPEN SPECIES PAGE
                if width/2-70 <= mouse[0] <= width/2+70 and 7*height/11 <= mouse[1] <= 7*height/11 + 80: 
                    Species_Turtle.information()
            
                #if the mouse is clicked on the fifth button (Gray Wolf), OPEN SPECIES PAGE
                if width/2 <= mouse[0] <= width/2+140 and 3*height/11 <= mouse[1] <= 3*height/11 + 100: 
                    Species_GrayWolf.information()
                  
        # Sets the Wolf Park Map as the BACKGROUND 
        map_Image = pygame.image.load('WolfParkMap-Sized.png')
        screen.blit(map_Image, (0, 0))
      
        # stores the (x,y) coordinates of the mouse position into a variable as a tuple 
        mouse = pygame.mouse.get_pos() 

        ### -------------------------------------------------------------------------------------- ### 
        ## IF MOUSE IS HOVERED OVER AN ICON, CHANGE IT TO GRAYSCALE VERSION... 
        # if mouse is hovered over first button (Bison) it changes to lighter shade 
        if  width/4-70 <= mouse[0] <= width/4+70 and 1*height/11 <= mouse[1] <= 1*height/11 + 100:   
            screen.blit(icon_bison_gray, [width/4-70,1*height/11,140,100])      #Grayscale Bison Icon
        else: 
            screen.blit(icon_bison, [width/4-70,1*height/11,140,100])           #Normal Bison Icon
    
        # if mouse is hovered over second button (Red Fox) it changes to lighter shade 
        if  width/3-70 <= mouse[0] <= width/3+70 and 7*height/11 <= mouse[1] <= 7*height/11 + 100: 
            screen.blit(icon_redfox_gray, [width/3-70,7*height/11,140,100])     #Grayscale Red Fox Icon
        else: 
            screen.blit(icon_redfox, [width/3-70,7*height/11,140,100])          #Normal Red Fox Icon

        # if mouse is hovered over first button (Gray Fox) it changes to lighter shade 
        if  width/3+70 <= mouse[0] <= width/3+210 and 6*height/11 <= mouse[1] <= 6*height/11 + 80: 
            screen.blit(icon_grayfox_gray, [width/3+70,6*height/11,140,100])    #Grayscale Gray Fox Icon    
        else: 
            screen.blit(icon_grayfox, [width/3+70,6*height/11,140,100])         #Normal Gray Fox Icon
    
        # if mouse is hovered over first button (Turtle) it changes to lighter shade 
        if  width/2-70 <= mouse[0] <= width/2+70 and 7*height/11 <= mouse[1] <= 7*height/11 + 80:  
            screen.blit(icon_turtle_gray, [width/2-70,7*height/11,140,100])     #Grayscale Turtle Icon 
        else: 
            screen.blit(icon_turtle, [width/2-70,7*height/11,140,100])          #Normal Turtle Icon
    
        # if mouse is hovered over first button (Gray Wolf) it changes to lighter shade 
        if  width/2 <= mouse[0] <= width/2+140 and 3*height/11 <= mouse[1] <= 3*height/11 + 100: 
            screen.blit(icon_graywolf_gray, [width/2,3*height/11,140,140])      #Grayscale Gray Wolf Icon
        else: 
            screen.blit(icon_graywolf, [width/2,3*height/11,140,140])           #Normal Gray Wolf Icon
        ### ----------------------------------------------------------------------------------- ###
      
        # SUPERIMPOSE the text near each species icon 
        screen.blit(Bison , (width/4-40, 1*height/11 + 105)) 
        screen.blit(RedFox , (width/3-55, 7*height/11 + 110)) 
        screen.blit(GrayFox , (width/3+80, 6*height/11 + 80)) 
        screen.blit(Turtle , (width/2-40, 7*height/11 + 80)) 
        screen.blit(GrayWolf , (width/2 + 2, 3*height/11 + 130)) 
      
        # updates the frames of the game 
        pygame.display.update() 