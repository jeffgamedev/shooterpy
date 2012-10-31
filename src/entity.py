############################################################
# File:		entity.py
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

from tiledtmxloader import helperspygame
from input import Input
from random import randint
import settings
import pygame

walkDown = [0, 1, 2, 1, 0, 3, 4, 3]
walkUp= [5, 6, 7, 6, 5, 8, 9, 8]
walkLeft= [10, 11, 12, 11, 10, 13, 14, 13]
walkRight= [15, 16, 17, 16, 15, 18, 19, 18]

class Entity(helperspygame.SpriteLayer.Sprite):
	"""Entity class is the base class for all person-like characters in the game"""
	Path = "../gfx/sprites/"
	def __init__(self, entityName, startX, startY, spriteFileName = None, frameSize = (17, 31), scaleFactor = settings.SPRITE_SCALE_FACTOR):
		self.mapLocation = (startX, startY)
		self.name = entityName
		self.layer = 0
		self.size = 16 * scaleFactor, 16 * scaleFactor		
		self.frame = 0
		self.velocityX = 1
		self.velocityY = 1
		self.visible = True
		self.direction = 1
		self.acceleration = 0.5, 0.5
		self.maxVelocity = 5, 5
		self.currentAnimation = walkDown
		self.frameSize = frameSize[0], frameSize[1]
		self.framesPerRow = 5
		self.rect = pygame.Rect(self.mapLocation[0], self.mapLocation[1], self.frameSize[0]*scaleFactor, self.frameSize[1]*scaleFactor)
		
		self.DebugRectSize()
		
		self.touchRect = pygame.Rect(self.rect.left, self.rect.top, self.size[0]*scaleFactor, self.size[1]*scaleFactor)
		self.frameRect = pygame.Rect(0, 0, self.frameSize[0]*scaleFactor, self.frameSize[1]*scaleFactor)
		
		self.scaleFactor = scaleFactor
		self.SetupImage(spriteFileName)
		self.pickupRange = 10
		self.playerControlled = False
		
		super(Entity, self).__init__(self.image, self.rect, self.frameRect)

	
	def DebugRectSize(self):
		print "{0} {1} ".format(self.rect.right - self.rect.left, self.rect.bottom-self.rect.top)
		
	def SetControl(self, bool):
		
		self.playerControlled = bool
		
	def SetupImage(self, spriteFileName):
		if spriteFileName is None:
			#self.image = pygame.Surface((self.frameSize[0], self.frameSize[1]), pygame.SRCALPHA)
			self.image = pygame.Surface((self.size[0], self.size[1]), pygame.SRCALPHA)
			self.image.fill((255, 0, 0, 200))
		else:
			self.image = pygame.image.load(Entity.Path + spriteFileName)
			x = self.image.get_width()
			y = self.image.get_height()
			self.image = pygame.transform.scale(self.image, (x*self.scaleFactor, y*self.scaleFactor))
		
	def Update(self):
		if self.playerControlled:
			self.PlayerControl()
		else:
			self.RandomAI()
		self.Animate()
		#print self.get_draw_cond(), self.rect.bottom
				
	def WalkUp(self):
		self.velocityY = settings.Clamp(self.velocityY - self.acceleration[1], -self.maxVelocity[1], self.maxVelocity[1])
		self.currentAnimation = walkUp
		self.direction = 0
	def WalkDown(self):
		self.velocityY = settings.Clamp(self.velocityY + self.acceleration[1], -self.maxVelocity[1], self.maxVelocity[1])
		self.currentAnimation = walkDown
		self.direction = 1
	def WalkLeft(self):
		self.velocityX = settings.Clamp(self.velocityX - self.acceleration[0], -self.maxVelocity[0], self.maxVelocity[0])
		self.currentAnimation = walkLeft
		self.direction = 2
	def WalkRight(self):
		self.velocityX = settings.Clamp(self.velocityX + self.acceleration[0], -self.maxVelocity[0], self.maxVelocity[0])
		self.currentAnimation = walkRight
		self.direction = 3
		
	def DeccelerateY(self):
		if self.velocityY < self.acceleration[1] and self.velocityY > -self.acceleration[1]:
			self.velocityY = 0
		else:
			self.velocityY = self.velocityY * settings.FRICTION
			
	def DeccelerateX(self):
		if self.velocityX < self.acceleration[0] and self.velocityX > -self.acceleration[0]:
			self.velocityX = 0
		else:
			self.velocityX = self.velocityX * settings.FRICTION
		
	def RandomAI(self):
		if randint(0, 20) == 0: # choose new direction
			self.direction = randint(0, 10)
		
		if self.direction == 0:
			self.WalkUp()
			#self.DeccelerateX()
		elif self.direction == 1:
			self.WalkDown()
			#self.DeccelerateX()
		elif self.direction == 2:
			self.WalkLeft()
			#self.DeccelerateY()
		elif self.direction == 3:
			self.WalkRight()
			#self.DeccelerateY()
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
			
	def CheckObstructions(self, obs):
		if self.velocityX < 0:
			x = (self.mapLocation[0] + self.velocityX) / settings.TILE_WIDTH
			y1 = (self.mapLocation[1]) / settings.TILE_HEIGHT 
			y2 = (self.mapLocation[1] + self.size[1]) / settings.TILE_HEIGHT
			if obs(int(x), int(y1)) or obs(int(x), int(y2)):
				self.velocityX = 0
		elif self.velocityX > 0:
			x = (self.mapLocation[0] + self.size[0] + self.velocityX) / settings.TILE_WIDTH
			y1 = (self.mapLocation[1]) / settings.TILE_HEIGHT 
			y2 = (self.mapLocation[1] + self.size[1]) / settings.TILE_HEIGHT
			if obs(int(x), int(y1)) or obs(int(x), int(y2)):
				self.velocityX = 0
		if self.velocityY < 0:
			y = (self.mapLocation[1] + self.velocityY) / settings.TILE_HEIGHT
			x1 = (self.mapLocation[0]) / settings.TILE_WIDTH
			x2 = (self.mapLocation[0] + self.size[0]) / settings.TILE_WIDTH
			if obs(int(x1), int(y)) or obs(int(x2), int(y)):
				self.velocityY = 0
		elif self.velocityY > 0:
			y = (self.mapLocation[1]  + self.size[1] + self.velocityY) / settings.TILE_HEIGHT
			x1 = (self.mapLocation[0]) / settings.TILE_WIDTH
			x2 = (self.mapLocation[0] + self.size[0]) / settings.TILE_WIDTH
			if obs(int(x1), int(y)) or obs(int(x2), int(y)):
				self.velocityY = 0
				
	def CheckEntities(self, ents):
		for ent in ents:
			if ent is not self:
				pass
				#if not self.touchRect.colliderect(ent.touchRect):
					#print "i"
				#if self.velocityX > 0:
					#if self.touchRect.left + self.velocityX 
				#if self.touchRect.colliderect(ent.touchRect):
				#	if self.velocityX > 0 and ent.touchRect.left > self.touchRect.left:
				#		self.velocityX = 0
				#	print "collide"
			
	def Animate(self):
		if self.velocityX != 0 or self.velocityY != 0:
			if self.frame >= len(self.currentAnimation):
				self.frame = 0
			self.SetFrame(self.frame)
			self.frame = self.frame + .25
		elif self.frame != 0:
			self.frame = 0
			self.SetFrame(0)
	
	def SetFrame(self, frame):
		if self.currentAnimation is not None:
			frame = self.currentAnimation[int(frame)]
			frameX = int(frame)%self.framesPerRow
			frameY = int(int(frame)/self.framesPerRow)
			self.frameRect.left = frameX * self.frameSize[0]*self.scaleFactor
			self.frameRect.top = frameY * self.frameSize[1]*self.scaleFactor
			
	
	def Move(self):
		self.mapLocation = self.mapLocation[0] + self.velocityX, self.mapLocation[1] + self.velocityY
		self.rect.left = self.mapLocation[0]
		self.rect.top = self.mapLocation[1] - self.size[1]
		self.touchRect.left = self.rect.left
		self.touchRect.top= self.rect.top
		#self.rangeRectangle.left = self.rect.left-self.pickupRange
		#self.rangeRectangle.top = self.rect.top-self.pickupRange