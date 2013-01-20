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
############################################################
import settings
from input import Input
from random import randint
from entity import Entity

# Animation frame patterns.
walkDown = [0, 1, 2, 1, 0, 3, 4, 3]
walkUp= [5, 6, 7, 6, 5, 8, 9, 8]
walkLeft= [10, 11, 12, 11, 10, 13, 14, 13]
walkRight= [15, 16, 17, 16, 15, 18, 19, 18]

class CharacterEntity(Entity):
	def __init__(self, entityName, startX, startY, spriteFileName = None):
		"""Constructor."""
		super (CharacterEntity, self).__init__(entityName, startX, startY, spriteFileName)
		self.currentAnimation = walkDown
		self.playerControlled = False
		self.followTarget = None
		self.followIndex = 0
		self.steps = []
		self.ai = None
		self.isEnemy = False
	
	def DebugRectSize(self):
		"""Prints out entity's rect size. Used in debugging."""
		print "{0} {1} ".format(self.rect.right - self.rect.left, self.rect.bottom-self.rect.top)
		
	def UpdateLocation(self):
		"""overriden method calls super and logs footsteps if player controlled"""
		super(CharacterEntity, self).UpdateLocation()
		if self.playerControlled:
			self.LogSteps()
			
	def SetLocation(self, coordinate):
		"""Sets entity's location."""
		for i in range(len(self.steps)):
			self.steps[i] = coordinate
		super(CharacterEntity, self).SetLocation(coordinate)
			
	def SetFollowTarget(self, entity, followIndex = 12):
		"""sets the target character entity to follow, specifying which footstep with followIndex"""
		self.followTarget = entity
		self.followIndex = followIndex
		self.collidable = False
		
	def FollowCurrentTarget(self):
		"""AI to follow on the targeted footstep"""
		if len(self.followTarget.steps) > self.followIndex:
			step = self.followTarget.steps[self.followIndex]	
			x, y = int(self.mapLocation[0]), int(self.mapLocation[1])
			walked = False
			if x < step[0]:
				self.WalkRight()
				walked = True
			elif x > step[0]:
				self.WalkLeft()
				walked = True
			if y < step[1]:
				self.WalkDown()
				walked = True
			elif y > step[1]:
				self.WalkUp()
				walked = True
			self.mapLocation = step # force entity in step
			if walked:
				self.velocityX, self.velocityY = 0.001, 0.001 # allows the entity to animate but not stray
			else:
				self.velocityX, self.velocityY = 0, 0 # stops entity animation and additional movement
			
	def LogSteps(self):
		"""logs the steps of a character"""
		step = int(self.mapLocation[0]), int(self.mapLocation[1])
		if len(self.steps) > 0:
			if self.steps[0] != step:
				self.steps.insert(0, step)
			if len(self.steps) > settings.PARTY_STEPS_LOGGED:
				self.steps.pop()
		else:
			self.steps.insert(0, step)
		
	def SetControl(self, bool):
		"""sets the entity to player controlled settings"""
		Entity.Player = self
		self.playerControlled = bool
		self.updateOffScreen = True
		self.steps = [self.mapLocation] * settings.PARTY_STEPS_LOGGED

	def Update(self):
		"""overriden update method checks if entity should be player controlled, is following another entity, or is on a certain AI. also calls animation method."""
		if self.playerControlled:
			self.PlayerControl()
		elif self.followTarget is not None:
			self.FollowCurrentTarget()
		else:
			self.AI()
		self.UpdateFrame()
		
	def AI(self):
		"""Performs AI actions based on AI mode."""
		if self.ai is None:
			self.RandomAI()
		elif self.ai == "basicEnemy":
			self.BasicEnemyAI()
			
	def BasicEnemyAI(self):
		"""AI mode for basic enemy."""
		if self.trigger == None:
			self.trigger = self.BattlePlayer
			
	def BattlePlayer(self, parent):
		self.ai = "dead"
		self.trigger = None
		print "begin battling player!"
				
	def WalkUp(self):
		"""basic acceleration and animation setting method (UP)"""
		self.Accelerate(0, -self.acceleration[1])
		self.currentAnimation = walkUp
		self.direction = settings.DIRECTION_UP
	def WalkDown(self):
		"""basic acceleration and animation setting method (DOWN)"""
		self.Accelerate(0, self.acceleration[1])
		self.currentAnimation = walkDown
		self.direction = settings.DIRECTION_DOWN
	def WalkLeft(self):
		"""basic acceleration and animation setting method (LEFT)"""
		self.Accelerate(-self.acceleration[0])
		self.currentAnimation = walkLeft
		self.direction = settings.DIRECTION_LEFT
	def WalkRight(self):
		"""basic acceleration and animation setting method (RIGHT)"""
		self.Accelerate(self.acceleration[0])
		self.currentAnimation = walkRight
		self.direction = settings.DIRECTION_RIGHT
		
	def RandomAI(self):
		if randint(0, 20) == 0: # choose new direction
			self.direction = randint(0, 10)
		
		if self.direction == settings.DIRECTION_UP:
			self.WalkUp()
		elif self.direction == settings.DIRECTION_DOWN:
			self.WalkDown()
		elif self.direction == settings.DIRECTION_LEFT:
			self.WalkLeft()
		elif self.direction == settings.DIRECTION_RIGHT:
			self.WalkRight()
		else:
			self.DeccelerateX()
			self.DeccelerateY()
		
	def PlayerControl(self):
		"""Causes entity to perform actions based on user input."""
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
			