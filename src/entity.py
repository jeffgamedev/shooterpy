from tiledtmxloader import helperspygame
from input import Input
import settings
import pygame
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

walkDown = [0, 1, 2, 1, 0, 3, 4, 3]
walkUp= [5, 6, 7, 6, 5, 8, 9, 8]
walkLeft= [10, 11, 12, 11, 10, 13, 14, 13]
walkRight= [15, 16, 17, 16, 15, 18, 19, 18]

class Entity(helperspygame.SpriteLayer.Sprite):
	"""Entity class is the base class for all person-like characters in the game"""
	Path = "../gfx/sprites/"
	def __init__(self, entityName, startX, startY, spriteFileName = None, frameSize = (17, 31)):
		self.mapLocation = (startX, startY)
		self.name = entityName
		self.layer = 0
		self.size = 16, 16
		self.frame = 0
		self.velocityX = 0
		self.velocityY = 0
		self.visible = True
		self.acceleration = 0.5, 0.5
		self.maxVelocity = 5, 5
		self.currentAnimation = walkDown
		self.frameSize = frameSize
		self.framesPerRow = 5
		self.rect = pygame.Rect(self.mapLocation[0], self.mapLocation[1], self.mapLocation[0] + self.frameSize[0], self.mapLocation[1] + self.frameSize[1])
		self.frameRect = pygame.Rect(0, 0, self.frameSize[0], self.frameSize[1])
		self.SetupImage(spriteFileName)
		super(Entity, self).__init__(self.image, self.rect, self.frameRect)
		
	def SetupImage(self, spriteFileName):
		if spriteFileName is None:
			#self.image = pygame.Surface((self.frameSize[0], self.frameSize[1]), pygame.SRCALPHA)
			self.image = pygame.Surface((self.size[0], self.size[1]), pygame.SRCALPHA)
			self.image.fill((255, 0, 0, 200))
		else:
			self.image = pygame.image.load(Entity.Path + spriteFileName)
		
	def Update(self):
		if Input.keyboard["up"]:
			self.velocityY = settings.Clamp(self.velocityY - self.acceleration[1], -self.maxVelocity[1], self.maxVelocity[1])
			self.currentAnimation = walkUp
		elif Input.keyboard["down"]:
			self.velocityY = settings.Clamp(self.velocityY + self.acceleration[1], -self.maxVelocity[1], self.maxVelocity[1])
			self.currentAnimation = walkDown
		elif self.velocityY != 0:
			if self.velocityY < self.acceleration[1] and self.velocityY > -self.acceleration[1]:
				self.velocityY = 0
			else:
				self.velocityY = self.velocityY * settings.FRICTION
		if Input.keyboard["left"]:
			self.velocityX = settings.Clamp(self.velocityX - self.acceleration[0], -self.maxVelocity[0], self.maxVelocity[0])
			self.currentAnimation = walkLeft
		elif Input.keyboard["right"]:
			self.velocityX = settings.Clamp(self.velocityX + self.acceleration[0], -self.maxVelocity[0], self.maxVelocity[0])
			self.currentAnimation = walkRight
		elif self.velocityX != 0:
			if self.velocityX < self.acceleration[0] and self.velocityX > -self.acceleration[0]:
				self.velocityX = 0
			else:
				self.velocityX = self.velocityX * settings.FRICTION			
		self.Animate()
			
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
			self.frameRect.left = frameX * self.frameSize[0]
			self.frameRect.top = frameY * self.frameSize[1]
	
	def Move(self):
		self.mapLocation = self.mapLocation[0] + self.velocityX, self.mapLocation[1] + self.velocityY
		self.rect.left = self.mapLocation[0]
		self.rect.top = self.mapLocation[1] - self.size[1]