############################################################
# File:		characterentity.py
# Project:	Shooter 1, II
# Date Created:	October 13, 2012	
#
# Description: 	This file contains the Entity class
#	which is the base class for player and npc.
#	The purpose of this class is to ensure that anything
#	that any attribute or method that a player and npc 
#	can share is declared here.
#
# Special Note on Use:
#	Polymorphism will assuredly be used when managing
#	Entities in game.py. I (Brian) would personally 
#	prefer to decouple graphics from game-logic, but 
#	we should look into how practical that will be to
#	do.
############################################################
from input import Input
from random import randint
from entity import Entity

walkDown = [0, 1, 2, 1, 0, 3, 4, 3]
walkUp= [5, 6, 7, 6, 5, 8, 9, 8]
walkLeft= [10, 11, 12, 11, 10, 13, 14, 13]
walkRight= [15, 16, 17, 16, 15, 18, 19, 18]

class CharacterEntity(Entity):
	def __init__(self, entityName, startX, startY, spriteFileName = None):
		super (CharacterEntity, self).__init__(entityName, startX, startY, spriteFileName)
		self.currentAnimation = walkDown
		self.playerControlled = False
		self.DebugRectSize()
	
	def DebugRectSize(self):
		print "{0} {1} ".format(self.rect.right - self.rect.left, self.rect.bottom-self.rect.top)
		
	def SetControl(self, bool):
		self.playerControlled = bool
		self.updateOffScreen = True
		
	def ShouldUpdate(self, cameraRectangle):
		if self.updateOffScreen:
			return True
		return self.rect.colliderect(cameraRectangle)

	def Update(self):
		if self.playerControlled:
			self.PlayerControl()
		else:
			self.RandomAI()
		self.Animate()
				
	def WalkUp(self):
		self.Accelerate(0, -self.acceleration[1])
		self.currentAnimation = walkUp
		self.direction = 0
	def WalkDown(self):
		self.Accelerate(0, self.acceleration[1])
		self.currentAnimation = walkDown
		self.direction = 1
	def WalkLeft(self):
		self.Accelerate(-self.acceleration[0])
		self.currentAnimation = walkLeft
		self.direction = 2
	def WalkRight(self):
		self.Accelerate(self.acceleration[0])
		self.currentAnimation = walkRight
		self.direction = 3
		
	def RandomAI(self):
		if randint(0, 20) == 0: # choose new direction
			self.direction = randint(0, 10)
		
		if self.direction == 0:
			self.WalkUp()
		elif self.direction == 1:
			self.WalkDown()
		elif self.direction == 2:
			self.WalkLeft()
		elif self.direction == 3:
			self.WalkRight()
		else:
			self.DeccelerateX()
			self.DeccelerateY()
		
	def PlayerControl(self):
		if Input.keyboard["up"]:
			self.WalkUp()
		elif Input.keyboard["down"]:
			self.WalkDown()
		elif self.velocityY != 0:
			self.DeccelerateY()
		if Input.keyboard["left"]:
			self.WalkLeft()
		elif Input.keyboard["right"]:
			self.WalkRight()
		elif self.velocityX != 0:
			self.DeccelerateX()
			