# File:		game.py
############################################################
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
from gameInstance import GameInstance
import gameMenu

# game dependencies initiation
pygame.init()
fpsClock = pygame.time.Clock()
pygame.display.set_caption('Shooter 1, II')
background_color = pygame.Color( 0, 0, 0)

game = GameInstance()

TextBoxHelper(game.gameSurface, game.interruptEventSystem) #instantiate class to fill static instance
TextBoxHelper.Instance.MenuBox(200, 150, ["FrogVolt!", "ShadowbladeOldman", "Blanez", "Master of the Obvious!"], [gameMenu.option1, gameMenu.option2, gameMenu.option3, gameMenu.option4]);

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
