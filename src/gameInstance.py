import settings, pygame
from map import Map
from overlay import InterruptEventSystem

class GameInstance:
	"""Main repository for game data when running.""" 
	def __init__(self):
		self.gameSurface = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
		self.interruptEventSystem = InterruptEventSystem(self.gameSurface)
		self.mapSystem = Map()
		self.mapSystem.LoadMap(settings.STARTING_MAP)