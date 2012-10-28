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
TextBoxSystem = overlay.TextBoxSystem(windowSurfaceObject)
TextBoxSystem.New("blane.png", "Let's rock out to Igelkott!")

map = Map()
map.LoadMap("firstmap.tmx")
map.AddEntity(170, 150)

pygame.mixer.music.load("../music/igelkott.mod")
pygame.mixer.music.play(1)


while True: # primary game loop	
	
	#windowSurfaceObject.fill(background_color)
	map.Render(windowSurfaceObject)
	TextBoxSystem.Display()
	
	pygame.display.update()
	fpsClock.tick(30);
	
	Input.Update(TextBoxSystem)
	
	map.Update()
