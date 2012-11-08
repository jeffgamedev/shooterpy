import tiledtmxloader
import settings
import tiledtmxloader.helperspygame
import pygame
from camera import Camera
from entity import Entity
from characterentity import CharacterEntity
from itementity import ItemEntity

class Map(object):
	Path = "../maps/"
	CurrentMap = None
	def __init__(self):	
		self.size = 0, 0		
		self.mapData = None		
		self.resources = tiledtmxloader.helperspygame.ResourceLoaderPygame()
		self.renderer = tiledtmxloader.helperspygame.RendererPygame()
		self.camera = Camera(self.renderer)
		self.spriteLayers = None
		self.obstructions = []
		self.entities = []
		self.updatingEntities = []
		self.script = None
		
	def Update(self):
		self.UpdateEntities()
		self.camera.Update()
			
	def UpdateEntities(self):
		for entity in self.entities:
			if entity.ShouldUpdate(self.renderer._cam_rect): # if entity is on screen
				self.UpdateEntity(entity)
			elif entity in self.updatingEntities: # if entity is not on screen and is in on screen entity list
				self.updatingEntities.remove(entity) # remove from on screen entity list
			
	def UpdateEntity(self, entity):
		if not entity in self.updatingEntities:
			self.updatingEntities.append(entity) #add it to on screen entity list
		entity.Update()
		entity.CheckObstructions(self.GetObs)
		entity.CheckEntityCollision(self.updatingEntities) # only check collision with on screen entities
		entity.Move()
			
	def GetTile(self, x, y, layer):
		if layer >= 0 and layer < len(self.mapData.layers) and x > 0 and y > 0 and x < self.mapData.width and y < self.mapData.height:
			return self.mapData.layers[layer].content2D[x][y]
		return -1
		
	def AddEntity(self, x, y, layer=1, fileName ="blanea.png"):
		entity = CharacterEntity("entity", x, y, fileName)
		self.spriteLayers[layer].add_sprite(entity)		
		self.entities.append(entity)
		return entity
		
	def AddItemEntity(self, index, x, y, trigger=None, layer=1):
		entity = ItemEntity(index, x, y, trigger)
		self.spriteLayers[layer].add_sprite(entity)		
		self.entities.append(entity)
		return entity
		
	def RemoveEntity(self, entity):
		if entity in self.entities:
			self.entities.remove(entity)
		if entity in self.updatingEntities:
			self.updatingEntities.remove(entity)
		for spritelayer in self.spriteLayers:
			if hasattr(spritelayer, 'remove_sprite'):
				spritelayer.remove_sprite(entity)
		print "removed entity"

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
				
		if self.mapData.properties["script"]:
			try:
				self.script = __import__( self.mapData.properties["script"] )
			except:
				self.script = None
				print "no script file of name " + self.mapData.properties["script"]
		else:
			print "no map property 'script'"
			
		objectList = None
		#find object layer
		for i in range(len(self.mapData.layers)):
			if self.mapData.layers[i].is_object_group:
				objectList = self.mapData.layers[i].objects
				break
		
		if objectList is not None:
			self.FilterMapObjects(objectList)

		Map.CurrentMap = self
		
		if self.script and hasattr(self.script, "Start"):
			self.script.Start(self)
	
	def FilterMapObjects(self, objectList):
		for obj in objectList:
			type = obj.type.lower()
			if type == "item": # object type is an item
				index = 0
				trigger = None
				for property in obj.properties:
					if property == "index":
						index = int(obj.properties[property]) # get item index
					if property == "trigger":
						if self.script is not None:
							if hasattr(self.script, obj.properties[property]):
								trigger = getattr(self.script, obj.properties[property])
				self.AddItemEntity(index, obj.x, obj.y, trigger)

	def Render(self, screen):
		if self.spriteLayers is not None:
			for spriteLayer in self.spriteLayers:
				self.camera.renderer.render_layer(screen, spriteLayer)		