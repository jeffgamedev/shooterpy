import pygame, settings
from InterruptEvent import InterruptEvent

class NotificationBox(InterruptEvent):

	"""Item Procured, etc"""
	def __init__(self, game, message, position=settings.NOTIFICATION_BOX_POSITION, size=settings.NOTIFICATION_BOX_SIZE, bgcolor=settings.TEXTBOX_COLOR, textcolor=settings.TEXTBOX_TEXT_COLOR, borderColor=settings.TEXTBOX_BORDER_COLOR, opacity=settings.TEXTBOX_OPACITY):
		"""Setup for Notification Box """
		self.font = settings.NOTIFICATION_FONT
		self.eventName = "NotificationBox"
		
		self.destinationSurface = game.gameSurface  # eg. the screen
		
		self.bgcolor = bgcolor  # should be in (r, g, b) format
		self.borderColor = borderColor  # should be in (r, g, b) format
		self.textcolor = textcolor
		self.opacity = opacity
		
		self.textMargin = settings.NOTIFICATION_BOX_TEXT_MARGIN
		
		# Set size based on message size
		self.size = (self.font.size(message)[0] + self.textMargin * 2, size[1])
		self.tempSurface = pygame.Surface(self.size)
		
		# Set position based on size
		self.position = (self.destinationSurface.get_width() / 2 - self.size[0] / 2, position[1]) 
		
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
	