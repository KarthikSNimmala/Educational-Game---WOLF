import pygame
pygame.init()

DEFAULT_FONT = pygame.font.SysFont('constantia',24)
DEFAULT_LARGE_FONT = pygame.font.SysFont('constantia',36)
DEFAULT_TEXT_COLOR = (239,228,176)

# The linebreak function yields a list of image-type objects rendering a line
# of the given text of the appropriate width.
def linebreak(text,width,maxheight=0,font=DEFAULT_FONT,color=DEFAULT_TEXT_COLOR):
    # Begin by converting the text - likely read from a file with line breaks of its own -
    # into a simple long string with single line breaks for paragraphs, less whitespace.
    pars = text.split('\n\n')
    for i in range(len(pars)):
        par = pars[i]
        par = par.replace('\n',' ')
        while '  ' in par:
            par = par.replace('  ',' ')
        pars[i] = par
    text = ' \n '.join(pars)
    # Then look as the text as a series of words, with paragraph breaks considered words.
    words = text.split(' ') # This is NOT equivalent to text.split()
    lines = [] # Lines is a series of images with text rendered in a font.
    line = words[0] # Line is the next words to be rendered.
    if font.render(words[0],True,color).get_width() > width:
        return False         # Linebreak yields false if a word is too long for
    for word in words[1:]:   # the width or the whole exceeds a maximum height.
        if font.render(word,True,color).get_width() > width:
            return False
        linextend = ' '.join([line,word])
        if word == '\n': # At paragraph breaks, end the line without adding the 'word'.
            lines.append(font.render(line,True,color))
            line = ''
        elif font.render(linextend,True,color).get_width() > width:
            lines.append(font.render(line,True,color))
            line = word # When adding a word would go beyond the width, end the line and start anew.
        else:
            line = linextend
    lines.append(font.render(line,True,color))
    lineheight = lines[0].get_height()
    if maxheight > 0 and lineheight*len(lines) > maxheight:
        return False
    else:
        return lines

# Bliterate takes a text string, line-breaks it, and blits it.
# It yields the y-position ideal for blitting text beneath it,
# as well as the width of the text block.
# Buffer here is used between lines and between block edges - the
# dialog method has its own buffers.
def bliterate(screen,text,x,y,width,height=0,justify=False,outerbuffer=0,buffer=0,font=DEFAULT_FONT,color=DEFAULT_TEXT_COLOR):
    lines = linebreak(text,width-2*outerbuffer,height-2*outerbuffer,font,color)
    widths = []
    if lines == False: # Display error for lines if word too wide or text too tall.
        screen.blit(font.render('Error',True,(255,0,0)),(x,y))
    else:
        runningheight = y + outerbuffer
        change = int(lines[0].get_height() + buffer / 2)
        for line in lines:
            if justify:
                screen.blit(line,(int(x+(width-line.get_width())/2),runningheight))
            else:
                screen.blit(line,(x+outerbuffer,runningheight))
            widths.append(line.get_width())
            runningheight += change
    return runningheight, max(widths)
