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
textbox = overlay.TextBox(windowSurfaceObject, fontObj, settings.TEXTBOX_COLOR, settings.TEXTBOX_TEXT_COLOR, settings.TEXTBOX_BORDER_COLOR, settings.TEXTBOX_POSITION, settings.TEXTBOX_SIZE)
textbox.NewDialog("blane.png", "The day has come to defeat that heinous imposter!")



#print mytb.splitMessage("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris imperdiet sagittis metus, sed sagittis purus tempus nec. Duis imperdiet placerat mi, nec imperdiet nisl volutpat interdum. Sed venenatis justo justo, eget rutrum erat. Integer mauris nunc, tempor in vestibulum ut, malesuada at ipsum. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Morbi facilisis tempus tincidunt. Sed at aliquet arcu. Maecenas massa ipsum, aliquet sed consectetur eu, pretium in felis.");

#overlay.TextBox.splitMessage("The quick brown fox jumped over the sleeping lazy dog")

#portrait = pygame.image.load("../gfx/portraits/blane.png")

while True: # primary game loop
	windowSurfaceObject.fill(background_color)
	textbox.Show()
	
	pygame.display.update()
	fpsClock.tick(30);

	# USER INPUT:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
