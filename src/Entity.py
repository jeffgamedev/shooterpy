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
############################################################
from tiledtmxloader import helperspygame
import settings
import pygame
import random

class Entity(helperspygame.SpriteLayer.Sprite):
	"""Entity class is the base class for all person-like characters in the game"""
	Player = None
	Path = "../gfx/sprites/"

	
	def __init__(self, entityName, startX, startY, spriteFileName = None, size = (14, 12), frameSize = (17, 33), scaleFactor = settings.SPRITE_SCALE_FACTOR):
		"""Constructor."""
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
		self.triggerAll = False # if trigger effects interacting with all entities, not just player
		self.direction = settings.DIRECTION_DOWN		
		self.acceleration = 0.5, 0.5
		self.maxVelocity = 5, 5
		self.currentAnimation = None
		self.spriteOffset = -4, -18
		self.frameSize = frameSize[0], frameSize[1]
		self.framesPerRow = 5
		self.updateOffScreen = False
		self.rect = pygame.Rect(self.mapLocation[0], self.mapLocation[1], self.frameSize[0]*scaleFactor, self.frameSize[1]*scaleFactor)
		self.touchRect = pygame.Rect(self.rect.left, self.rect.top, self.size[0], self.size[1])
		self.frameRect = pygame.Rect(0, 0, self.frameSize[0]*scaleFactor, self.frameSize[1]*scaleFactor)
		self.scaleFactor = scaleFactor
		self.SetupImage(spriteFileName)
		self.isMoving = False
		super(Entity, self).__init__(self.image, self.rect, self.frameRect)
		
	def Update(self):
		"""Applies deceleration to entity and animates sprite."""
		if self.velocityX != 0:
			self.DeccelerateX()
		if self.velocityY != 0:
			self.DeccelerateY()
		self.UpdateFrame()
		
	def ShouldUpdate(self, cameraRectangle):
		"""Returns boolean based on whether or not the entity should update.
		That is: whether or not they should deccelerate and animate.""" 
		if self.updateOffScreen:
			return True
		return self.rect.colliderect(cameraRectangle)
		
	def SetupImage(self, spriteFileName):
		"""Does initial image setup. The sprite is automatically chosen from the sprites directory of the filesystem.
		If no filename is given, a solid color block will be used to represent the entity."""
		if spriteFileName is None:
			self.image = pygame.Surface((self.size[0], self.size[1]), pygame.SRCALPHA)
			self.image.fill((255, 0, 0, 200))
		else:
			self.image = pygame.image.load(Entity.Path + spriteFileName)
			x = self.image.get_width()
			y = self.image.get_height()
			self.image = pygame.transform.scale(self.image, (x*self.scaleFactor, y*self.scaleFactor))
	
	def ChooseStartFrame(self):
		"""Determines the frame for the character to start walking on in order to keep them out of sync."""
		startFrame = random.randint(0,len(self.currentAnimation)-1)
		self.SetFrame(startFrame)
		self.frame = startFrame
	
	def Accelerate(self, x=0, y=0):
		"""Updates the Entity with respect to momentum.
		Maybe this should go in the update method?"""
		if self.velocityX == 0 and self.velocityY == 0 and not self.isMoving:
			self.ChooseStartFrame()
			self.isMoving = True
		if x < 0:
			self.velocityX = settings.Clamp(self.velocityX + x, -self.maxVelocity[0], 0)
		elif x > 0:
			self.velocityX = settings.Clamp(self.velocityX + x, 0, self.maxVelocity[0])
		if y < 0:
			self.velocityY = settings.Clamp(self.velocityY + y, -self.maxVelocity[1], 0)
		elif y > 0:
			self.velocityY = settings.Clamp(self.velocityY + y, 0, self.maxVelocity[1])
		
	def DeccelerateY(self):
		"""Decreases vertical velocity."""
		if self.velocityY < self.acceleration[1] and self.velocityY > -self.acceleration[1]:
			self.velocityY = 0
		else:
			self.velocityY = self.velocityY * settings.FRICTION
			
	def DeccelerateX(self):
		"""Decreases horizontal velocity."""
		if self.velocityX < self.acceleration[0] and self.velocityX > -self.acceleration[0]:
			self.velocityX = 0
		else:
			self.velocityX = self.velocityX * settings.FRICTION

	def CheckObstructions(self, isObstructed):
		"""Checks to see if entity is obstructed via the map."""
		# TODO: This should return a boolean, and the actual velocity change should occur in the Update() method.
		tryVelocityX = self.velocityX
		tryVelocityY = self.velocityY
		
		if self.velocityX < 0:
			x = (self.mapLocation[0] + self.velocityX) / settings.TILE_WIDTH # Gets horizontal tile location after move.
			y1 = (self.mapLocation[1]) / settings.TILE_HEIGHT  # Gets vertical tile location for top.
			y2 = (self.mapLocation[1] + self.size[1]) / settings.TILE_HEIGHT  # Gets vertical tile location for bottom.
			if isObstructed(int(x), int(y1)) or isObstructed(int(x), int(y2)):
				self.velocityX = 0
		elif self.velocityX > 0:
			x = (self.mapLocation[0] + self.size[0] + self.velocityX) / settings.TILE_WIDTH
			y1 = (self.mapLocation[1]) / settings.TILE_HEIGHT 
			y2 = (self.mapLocation[1] + self.size[1]) / settings.TILE_HEIGHT
			if isObstructed(int(x), int(y1)) or isObstructed(int(x), int(y2)):
				self.velocityX = 0
		if self.velocityY < 0:
			y = (self.mapLocation[1] + self.velocityY) / settings.TILE_HEIGHT
			x1 = (self.mapLocation[0]) / settings.TILE_WIDTH
			x2 = (self.mapLocation[0] + self.size[0]) / settings.TILE_WIDTH
			if isObstructed(int(x1), int(y)) or isObstructed(int(x2), int(y)):
				self.velocityY = 0
		elif self.velocityY > 0:
			y = (self.mapLocation[1]  + self.size[1] + self.velocityY) / settings.TILE_HEIGHT
			x1 = (self.mapLocation[0]) / settings.TILE_WIDTH
			x2 = (self.mapLocation[0] + self.size[0]) / settings.TILE_WIDTH
			if isObstructed(int(x1), int(y)) or isObstructed(int(x2), int(y)):
				self.velocityY = 0
		if (tryVelocityX > 0 and self.velocityX == 0) or (tryVelocityY > 0 and self.velocityY == 0): #animating but not moving.
			self.isMoving = True
		else:
			self.isMoving = False
				
	def CheckEntityCollision(self, entities):
		"""Checks to see if there is a collision between two entities."""
		for ent in entities:
			if ent is not self:
				if ent.collidable or ent.trigger: # check if should collision check
					if self.touchRect.colliderect(ent.touchRect):
						if ent.collidable and self.collidable: # its a physical collision
							self.PushAgainstEntity(ent)
						if ent.trigger is not None: # theres a collision and should be an even triggered
							if self is Entity.Player:
								ent.trigger(ent)
							elif ent.triggerAll:
								ent.trigger(ent)
	
	def PushAgainstEntity(self, ent):
		"""Checks to see if the entity pushes against another entity.
		If so, this entity slows down, and the other is pushed by increasing its velocity."""
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
			
	def UpdateFrame(self):
		"""Updates animation Frame."""
		# Not moving.
		if self.velocityX != 0 or self.velocityY != 0:
			if self.frame >= len(self.currentAnimation):
				self.frame = 0
			self.SetFrame(self.frame)
			self.frame = self.frame + settings.ENTITY_ANIMATION_SPEED
		elif self.frame != 0:
			self.frame = 0 # TODO: Why are there two things that appear to do the same thing. self.frame should probably be inside of self.SetFrame(0).
			self.SetFrame(0)
			
	def SetLocation(self, coordinates):
		"""Sets the location of the entity on the map."""
		self.mapLocation = coordinates
		self.UpdateLocation() # TODO: Why is move contained in set locatioN? When I think set location, I don't expect the entity to move as well.
	
	def SetFrame(self, frame):
		"""Sets the animation frame for the entity."""
		if self.currentAnimation is not None:
			frame = self.currentAnimation[int(frame)]
			frameX = int(frame)%self.framesPerRow
			frameY = int(int(frame)/self.framesPerRow)
			self.frameRect.left = frameX * self.frameSize[0]*self.scaleFactor
			self.frameRect.top = frameY * self.frameSize[1]*self.scaleFactor
	
	def UpdateLocation(self):
		"""Updates the entity's location based on velocity."""
		# TODO: Why is this also not part of update?
		self.mapLocation = self.mapLocation[0] + self.velocityX, self.mapLocation[1] + self.velocityY
		self.rect.left = self.mapLocation[0] + self.spriteOffset[0]
		self.rect.top = self.mapLocation[1] - self.size[1] + self.spriteOffset[1]
		self.touchRect.left = self.rect.left
		self.touchRect.top= self.rect.top
		self.isMoving = True
