from NotificationBox import NotificationBox

def option1(game):
	game.interruptEventSystem.Add(NotificationBox(game, "You chose option 1."))

def option2(game):
	game.interruptEventSystem.Add(NotificationBox(game, "You chose option 2."))
	
def option3(game):
	game.interruptEventSystem.Add(NotificationBox(game, "You chose option 3."))