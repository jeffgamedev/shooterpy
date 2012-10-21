## Textbox Examples
## Shows off overlay.py

import pygame, sys, overlay
import settings # for constants, etc
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()

windowSurfaceObject = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

pygame.display.set_caption('Shooter 1, II')
fontObj = pygame.font.Font('freesansbold.ttf', 22)
msg = 'Hello World'

background_color = pygame.Color( 0, 0, 0)

#Testing TextBoxes
mytb = overlay.TextBox(windowSurfaceObject, fontObj, settings.TEXTBOX_COLOR, settings.TEXTBOX_TEXT_COLOR, settings.TEXTBOX_BORDER_COLOR, settings.TEXTBOX_POSITION, settings.TEXTBOX_SIZE)
#print mytb.splitMessage("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris imperdiet sagittis metus, sed sagittis purus tempus nec. Duis imperdiet placerat mi, nec imperdiet nisl volutpat interdum. Sed venenatis justo justo, eget rutrum erat. Integer mauris nunc, tempor in vestibulum ut, malesuada at ipsum. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Morbi facilisis tempus tincidunt. Sed at aliquet arcu. Maecenas massa ipsum, aliquet sed consectetur eu, pretium in felis.");

#overlay.TextBox.splitMessage("The quick brown fox jumped over the sleeping lazy dog")

while True: # primary game loop
	windowSurfaceObject.fill(background_color)
	mytb.showTextOnly( "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris imperdiet sagittis metus, sed sagittis purus tempus nec. Duis imperdiet placerat mi, nec imperdiet nisl volutpat interdum. Sed venenatis justo justo, eget rutrum erat. Integer mauris nunc, tempor in vestibulum ut, malesuada at ipsum. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. ")
	#mytb.showTextOnly('Blane: We must be prepared for the onslaught!')
	
	pygame.display.update()
	fpsClock.tick(30);

	# USER INPUT:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
