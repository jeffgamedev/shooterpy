############################################################
# File:        player.py
# Project:    Shooter 1, II
# Date Created:    Oct 18, 2012    
#
# Description:
############################################################

import Entity, PlayerAttributes

class Player(entity.Entity):
    """The Player class is the class for members of the user's party."""
    def __init__(self, entityName, startX, startY):
        super(self, entityName, startX, startY)
        self.hasFocus = False # True for the player that the keyboard controls
        self.description = "" # seen in menu
        self.attributes = player_attributes.PlayerAttributes()
 