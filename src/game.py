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
############################################################
import pygame
import settings # for constants, etc
from pygame.locals import *
from map import Map
from input import Input
from overlay import TextBoxHelper, InterruptEventSystem


# game dependencies initiation
pygame.init()
fpsClock = pygame.time.Clock()
gameSurface = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
pygame.display.set_caption('Shooter 1, II')
background_color = pygame.Color( 0, 0, 0)
map = Map()
interruptEvents = InterruptEventSystem(gameSurface)
TextBoxHelper(gameSurface, interruptEvents) #instantiate class to fill static instance
# level setup
map.LoadMap("firstmap.tmx")
pygame.mixer.music.load("../music/igelkott.mod")
pygame.mixer.music.play(1)
map.Update() #fixes the jump at the beginning. would be best to fix the source of the problem tho.

while True: # primary game loop	
	##### LOGIC UPDATES #####
	interruptEvents.Update()
	if not interruptEvents.HasActiveEvent(): # Map Logic does not update while an interrupt event is waiting to be dismissed!
		map.Update()
	Input.Update(interruptEvents)
	##### DISPLAY UPDATES #####	
	map.Render(gameSurface)	
	interruptEvents.Display()
	pygame.display.update()
	#Framerate Regulation
	fpsClock.tick(30);
