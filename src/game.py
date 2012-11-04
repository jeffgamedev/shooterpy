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
from overlay import TextBox, NotificationBox

pygame.init()
fpsClock = pygame.time.Clock()

gameSurface = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

pygame.display.set_caption('Shooter 1, II')
textBoxFont = pygame.font.Font('freesansbold.ttf', settings.TEXTBOX_FONT_SIZE)
notificationFont = pygame.font.Font('freesansbold.ttf', settings.NOTIFICATION_FONT_SIZE)
background_color = pygame.Color( 0, 0, 0)

#Testing TextBoxes
interruptEvents = overlay.InterruptEventSystem(gameSurface)

interruptEvents.Add(TextBox(gameSurface, textBoxFont, "blane.png", "GOOD EVENING! I have updated the interruptEvents system to be more polymorphic. Use the Add() method instead of AddTextBox etc. That way any time we make a new interruptEvent, we don't need to make a new method for it in the system's class."))
interruptEvents.Add(TextBox(gameSurface, textBoxFont, "blane.png", "This WILL break the old way of doing things. Just FYI."))
interruptEvents.Add(TextBox(gameSurface, textBoxFont, "blane.png", "I also changed a couple variable names\ngameSurface is now the surface object\nfont object names have been changed as well."))
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
	interruptEvents.Update()
	
	# Map Logic does not update while an interrupt event is waiting to be dismissed!
	if not interruptEvents.HasActiveEvent():
		map.Update()
	
	Input.Update(interruptEvents)
	
	##### DISPLAY UPDATES #####	
	map.Render(gameSurface)
	interruptEvents.Display()
	pygame.display.update()
	
	#Framerate Regulation
	fpsClock.tick(30);
