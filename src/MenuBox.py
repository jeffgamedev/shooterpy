import pygame, settings, os
from InterruptEvent import InterruptEvent

GFX_PATH = os.path.join('..','gfx','menu')

class MenuBox(InterruptEvent):
	"""Single menu box. Can be strung together to create a complex menu system."""
	
	def __init__(self, game, positionLeft, positionTop, itemsList, methodList):
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

		pointerGraphicPath = os.path.join(GFX_PATH, 'menu_pointer.png')
		self.pointerGraphic = pygame.image.load(pointerGraphicPath)
		
		self.destinationSurface = game.gameSurface
		self.menuItems = itemsList
		self.selected = 0
		self.font = settings.MENU_FONT
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
	