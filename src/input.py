import pygame
import sys
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
	def Update(interruptEventSystemInstance):
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
					
		if interruptEventSystemInstance.HasActiveEvent():
			Input.TextBoxInput(interruptEventSystemInstance)
		else:
			Input.StandardInput()

	@staticmethod
	def TextBoxInput(textBoxSystemInstance):
		
		if Input.keyboard[K_RETURN] and Input.interruptWait == False:
			textBoxSystemInstance.Dismiss()
			Input.interruptWait = True
		elif not Input.keyboard[K_RETURN] and Input.interruptWait == True:
			Input.interruptWait = False
		
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
			
