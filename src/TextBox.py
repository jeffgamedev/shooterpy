###################################################################
# Overlay contains Pygame code to display menus, textboxes, etc
# created 10/20/12 
###################################################################

import pygame, settings, Queue
from InterruptEvent import InterruptEvent

class TextBox(InterruptEvent):
	def __init__(self, game, portrait, message, position=settings.TEXTBOX_POSITION, size=settings.TEXTBOX_SIZE, bgcolor=settings.TEXTBOX_COLOR, textcolor=settings.TEXTBOX_TEXT_COLOR, borderColor=settings.TEXTBOX_BORDER_COLOR, opacity=settings.TEXTBOX_OPACITY):
		"""Does all the set up for the look and position of the TextBox 
		on the screen. Message is set separately. Idea: Create one textbox for the game, and
		reuse it as many times as needed by resetting the text and then calling Show()."""
		
		self.eventName = "TextBox"
		
		self.destinationSurface = game.gameSurface  # eg. the screen
		self.tempSurface = pygame.Surface(size)  # holding place to be displayed
		self.font = pygame.font.Font('freesansbold.ttf', settings.NOTIFICATION_FONT_SIZE)
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

