###################################################################
# Overlay contains Pygame code to display menus, textboxes, etc
# created 10/20/12 
###################################################################

import pygame, settings, Queue
from input import Input

class InterruptEvent:
    """Interrupt Events are events that occur in the UI such as a text box that must be dismissed before 
    other game logic can continue"""
    def __init___ (self):
        pass
    def Show(self):
        print "Show() not implemented."
    
class NotificationBox(InterruptEvent):
    """Item Procured, etc"""
    def __init__(self, destinationSurface, font, message, position=settings.NOTIFICATION_BOX_POSITION, size=settings.NOTIFICATION_BOX_SIZE, bgcolor=settings.TEXTBOX_COLOR, textcolor=settings.TEXTBOX_TEXT_COLOR, borderColor=settings.TEXTBOX_BORDER_COLOR, opacity=settings.TEXTBOX_OPACITY):
        """Setup for Notification Box """
        self.destinationSurface = destinationSurface # eg. the screen
        self.font = font # pygame font object
        
        self.bgcolor = bgcolor # should be in (r, g, b) format
        self.borderColor = borderColor # should be in (r, g, b) format
        self.textcolor = textcolor
        self.opacity = opacity
        
        self.textMargin = settings.NOTIFICATION_BOX_TEXT_MARGIN
        
        # Set size based on message size
        self.size = (self.font.size(message)[0] + self.textMargin*2, size[1])
        self.tempSurface = pygame.Surface(self.size)
        
        #Set position based on size
        self.position = (destinationSurface.get_width()/2-self.size[0]/2, position[1]) 
        
        self.rect = pygame.Rect ( self.position, self.size )
        self.borderRect = pygame.Rect((2,2), (self.size[0]-4, self.size[1]-4))
        self.DrawNotification(message)
        
    def DrawNotification(self, message):
        
        
        self.DrawBoxToTempSurface()
        self.DrawTextToTempSurface(message)
    
    def DrawBoxToTempSurface(self):
        """Draws the TextBox background and border to a temporary Surface to be displayed
        with shown"""
        # Notification background
        self.tempSurface.fill(self.bgcolor)
        self.tempSurface.set_alpha(self.opacity)
        
        # Notification Border
        pygame.draw.rect(self.tempSurface, self.borderColor, self.borderRect, 2 )
        
    # Sets the text and draws it to a surface to be used
    def DrawTextToTempSurface(self, message_text):
        """Draws only the words of the textbox to the temporary surface"""
        label = self.font.render(message_text, 1, self.textcolor)
        self.tempSurface.blit(label, (self.textMargin, self.textMargin))
    
    
    def Show(self):
        self.destinationSurface.blit(self.tempSurface, self.rect)
    
class TextBox(InterruptEvent):
    def __init__(self, destinationSurface, font, portrait, message, position=settings.TEXTBOX_POSITION, size=settings.TEXTBOX_SIZE, bgcolor=settings.TEXTBOX_COLOR, textcolor=settings.TEXTBOX_TEXT_COLOR, borderColor=settings.TEXTBOX_BORDER_COLOR, opacity=settings.TEXTBOX_OPACITY):
        """Does all the set up for the look and position of the TextBox 
        on the screen. Message is set separately. Idea: Create one textbox for the game, and
        reuse it as many times as needed by resetting the text and then calling Show()."""
        
        self.destinationSurface = destinationSurface # eg. the screen
        self.tempSurface = pygame.Surface(size) #holding place to be displayed
        self.font = font # pygame font object
        self.bgcolor = bgcolor # should be in (r, g, b) format
        self.borderColor = borderColor # should be in (r, g, b) format
        self.rect = pygame.Rect ( position, size )
        self.borderRect = pygame.Rect((1,1), (size[0]-2, size[1]-2))
        self.textcolor = textcolor
        self.linepacing = 0
        self.textMargin = 10
        self.lineWidth = size[0]-self.textMargin*2
        self.portrait = None #this will contain an image if chosen to
        self.opacity = opacity
        self.NewDialog(portrait, message)
        
    def SplitMessage( self, message_text ):
        """Does the word-wrap logic for the message to be displayed"""
        lineList = []   # lists of lines to be returned and rendered
        temp = ""       # temp holding place for lines
        
        temp_line_width = self.lineWidth
        
        if (self.portrait is not None):
            temp_line_width -= self.portrait.get_width()
        
        # Word-wrap
        while len(message_text) > 0:
            ch = message_text[0]
            message_text = message_text[1:]
            
            # TODO: Allow hard returns in message_text contents
            if ch == '\n':
                lineList += [temp.strip()]
                temp = ""
                continue
            
            temp += ch
            
            #if we've reached the max size of a line
            if self.font.size(temp)[0] > temp_line_width:
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
    
    def SetText(self, message_text):
        """Used to set the message to be seen when the TextBox is displayed."""
        self.DrawBoxToTempSurface()
        
        if self.portrait is not None:
            self.DrawPortraitToTempSurface()        
        
        self.DrawTextToTempSurface(message_text)

    def SetPortrait(self, filename=None):
        """Sets the portraitImage"""
        if filename is None:
            self.portrait = None
        else:
            self.portrait = pygame.image.load("../gfx/portraits/" + filename)
        
    def NewDialog(self, image_filename, message_text):
        """Dialog in the sense of a character speaking. Accompanied by a portrait image."""
        self.SetPortrait(image_filename)
        self.SetText(message_text)
        return self
        
    def DrawPortraitToTempSurface(self):
        portloc = (self.textMargin,self.textMargin/2)
        self.tempSurface.blit(self.portrait, portloc)
        
    # Sets the text and draws it to a surface to be used
    def DrawTextToTempSurface(self, message_text):
        """Draws only the words of the textbox to the temporary surface"""
        spacing = self.font.size("ABC")[1]+ self.linepacing
        i = 0

        portrait_margin = 0
        if self.portrait is not None:
            portrait_margin = self.portrait.get_width()+self.textMargin

        for line in self.SplitMessage(message_text):
            label = self.font.render(line, 1, self.textcolor)
            self.tempSurface.blit(label, (self.textMargin+portrait_margin, i*spacing+self.textMargin))
            i+=1
      
    def DrawBoxToTempSurface(self):
        """Draws the TextBox background and border to a temporary Surface to be displayed
        with shown"""
        # Textbox background
        self.tempSurface.fill(self.bgcolor)
        self.tempSurface.set_alpha(self.opacity)
        
        # Textbox Border
        pygame.draw.rect(self.tempSurface, self.borderColor, self.borderRect, 1 )

    def Show(self):
        """Displays the textbox that has been created"""
        self.destinationSurface.blit(self.tempSurface, self.rect)

class TextBoxEvent(InterruptEvent):
    def __init__(self, portrait, message):
        pass

class InterruptEventSystem:
    """Handles interrupt Event functionality and user interaction for the main game loop"""

    def __init__(self, windowSurfaceObject):
        self.windowSurfaceObject = windowSurfaceObject
        self.currentEvent = None
        self.eventQueue = Queue.Queue()

    def Display(self):
        """Put this in the main game loop. Will only display if the textbox has focus."""
        if self.HasActiveEvent():
            self.currentEvent.Show()

    def Dismiss(self):
        """Dismisses textbox by setting it's focus to false"""
        self.currentEvent = None
    
    def HasActiveEvent(self):
        return self.currentEvent <> None
    
    def Update(self):
        if self.currentEvent == None and not self.eventQueue.empty():
            self.currentEvent = self.eventQueue.get()
            print "DEBUG: getting from queue"

    # depricated!
    def GetInput(self):
        """DEPRICATED: Works for pygame in general. But functionality has been replaced in the input.py file"""
        if Input.keyboard[pygame.K_RETURN]:
            self.currentEvent = None

    # Truly polymorphic as opposed to separate addTextBox and addNotificationBox Classes
    def Add(self, eventObject):
        self.eventQueue.put(eventObject)

class TextBoxHelper(object):
	Instance = None
	def __init__(self, surface, interruptEvents, textboxFont=None, notificationFont=None):
		TextBoxHelper.Instance = self
		self.surface = surface
		self.interruptEvents = interruptEvents
		self.textboxFont = textboxFont
		self.notificationFont = notificationFont
		if notificationFont is None:
			self.notificationFont = pygame.font.Font('freesansbold.ttf', settings.NOTIFICATION_FONT_SIZE)		
		if textboxFont is None:
			self.textboxFont = pygame.font.Font('freesansbold.ttf', settings.TEXTBOX_FONT_SIZE)		
		
	def TextBox(self, portrait=None, text=""):
		self.interruptEvents.Add(TextBox(self.surface, self.textboxFont, portrait, text))
		
	def Notification(self, text=""):
		self.interruptEvents.Add(NotificationBox(self.surface, self.notificationFont, text))
		