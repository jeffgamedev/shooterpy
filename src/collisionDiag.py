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
interruptEvents = overlay.InterruptEventSystem(windowSurfaceObject)
interruptEvents.AddTextBox("blane.png", "Good day, sir Frog! I put together some on-screen diagnostic tools to help you figure this thing out. My first observation is that the touchRects are simply way too big. Like 200x200 for each. That might be why it seems like they are always colliding. Hope this helps!")
map = Map()
map.LoadMap("firstmap.tmx")

Blane = map.AddEntity(170, 150)
Blane.SetControl(True)
map.camera.SetTarget(Blane)
#map.AddEntity(190, 160)
#map.AddEntity(210, 170)
Doob = map.AddEntity(240, 180)

pygame.mixer.music.load("../music/igelkott.mod")
pygame.mixer.music.play(1)

collision = fontObj.render("Collision!", 1, (255, 255,255))

while True: # primary game loop 
    blaneStr = "Blane touchRect = ({0}, {1}) to ({2}, {3})".format(Blane.touchRect.left,Blane.touchRect.top, Blane.touchRect.right, Blane.touchRect.bottom)
    blaneLoc = fontObj.render(blaneStr, 1, (255,255,255))
    doobStr = "Doob touchRect = ({0}, {1}) to ({2}, {3})".format(Doob.touchRect.left,Doob.touchRect.top, Doob.touchRect.right, Doob.touchRect.bottom)
    doobLoc = fontObj.render(doobStr, 1, (255, 255,255))
        
        
    #windowSurfaceObject.fill(background_color)
    map.Render(windowSurfaceObject)
    interruptEvents.Display()
        
    map.Render(windowSurfaceObject)
    interruptEvents.Display()
    
    windowSurfaceObject.blit(blaneLoc, (0, 0))
    windowSurfaceObject.blit(doobLoc, (0, 30))
        
    if Blane.touchRect.colliderect(Doob.touchRect):
        windowSurfaceObject.blit(collision, (0, 60))



    Input.Update(interruptEvents)
    pygame.display.update()
    fpsClock.tick(30);

    interruptEvents.Update()

    map.Update()