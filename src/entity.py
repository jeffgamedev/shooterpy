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

class Entity(helperspygame.SpriteLayer.Sprite):
	"""Entity class is the base class for all person-like characters in the game"""
	def __init__(self, entityName, startX, startY):
		self.mapLocation = (startX, startY)
		self.name = entityName
		self.layer = 0
		self.velocityX = 0
		self.velocityY = 0
		self.acceleration = 0.5, 0.5
		self.maxVelocity = 5, 5
		self.visible = True
		self.image = pygame.Surface((25, 45), pygame.SRCALPHA)
		self.image.fill((255, 0, 0, 200))
		self.rect = self.image.get_rect()
		self.size = self.rect.width, self.rect.height
		self.rect = pygame.Rect(self.mapLocation[0], self.mapLocation[1], self.mapLocation[0]+self.size[0], self.mapLocation[1]+self.size[1])
		super(Entity, self).__init__(self.image, self.rect)
		
	def Update(self):
		if Input.keyboard["up"]:
			self.velocityY = settings.Clamp(self.velocityY - self.acceleration[1], -self.maxVelocity[1], self.maxVelocity[1])
		elif Input.keyboard["down"]:
			self.velocityY = settings.Clamp(self.velocityY + self.acceleration[1], -self.maxVelocity[1], self.maxVelocity[1])
		else:
			self.velocityY = self.velocityY * settings.FRICTION
		if Input.keyboard["left"]:
			self.velocityX = settings.Clamp(self.velocityX - self.acceleration[0], -self.maxVelocity[0], self.maxVelocity[0])
		elif Input.keyboard["right"]:
			self.velocityX = settings.Clamp(self.velocityX + self.acceleration[0], -self.maxVelocity[0], self.maxVelocity[0])
		else:
			self.velocityX = self.velocityX * settings.FRICTION
			
	def CheckObstructions(self, obs):
		x = int((self.mapLocation[0] + self.velocityX) / settings.TILE_WIDTH)
		y = int((self.mapLocation[1] + self.size[1]) / settings.TILE_HEIGHT)
		
		if obs(x, y):
			self.velocityX = 0
		x = int((self.mapLocation[0]) / settings.TILE_WIDTH)
		y = int((self.mapLocation[1] + self.velocityY + self.size[1]) / settings.TILE_HEIGHT)
		if obs(x, y):
			self.velocityY = 0
		
	
	def Move(self):
		self.mapLocation = self.mapLocation[0] + self.velocityX, self.mapLocation[1] + self.velocityY
		self.rect.left = self.mapLocation[0]
		self.rect.top = self.mapLocation[1]