############################################################
# File:           npc.py
# Project:        Shooter 1, II
# Date Created:   Oct 18, 2012    
#
# Description:     Town Entities. Enemy Entities.
#
############################################################

import Entity

class NPC(entity.Entity):
    """Contains entity information distinct to NPCs"""
    def __init__(self, entityName, startX, startY, ScriptFile):
        self.ScriptFile = ScriptFile  

