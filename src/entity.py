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


class Entity:
	"""Entity class is the base class for all person-like characters in the game"""
	def __init__(self, entityName, startX, startY):
		self.mapLocation = (startX, startY)
		self.name = entityName
		self.layer = 0 # which layer entity is on top of
		self.visible = True

	
