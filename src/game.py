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
#interruptEvents.AddTextBox("blane.png", "Good day, sir Frog! It appears I have solved the problems with collision detection and entity display! Huzzah! Now we can easily move on to other parts of the game!")
interruptEvents.AddTextBox("TL_port_blu.bmp", "Sir, it appears the cloning device has gone haywire.")

#interruptEvents.AddNotificationBox("Pistol Procured!")
map = Map()
map.LoadMap("firstmap.tmx")

Blane = map.AddEntity(170, 150)
Blane.SetControl(True)
map.camera.SetTarget(Blane)

for x in range(7):
	for y in range(6):		
		map.AddEntity(160+x*50, 120+y*50)
		
for x in range(7):
	for y in range(6):		
		map.AddEntity(1720+x*50, 720+y*50)
		
map.AddEntity(210, 170)
map.AddEntity(240, 180)

pygame.mixer.music.load("../music/igelkott.mod")
pygame.mixer.music.play(1)


map.Update() #fixes the jump at the beginning. would be best to fix the source of the problem tho.

while True: # primary game loop	
	
	##### LOGIC UPDATES #####
	
	fps = fontObj.render("42", 1, (255,255,255))	
	
	interruptEvents.Update()
	
	# Map Logic does not update while an interrupt event is waiting to be dismissed!
	if not interruptEvents.HasActiveEvent():
		map.Update()
	
	Input.Update(interruptEvents)

	
	##### DISPLAY UPDATES #####	
	map.Render(windowSurfaceObject)
	interruptEvents.Display()

	pygame.display.update()
	
	#Framerate Regulation
	fpsClock.tick(30);
	


	
