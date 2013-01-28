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
pygame.init() # needs to be initialized for static members of other classes

import settings # for constants, etc
from pygame.locals import *
from map import Map
from input import Input
from InterruptEventSystem import InterruptEventSystem
from MenuBox import MenuBox
from TextBox import TextBox
from NotificationBox import NotificationBox
from gameInstance import GameInstance
import gameMenu

# game dependencies initiation

fpsClock = pygame.time.Clock()
pygame.display.set_caption('Shooter 1, II')
background_color = pygame.Color( 0, 0, 0)

game = GameInstance()

game.interruptEventSystem.Add(TextBox(game, "blane.png", "hi"))
game.interruptEventSystem.Add(MenuBox(game, 100, 200, ["one", "two", "three"], [gameMenu.option1, gameMenu.option2, gameMenu.option3]))

# level setup
pygame.mixer.music.load("../music/sledpuller.it")
pygame.mixer.music.play(-1)
game.mapSystem.Update() # fixes the jump at the beginning. would be best to fix the source of the problem tho.

while True: # primary game loop	
	##### LOGIC UPDATES #####
	game.interruptEventSystem.Update()
	if not game.interruptEventSystem.HasActiveEvent(): # Map Logic does not update while an interrupt event is waiting to be dismissed!
		game.mapSystem.Update()
		
	Input.Update(game)

	##### DISPLAY UPDATES #####	
	game.mapSystem.Render(game.gameSurface)	
	game.interruptEventSystem.Display()
	pygame.display.update()
	
	#Framerate Regulation
	fpsClock.tick(settings.FRAMES_PER_SECOND);
