# Overlay contains Pygame code to display menus, textboxes, etc
# created 10/20/12 
###################################################################

import pygame

class TextBox:
    def __init__(self, surface, font, color, textcolor, bcolor, position, size): # position: (x, y) # size (width, height)
        self.surface = surface
        self.font = font
        self.color = color # should be in (r, g, b) format
        self.borderColor = bcolor # should be in (r, g, b) format
        self.rect = pygame.Rect ( position, size )
        self.borderRect = pygame.Rect((0+1,0+1), (780-2, 190-2))
        self.textcolor = textcolor
        self.linepacing = 0
        self.textMargin = 10
        self.lineWidth = size[0]-self.textMargin*2

    def splitMessage( self, message_text ):
        lineList = []   # lists of lines to be returned and rendered
        temp = ""       # temp holding place for lines
        
        # Word-wrap
        while len(message_text) > 0:
            ch = message_text[0]
            message_text = message_text[1:]
            
#            if ch == '\n'.:
#                lineList += temp
#               temp = ""
#                continue
            
            temp += ch
            
            #if we've reached the max size of a line
            if self.font.size(temp)[0] > self.lineWidth:
                ch = temp[-1] 
                
                # go backwards until we find a space to break the line correctly
                while ch <> " ":
                    ch = temp[-1] 
                    temp=temp[:-1]
                    message_text = ch + message_text
                
                # add the line to the list and reset the temp
                #print temp.strip()
                lineList += [temp.strip()]
                temp = ""
        lineList += [temp.strip()]
              
        return lineList
            
    def showTextOnly(self, message_text):
        # Textbox background
        tb_surface = pygame.Surface(self.rect.size)
        tb_surface.fill(self.color)
        tb_surface.set_alpha(200)
        
        # Textbox Border
        pygame.draw.rect(tb_surface, self.borderColor, self.borderRect, 1 )
        
        
        # Text Display: Need to add word-wrapping
        spacing = self.font.size("ABC")[1]+ self.linepacing
        i = 0
        
        for line in self.splitMessage(message_text):
            label = self.font.render(line, 1, self.textcolor)
            tb_surface.blit(label, (self.textMargin, i*spacing+self.textMargin))
            i+=1
            
        # Blit to screen surface
        self.surface.blit(tb_surface, self.rect)
        
