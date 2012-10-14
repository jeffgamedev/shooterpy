############################################################
# File:		game.py
# Project:	Shooter 1, II
# Date Created:	Oct 13, 2012	
#
# Description: 	This file is the main entrance point of the
#	Game. Everything else is managed or called from here.
#	As much pygame specific code as possible should be
#	kept in here and out of other files/classes.
#
# NOTE:
# What I've put in here so far is basically going of the python
#	Cheat Sheet which can be found here:
#	http://inventwithpython.com/pygamecheatsheet.png
############################################################

import pygame, sys
import settings # for constants, etc
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()

windowSurfaceObject = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

pygame.display.set_caption('Shooter 1, II')
fontObj = pygame.font.Font('freesansbold.ttf', 32)
msg = 'Hello World'

background_color = pygame.Color( 0, 0, 0)

while True: # primary game loop
	windowSurfaceObject.fill(background_color)
	pygame.display.update()
	fpsClock.tick(30);

	# USER INPUT:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
