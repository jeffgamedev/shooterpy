from tiledtmxloader import helperspygame
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
		self.layer = 0 # which layer entity is on top of
		self.visible = True
		self.image = pygame.Surface((25, 45), pygame.SRCALPHA)
		self.image.fill((255, 0, 0, 200))
		self.rect = self.image.get_rect()
		self.size = self.rect.width, self.rect.height
		self.rect = pygame.Rect(self.mapLocation[0], self.mapLocation[1], self.mapLocation[0]+self.size[0], self.mapLocation[1]+self.size[1])
		super(Entity, self).__init__(self.image, self.rect)
		
	def Update(self):
		self.mapLocation = self.mapLocation[0] + 12, self.mapLocation[1] + 4
		self.rect.left = self.mapLocation[0] # pygame.Rect(self.mapLocation[0], self.mapLocation[1], self.mapLocation[0]+self.size[0], self.mapLocation[1]+self.size[1])
		self.rect.top = self.mapLocation[1]
