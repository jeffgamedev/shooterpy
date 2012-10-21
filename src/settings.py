############################################################
# File:		settings.py
# Project:	Shooter 1, II
# Date Created:	Oct 13, 2012	
#
# Description: 	This file is used to store game-wide settings
#	so as to reduce the amount of refactoring done if
#	one of these settings need to change.
#
############################################################

#### Game-Related settings ####

# Screen related
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
# Starting map for the game
STARTING_MAP = "start.tmx"

# TextBox Settings
TEXTBOX_X_MARGIN = 10
TEXTBOX_Y_MARGIN = 5
TEXTBOX_SIZE = (SCREEN_WIDTH-2*TEXTBOX_X_MARGIN, 200-2*TEXTBOX_Y_MARGIN)
TEXTBOX_POSITION = (0+TEXTBOX_X_MARGIN, 400+TEXTBOX_Y_MARGIN)
TEXTBOX_COLOR = (0,0,255)
TEXTBOX_TEXT_COLOR = (255,255,255)
TEXTBOX_OPACITY = 200
TEXTBOX_BORDER_COLOR = (200, 200, 200)