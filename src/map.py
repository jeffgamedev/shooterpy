import tiledtmxloader
import settings
import tiledtmxloader.helperspygame
from entity import Entity

class Map(object):
	def __init__(self):	
		self.size = 0, 0
		self.speed = 4, .2
		self.position = 0, 0
		self.lastPosition = 0, 0		
		self.mapData = None
		self.resources = tiledtmxloader.helperspygame.ResourceLoaderPygame()
		self.renderer = tiledtmxloader.helperspygame.RendererPygame()
		self.renderer.set_camera_position_and_size(self.position[0], self.position[1], settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, "topleft")
		self.spriteLayers = None
		self.obstructions = []
		self.entities = []
		
	def Update(self):
		self.Scroll()
			
	def Scroll(self):
		self.position = max(0, min((self.position[0] + self.speed[0]), self.size[0])), max(0, min((self.position[1] + self.speed[1]), self.size[1]))
		if self.position != self.lastPosition:
			self.renderer.set_camera_position(self.position[0], self.position[1], 'topleft')
			self.lastPosition = self.position
			
	def GetTile(self, x, y, layer):
		if layer >= 0 and layer < len(self.mapData.layers) and x > 0 and y > 0 and x < self.mapData.width and y < self.mapData.height:
			return self.mapData.layers[layer].content2D[x][y]
		return -1
		
	def AddEntity(self, x, y, layer=0):
		pass
		
	def GetObs(self, x, y):
		if x >= 0 and  y >= 0 and x < self.mapData.width and y < self.mapData.height:
			return self.obstructions[x][y]
		else:
			return 1 # return 1 for "obstructed" on outside zones
		
	def LoadMap(self, name):
		self.mapData = tiledtmxloader.tmxreader.TileMapParser().parse_decode(name)
		self.resources.load(self.mapData)
		self.spriteLayers = tiledtmxloader.helperspygame.get_layers_from_map(self.resources)
		self.size = self.mapData.width * self.mapData.tilewidth, self.mapData.height * self.mapData.tileheight
		for i in range(len(self.mapData.layers)):
			if self.mapData.layers[i].name == 'obstruction':
				self.obstructions = self.mapData.layers[i].content2D
				self.mapData.layers.pop(i)
				self.spriteLayers.pop(i)
				break
		
	def Render(self, screen):
		if self.spriteLayers is not None:
			for spriteLayer in self.spriteLayers:
				self.renderer.render_layer(screen, spriteLayer)