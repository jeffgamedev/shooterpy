import tiledtmxloader
import settings
import tiledtmxloader.helperspygame
from camera import Camera
from entity import Entity

class Map(object):
	def __init__(self):	
		self.size = 0, 0		
		self.mapData = None		
		self.resources = tiledtmxloader.helperspygame.ResourceLoaderPygame()
		self.renderer = tiledtmxloader.helperspygame.RendererPygame()
		self.camera = Camera(self.renderer)
		self.spriteLayers = None		
		self.obstructions = []
		self.entities = []
		
	def Update(self):
		self.UpdateEntities()
		self.camera.Update()
			
	def UpdateEntities(self):
		for entity in self.entities:
			entity.Update()
			entity.CheckObstructions(self.GetObs)
			entity.Move()
			
	def GetTile(self, x, y, layer):
		if layer >= 0 and layer < len(self.mapData.layers) and x > 0 and y > 0 and x < self.mapData.width and y < self.mapData.height:
			return self.mapData.layers[layer].content2D[x][y]
		return -1
		
	def AddEntity(self, x, y, layer=0):
		entity = Entity("entity", x, y)
		self.spriteLayers[layer].add_sprite(entity)
		self.camera.SetTarget(entity)
		self.entities.append(entity)
		
	def GetObs(self, x, y):
		if x >= 0 and  y >= 0 and x < self.mapData.width and y < self.mapData.height:
			return self.obstructions[x][y]
		else:
			return 1 # return 1 for "obstructed" on outside zones
		
	def LoadMap(self, name):
		self.mapData = tiledtmxloader.tmxreader.TileMapParser().parse_decode(name)
		self.resources.load(self.mapData)
		self.spriteLayers = tiledtmxloader.helperspygame.get_layers_from_map(self.resources)
		self.camera.SetBoundaries(0, 0, (self.mapData.width * self.mapData.tilewidth)-(settings.SCREEN_WIDTH), (self.mapData.height * self.mapData.tileheight)-(settings.SCREEN_HEIGHT))
		for i in range(len(self.mapData.layers)):
			if self.mapData.layers[i].name == 'obstruction':
				self.obstructions = self.mapData.layers[i].content2D
				self.mapData.layers.pop(i)
				self.spriteLayers.pop(i)
				break
		
	def Render(self, screen):
		if self.spriteLayers is not None:
			for spriteLayer in self.spriteLayers:
				self.camera.renderer.render_layer(screen, spriteLayer)