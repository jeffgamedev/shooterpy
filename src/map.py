import tiledtmxloader
import settings
import tiledtmxloader.helperspygame
import pygame
from camera import Camera
from entity import Entity

class Map(object):
	Path = "../maps/"
	class MapObject(tiledtmxloader.helperspygame.SpriteLayer.Sprite):
		def __init__(self, x, y, width, height, spriteFileName, index):
			self.mapLocation = x, y
			self.rect = pygame.Rect(x, y, x + width, y + height)
			self.image = None
			self.frameRect = None
			if spriteFileName is not None:
				self.frameRect = pygame.Rect(index * 100, 0, (index * 100) + 100, 100)
				self.image = pygame.image.load(Entity.Path + spriteFileName)
			else:
				self.image = pygame.Surface((width, height), pygame.SRCALPHA)				
				self.image.fill((255, 0, 0, 200))
			super(Map.MapObject, self).__init__(self.image, self.rect, self.frameRect)
	
	def __init__(self):	
		self.size = 0, 0		
		self.mapData = None		
		self.resources = tiledtmxloader.helperspygame.ResourceLoaderPygame()
		self.renderer = tiledtmxloader.helperspygame.RendererPygame()
		self.camera = Camera(self.renderer)
		self.spriteLayers = None
		self.objects = []
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
			
		if self.spriteLayers[0] is not None:
			self.spriteLayers[0].sprites.sort(key=lambda x: x.rect.top, reverse=False)
			
	def GetTile(self, x, y, layer):
		if layer >= 0 and layer < len(self.mapData.layers) and x > 0 and y > 0 and x < self.mapData.width and y < self.mapData.height:
			return self.mapData.layers[layer].content2D[x][y]
		return -1
		
	def AddEntity(self, x, y, layer=0):
		entity = Entity("entity", x, y, "blanea.png")
		self.spriteLayers[layer].add_sprite(entity)
		self.camera.SetTarget(entity)
		self.entities.append(entity)
		
	def GetObs(self, x, y):
		if x >= 0 and  y >= 0 and x < self.mapData.width and y < self.mapData.height:
			return self.obstructions[x][y]
		else:
			return 1 # return 1 for "obstructed" on outside zones
		
	def LoadMap(self, name):
		self.mapData = tiledtmxloader.tmxreader.TileMapParser().parse_decode(Map.Path + name)
		self.resources.load(self.mapData)
		self.spriteLayers = tiledtmxloader.helperspygame.get_layers_from_map(self.resources)
		self.camera.SetBoundaries(0, 0, (self.mapData.width * self.mapData.tilewidth)-(settings.SCREEN_WIDTH), (self.mapData.height * self.mapData.tileheight)-(settings.SCREEN_HEIGHT))
		#find obstructions layer
		for i in range(len(self.mapData.layers)):
			if self.mapData.layers[i].name == 'obstruction':
				self.obstructions = self.mapData.layers[i].content2D
				self.mapData.layers.pop(i)
				self.spriteLayers.pop(i)
				break
				
		objectList = None
		#find object layer
		for i in range(len(self.mapData.layers)):
			if self.mapData.layers[i].is_object_group:
				objectList = self.mapData.layers[i].objects
				#self.mapData.layers.pop(i)
				#self.spriteLayers.pop(i)
				break
		
		if objectList is not None:
			self.FilterMapObjects(objectList)
				
	def FilterMapObjects(self, objectList):
		for obj in objectList:
			imageFileName = None
			index = 0
			for property in obj.properties:
				if property == "image":
					imageFileName = obj.properties[property]
				if property == "index":
					index = int(obj.properties[property])
				#print property, obj.properties[property]
			newObject = Map.MapObject(obj.x, obj.y, obj.width, obj.height, imageFileName, index)
			self.objects.append(newObject)
			if self.spriteLayers is not None:
				self.spriteLayers[0].add_sprite(newObject)
		
		
	def Render(self, screen):
		if self.spriteLayers is not None:
			for spriteLayer in self.spriteLayers:
				self.camera.renderer.render_layer(screen, spriteLayer)