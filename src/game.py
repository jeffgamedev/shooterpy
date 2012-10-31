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

import pygame, overlay
import settings # for constants, etc
from pygame.locals import *
from map import Map
from input import Input

pygame.init()
fpsClock = pygame.time.Clock()

windowSurfaceObject = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

pygame.display.set_caption('Shooter 1, II')
fontObj = pygame.font.Font('freesansbold.ttf', 22)
background_color = pygame.Color( 0, 0, 0)

#Testing TextBoxes
interruptEvents = overlay.InterruptEventSystem(windowSurfaceObject)
interruptEvents.AddTextBox("blane.png", "Good day, sir Frog! It appears I have solved the problems with collision detection and entity display! Huzzah! Now we can easily move on to other parts of the game!")
interruptEvents.AddNotificationBox("Pistol Procured!")
map = Map()
map.LoadMap("firstmap.tmx")

Blane = map.AddEntity(170, 150)
Blane.SetControl(True)
map.camera.SetTarget(Blane)
#map.AddEntity(190, 160)
#map.AddEntity(210, 170)
map.AddEntity(240, 180)

pygame.mixer.music.load("../music/igelkott.mod")
pygame.mixer.music.play(1)



while True: # primary game loop	
	
	#windowSurfaceObject.fill(background_color)
	map.Render(windowSurfaceObject)
	interruptEvents.Display()
	
	Input.Update(interruptEvents)
	pygame.display.update()
	fpsClock.tick(30);
	
	interruptEvents.Update()

	map.Update()
