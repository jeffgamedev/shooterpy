###################################################################
# Overlay contains Pygame code to display menus, textboxes, etc
# created 10/20/12 
###################################################################

import pygame, settings, Queue

class InterruptEvent:
	"""Interrupt Events are events that occur in the UI such as a text box that must be dismissed before 
	other game logic can continue"""
	def __init___ (self):
		self.tempSurface = None
		self.destinationSurface = None
		self.rect = None
	
	def Show(self):
		"""Does not need to be overridden if the following fields are instantiated."""
		if self.tempSurface == None:
			raise Exception("tempSurface has not yet been instantiated.")
		elif self.destinationSurface == None:
			raise Exception("destinationSurface has not yet been instantiated.")
		elif self.rect == None:
			raise Exception("rect has not yet been instantiated.")
		else:
			self.destinationSurface.blit(self.tempSurface, self.rect)
		

class MenuBox(InterruptEvent):
	"""Single menu box. Can be strung together to create a complex menu system."""
	
	def __init__(self, destinationSurface, positionLeft, positionTop, menuFont, itemsList, methodList):
		"""Constructor."""
		self.eventName = "MenuBox"
		
		if len(itemsList) < 1:
			raise IndexError("Menus must have at least one menu item.")
		if len(itemsList) != len(methodList):
			raise IndexError("You must include a method for each item in the menu choice list.")
		
		self.methodList = methodList
		
		self.bgcolor = settings.TEXTBOX_COLOR
		self.opacity = settings.TEXTBOX_OPACITY
		self.borderColor = settings.TEXTBOX_BORDER_COLOR
		self.pointerGraphic = pygame.image.load("..\\gfx\\menu\\menu_pointer.png")
		
		self.destinationSurface = destinationSurface
		self.menuItems = itemsList
		self.selected = 0
		self.font = menuFont
		self.textcolor = settings.TEXTBOX_TEXT_COLOR
		
		self.textMarginLeft = settings.MENU_BOX_TEXT_MARGIN + 20
		self.textMarginRight = settings.MENU_BOX_TEXT_MARGIN
		self.textMarginY = settings.MENU_BOX_TEXT_MARGIN
		self.pointerMarginLeft = settings.MENU_BOX_TEXT_MARGIN
		
		self.size = self.computeMenuSize()
		self.tempSurface = pygame.Surface(self.size)
		self.rect = ((positionLeft, positionTop), self.size)
		self.borderRect = (1, 1, self.size[0] - 3, self.size[1] - 3)
		
		self.UpdateGraphics()
		

		
	def computeMenuSize(self):
		"""Initial width and height computation based on length of longest menu item and number of items respectively.
		Should only be used in constructor."""
		
		# Height calculations.
		numLines = len(self.menuItems)
		lineHeight = self.font.size("ABC")[1]
		
		# Find longest line.
		maxLineWidth = None
		maxLineChars = 0
		for line in self.menuItems:
			if len(line) > maxLineChars:
				maxLineChars = len(line)
				maxLineWidth = self.font.size(line)[0]
		
		# Final calculations.
		width = self.textMarginLeft + maxLineWidth + self.textMarginRight 
		height = self.textMarginY + lineHeight * numLines + self.textMarginY
		
		return (width, height)
		
	
	def UpdateGraphics(self):
		"""Redraw to temp surface"""
		self.tempSurface.fill(self.bgcolor)
		self.tempSurface.set_alpha(self.opacity)
		
		# Notification Border
		pygame.draw.rect(self.tempSurface, self.borderColor, self.borderRect, 2)
		
		lineHeight = spacing = self.font.size("ABC")[1]
		print "lineheight" , lineHeight
		index = 0
		for line in self.menuItems:
			label = self.font.render(line, 1, self.textcolor)
			self.tempSurface.blit(label, (self.textMarginLeft, self.textMarginY + lineHeight * index))
			if index == self.selected:
				self.tempSurface.blit(self.pointerGraphic, (self.pointerMarginLeft, self.textMarginY + lineHeight * index))
			index += 1
	
	def updateCursorPosition(self, direction):
		"""When the user presses up or down on the keyboard"""
		if direction == "down":
			self.selected += 1
			
			if self.selected >= len(self.menuItems):
				self.selected = 0
			self.UpdateGraphics()
		elif direction == "up":
			self.selected -= 1
			if self.selected < 0:
				self.selected = len(self.menuItems) - 1
			self.UpdateGraphics()
		else:
			raise ValueError("update cursor position only accepts \"up\" and \"down\" for the direction arguemnt.")
	
class NotificationBox(InterruptEvent):
	"""Item Procured, etc"""
	def __init__(self, destinationSurface, font, message, position=settings.NOTIFICATION_BOX_POSITION, size=settings.NOTIFICATION_BOX_SIZE, bgcolor=settings.TEXTBOX_COLOR, textcolor=settings.TEXTBOX_TEXT_COLOR, borderColor=settings.TEXTBOX_BORDER_COLOR, opacity=settings.TEXTBOX_OPACITY):
		"""Setup for Notification Box """
		
		self.eventName = "NotificationBox"
		
		self.destinationSurface = destinationSurface  # eg. the screen
		self.font = font  # pygame font object
		
		self.bgcolor = bgcolor  # should be in (r, g, b) format
		self.borderColor = borderColor  # should be in (r, g, b) format
		self.textcolor = textcolor
		self.opacity = opacity
		
		self.textMargin = settings.NOTIFICATION_BOX_TEXT_MARGIN
		
		# Set size based on message size
		self.size = (self.font.size(message)[0] + self.textMargin * 2, size[1])
		self.tempSurface = pygame.Surface(self.size)
		
		# Set position based on size
		self.position = (destinationSurface.get_width() / 2 - self.size[0] / 2, position[1]) 
		
		self.rect = pygame.Rect (self.position, self.size)
		self.borderRect = pygame.Rect((2, 2), (self.size[0] - 4, self.size[1] - 4))
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
		pygame.draw.rect(self.tempSurface, self.borderColor, self.borderRect, 2)
		
	# Sets the text and draws it to a surface to be used
	def DrawTextToTempSurface(self, message_text):
		"""Draws only the words of the textbox to the temporary surface"""
		label = self.font.render(message_text, 1, self.textcolor)
		self.tempSurface.blit(label, (self.textMargin, self.textMargin))
	
class TextBox(InterruptEvent):
	def __init__(self, destinationSurface, font, portrait, message, position=settings.TEXTBOX_POSITION, size=settings.TEXTBOX_SIZE, bgcolor=settings.TEXTBOX_COLOR, textcolor=settings.TEXTBOX_TEXT_COLOR, borderColor=settings.TEXTBOX_BORDER_COLOR, opacity=settings.TEXTBOX_OPACITY):
		"""Does all the set up for the look and position of the TextBox 
		on the screen. Message is set separately. Idea: Create one textbox for the game, and
		reuse it as many times as needed by resetting the text and then calling Show()."""
		
		self.eventName = "TextBox"
		
		self.destinationSurface = destinationSurface  # eg. the screen
		self.tempSurface = pygame.Surface(size)  # holding place to be displayed
		self.font = font  # pygame font object
		self.bgcolor = bgcolor  # should be in (r, g, b) format
		self.borderColor = borderColor  # should be in (r, g, b) format
		self.rect = pygame.Rect (position, size)
		self.borderRect = pygame.Rect((1, 1), (size[0] - 2, size[1] - 2))
		self.textcolor = textcolor
		self.linepacing = 0
		self.textMargin = 10
		self.lineWidth = size[0] - self.textMargin * 2
		self.portrait = None  # this will contain an image if chosen to
		self.opacity = opacity
		self.NewDialog(portrait, message)
		
	def SplitMessage(self, message_text):
		"""Does the word-wrap logic for the message to be displayed"""
		lineList = []  # lists of lines to be returned and rendered
		temp = ""  # temp holding place for lines
		
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
			
			# if we've reached the max size of a line
			if self.font.size(temp)[0] > temp_line_width:
				ch = temp[-1] 
				
				# go backwards until we find a space to break the line correctly
				while ch <> " ":
					ch = temp[-1] 
					temp = temp[:-1]
					message_text = ch + message_text
				
				# add the line to the list and reset the temp
				# print temp.strip()
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

	def LoadPortrait(self, filename=None):
		"""Sets the portraitImage"""
		if filename is None:
			self.portrait = None
		else:
			self.portrait = pygame.image.load("../gfx/portraits/" + filename)
		
	def NewDialog(self, image_filename, message_text):
		"""Dialog in the sense of a character speaking. Accompanied by a portrait image."""
		self.LoadPortrait(image_filename)
		self.SetText(message_text)
		return self
		
	def DrawPortraitToTempSurface(self):
		portloc = (self.textMargin, self.textMargin / 2)
		self.tempSurface.blit(self.portrait, portloc)
		
	# Sets the text and draws it to a surface to be used
	def DrawTextToTempSurface(self, message_text):
		"""Draws only the words of the textbox to the temporary surface"""
		spacing = self.font.size("ABC")[1] + self.linepacing
		i = 0

		portrait_margin = 0
		if self.portrait is not None:
			portrait_margin = self.portrait.get_width() + self.textMargin

		for line in self.SplitMessage(message_text):
			label = self.font.render(line, 1, self.textcolor)
			self.tempSurface.blit(label, (self.textMargin + portrait_margin, i * spacing + self.textMargin))
			i += 1
	  
	def DrawBoxToTempSurface(self):
		"""Draws the TextBox background and border to a temporary Surface to be displayed
		with shown"""
		# Textbox background
		self.tempSurface.fill(self.bgcolor)
		self.tempSurface.set_alpha(self.opacity)
		
		# Textbox Border
		pygame.draw.rect(self.tempSurface, self.borderColor, self.borderRect, 1)


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
		"""Dismisses the InterruptEvent."""
		self.currentEvent = None
	
	def HasActiveEvent(self):
		"""Returns whether or there is an event waiting to be dismissed"""
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
		"""Adds an event to the queue"""
		self.eventQueue.put(eventObject)

class TextBoxHelper(object):  # TODO: Is this being used?
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

	def MenuBox(self, positionLeft=settings.MENU_BOX_POSITION_LEFT, positionTop=settings.MENU_BOX_POSITION_TOP, optionList=["New Game", "Save Game", "Load Game", "Exit Game"], methodList=[1, 2, 3, 4]):
		self.interruptEvents.Add(MenuBox(self.surface, positionLeft, positionTop, self.notificationFont, optionList, methodList))
		
