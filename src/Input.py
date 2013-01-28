import pygame
import sys
from MenuBox import MenuBox
from TextBox import TextBox
from NotificationBox import NotificationBox
from pygame.locals import *

class Input:
	keyboard = {}
	keyboard[K_UP] = 0
	keyboard[K_w] = 0
	keyboard[K_DOWN] = 0
	keyboard[K_s] = 0
	keyboard[K_LEFT] = 0
	keyboard[K_a] = 0
	keyboard[K_RIGHT] = 0
	keyboard[K_d] = 0
	keyboard[K_ESCAPE] = 0
	keyboard[K_RETURN] = 0
	keyboard[K_SPACE] = 0
	keyboard["up"] = 0
	keyboard["down"] = 0
	keyboard["left"] = 0
	keyboard["right"] = 0
	
	interruptWait = False
	
	@staticmethod
	def Update(game):
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYUP:
				if event.key in Input.keyboard:
					Input.keyboard[event.key] = 0
					
			elif event.type == KEYDOWN:
				if event.key in Input.keyboard:
					Input.keyboard[event.key] = 1
					
		if game.interruptEventSystem.HasActiveEvent():
			if game.interruptEventSystem.currentEvent.eventName == "TextBox" or game.interruptEventSystem.currentEvent.eventName == "NotificationBox":
				Input.TextBoxInput(game)
			elif game.interruptEventSystem.currentEvent.eventName == "MenuBox": #ype(game.interruptEventSystem.currentEvent) is MenuBox:
				Input.MenuBoxInput(game)
		else:
			Input.StandardInput()

	@staticmethod
	def TextBoxInput(game):
		print "textbox input"
		if Input.keyboard[K_RETURN] and Input.interruptWait == False:
			game.interruptEventSystem.Dismiss()
			Input.interruptWait = True
		elif not Input.keyboard[K_RETURN] and Input.interruptWait == True:
			Input.interruptWait = False
			
	@staticmethod
	def MenuBoxInput(game):
		print "menubox input"
		if Input.keyboard[K_RETURN] and Input.interruptWait == False:
			tempEvent = game.interruptEventSystem.currentEvent
			game.interruptEventSystem.Dismiss()
			tempEvent.methodList[tempEvent.selected](game)
			Input.interruptWait = True
		if Input.keyboard[K_UP] and Input.interruptWait == False:
			game.interruptEventSystem.currentEvent.updateCursorPosition("up")
		if Input.keyboard[K_DOWN] and Input.interruptWait == False:
			game.interruptEventSystem.currentEvent.updateCursorPosition("down")


		
	@staticmethod
	def StandardInput():
		if Input.keyboard[K_RIGHT] or Input.keyboard[K_d]:
			Input.keyboard["right"] = 1
		else:
			Input.keyboard["right"] = 0
		if Input.keyboard[K_LEFT] or Input.keyboard[K_a]:
			Input.keyboard["left"] = 1
		else:
			Input.keyboard["left"] = 0
		if Input.keyboard[K_UP] or Input.keyboard[K_w]:
			Input.keyboard["up"] = 1
		else:
			Input.keyboard["up"] = 0
		if Input.keyboard[K_DOWN] or Input.keyboard[K_s]:
			Input.keyboard["down"] = 1
		else:
			Input.keyboard["down"] = 0
			
