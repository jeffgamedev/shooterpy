##################################################################
# File:          player_attributes.py
# Project:       Shooter 1, II
# Date Created:  October 20, 2012    
#
# Description:   This file contains player attributes and
#                Skills
#################################################################

class Attribute:
    """one individual attribute"""
    def __init__(self, lowAttrib, highAttrib, balance): # Balance 1-100
        self.lowAttrib = lowAttrib
        self.highAttrib = highAttrib
        self.balance = balance
         
class PlayerAttributes:
    """Attribute Continuums that make up the player's personality and influences their skill-learning"""
    def __init__(self):
        """Set Defaults"""
        attrib  = {"Learning" : Attribute("Academic", "Tinkerer", 50)}
        attrib += {"Decisions" : Attribute("Pragmatism", "Creativity", 50)}
        attrib += {"Study" : Attribute("Intelligence", "Athleticism", 50)}
        attrib += {"Personality" : Attribute("Initiative", "Influence", 50)}
        attrib += {"Honor" : Attribute("Altruist", "Mercenary", 50)}
        attrib += {"Discipline" : Attribute("Magical", "Mechanical", 50)}
        
class Skill:
    """Individual Skills"""
    def __init__(self, startingValue):
        self.value = startingValue
        
class PlayerSkills:
    def __init__(self):
        """Skills for individual players"""
        skills  = {"Leadership" : Skill(0)} # Supports whole team in battle
        skills += {"Fighting" : Skill(0)}   # increases hit or damage to enemy
        skills += {"Magic" : Skill(0)}      # magical effectiveness in battle
        skills += {"Tech" : Skill(0)}       # tech effectiveness in battle (eg. rocket launcher)
        skills += {"Healing" : Skill(0)}    # heals party members in battle or out
        skills += {"Lockpicking" : Skill(0)}# non-battle skill, higher skills cracks harder doors
        skills += {"Haggle" : Skill(0)}     # less cost in buying, more profit from selling
        skills += {"Persuade" : Skill(0)}   # non-battle skill, get what you want from towns ppl etc
    
