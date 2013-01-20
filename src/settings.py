############################################################
# File:		settings.py
# Project:	Shooter 1, II
# Date Created:	Oct 13, 2012	
#
# Description: 	This file is used to store game-wide settings
#	so as to reduce the amount of refactoring done if
#	one of these settings need to change. This file should not
#	contain any methods.
#
############################################################

#### Game-Related settings ####

# Screen related
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
FRAMES_PER_SECOND = 30

# Message Box Settings
TEXTBOX_X_MARGIN = 10
TEXTBOX_Y_MARGIN = 5
TEXTBOX_SIZE = (SCREEN_WIDTH-2*TEXTBOX_X_MARGIN, 200-2*TEXTBOX_Y_MARGIN)
TEXTBOX_POSITION = (0+TEXTBOX_X_MARGIN, 400+TEXTBOX_Y_MARGIN)
TEXTBOX_COLOR = (0,0,255)
TEXTBOX_TEXT_COLOR = (255,255,255)
TEXTBOX_BORDER_COLOR = (200, 200, 200)
TEXTBOX_OPACITY = 220
TEXTBOX_FONT_SIZE = 22

NOTIFICATION_FONT_SIZE = 22
NOTIFICATION_BOX_SIZE = (240, 70)
NOTIFICATION_BOX_POSITION = (SCREEN_WIDTH/2-(NOTIFICATION_BOX_SIZE[0]/2), SCREEN_HEIGHT/2-(NOTIFICATION_BOX_SIZE[1]/2 ))
NOTIFICATION_BOX_TEXT_MARGIN = NOTIFICATION_BOX_SIZE[1]/2-NOTIFICATION_FONT_SIZE*.75
							
# MAP SETTINGS
STARTING_MAP = "start.tmx"
TILE_WIDTH = 32
TILE_HEIGHT = 32

# Player Control Settings
FRICTION = 0.6 # TODO: Comment. In pixels?
COLLISION_SLOWDOWN = .8 # TODO: Comment. In pixels?
PUSH_SPEED = 1 # TODO: Is this pixels pushed? Please specifiy in constant name.
PARTY_STEPS_LOGGED = 20 # What is this for?

# Sprite Settings
SPRITE_SCALE_FACTOR = 2
ENTITY_ANIMATION_SPEED = 0.25 # TODO: Comment. What does this mean? every quarter of a second, the frame updates? If so, please change name to SECONDS_PER_FRAME_CHANGE.
DIRECTION_UP = 0
DIRECTION_DOWN = 1
DIRECTION_LEFT = 2
DIRECTION_RIGHT = 3

def Clamp(num, minNum, maxNum): # TODO: Should not be in settings.py. Maybe an EntityHelper.py or something if it's used outside of entity.py.
	return max(minNum, min(num, maxNum))