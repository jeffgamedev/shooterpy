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
import settings
import pygame
import random

class Entity(helperspygame.SpriteLayer.Sprite):
	"""Entity class is the base class for all person-like characters in the game"""
	Path = "../gfx/sprites/"
	def __init__(self, entityName, startX, startY, spriteFileName = None, size = (16, 17), frameSize = (17, 33), scaleFactor = settings.SPRITE_SCALE_FACTOR):
		self.mapLocation = (startX, startY)
		self.name = entityName
		self.layer = 0
		self.size = size[0] * scaleFactor, size[1] * scaleFactor
		self.frame = 0
		self.velocityX = 0
		self.velocityY = 0
		self.visible = True
		self.collidable = True
		self.trigger = None
		self.direction = 1		
		self.acceleration = 0.5, 0.5
		self.maxVelocity = 5, 5
		self.currentAnimation = None
		self.frameSize = frameSize[0], frameSize[1]
		self.framesPerRow = 5
		self.updateOffScreen = False
		self.rect = pygame.Rect(self.mapLocation[0], self.mapLocation[1], self.frameSize[0]*scaleFactor, self.frameSize[1]*scaleFactor)
		self.touchRect = pygame.Rect(self.rect.left, self.rect.top, self.size[0], self.size[1])
		self.frameRect = pygame.Rect(0, 0, self.frameSize[0]*scaleFactor, self.frameSize[1]*scaleFactor)
		self.scaleFactor = scaleFactor
		self.SetupImage(spriteFileName)
		super(Entity, self).__init__(self.image, self.rect, self.frameRect)
		
	def Update(self):
		if self.velocityX != 0:
			self.DeccelerateX()
		if self.velocityY != 0:
			self.DeccelerateY()
		self.Animate()
		
	def ShouldUpdate(self, cameraRectangle):
		if self.updateOffScreen:
			return True
		return self.rect.colliderect(cameraRectangle)
		
	def SetupImage(self, spriteFileName):
		if spriteFileName is None:
			self.image = pygame.Surface((self.size[0], self.size[1]), pygame.SRCALPHA)
			self.image.fill((255, 0, 0, 200))
		else:
			self.image = pygame.image.load(Entity.Path + spriteFileName)
			x = self.image.get_width()
			y = self.image.get_height()
			self.image = pygame.transform.scale(self.image, (x*self.scaleFactor, y*self.scaleFactor))
	
	def ChooseStartFrame(self):
		"""Determines the frame for the character to start walking on in order to keep them out of sync"""
		startFrame = random.randint(0,len(self.currentAnimation)-1)
		self.SetFrame(startFrame)
		self.frame = startFrame
	
	
	def Accelerate(self, x=0, y=0):
		if self.velocityX == 0 and self.velocityY == 0:
			self.ChooseStartFrame();
		if x != 0:
			self.velocityX = settings.Clamp(self.velocityX + x, -self.maxVelocity[0], self.maxVelocity[0])
		if y != 0:
			self.velocityY = settings.Clamp(self.velocityY + y, -self.maxVelocity[1], self.maxVelocity[1])
		
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
				
	def CheckEntityCollision(self, ents):
		for ent in ents:
			if ent is not self:
				if ent.collidable or ent.trigger: # check if should collision check
					if self.touchRect.colliderect(ent.touchRect):
						if ent.collidable and self.collidable: # its a physical collision
							self.PushAgainstEntity(ent)
						if ent.trigger is not None: # theres a collision and should be an even triggered
							ent.trigger(ent)
	
	def PushAgainstEntity(self, ent):
		if self.velocityX > 0 and self.touchRect.right <= ent.touchRect.right:
			self.velocityX = self.velocityX * settings.COLLISION_SLOWDOWN
			ent.velocityX += settings.PUSH_SPEED
		elif self.velocityX < 0 and self.touchRect.left >= ent.touchRect.left:
			self.velocityX = self.velocityX * settings.COLLISION_SLOWDOWN
			ent.velocityX -= settings.PUSH_SPEED
		if self.velocityY > 0 and self.touchRect.bottom <= ent.touchRect.bottom:
			self.velocityY = self.velocityY * settings.COLLISION_SLOWDOWN
			ent.velocityY += settings.PUSH_SPEED
		elif self.velocityY < 0 and self.touchRect.top >= ent.touchRect.top:
			self.velocityY = self.velocityY * settings.COLLISION_SLOWDOWN
			ent.velocityY -= settings.PUSH_SPEED
			
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