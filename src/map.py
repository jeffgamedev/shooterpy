import tiledtmxloader
import settings
import tiledtmxloader.helperspygame

class Map(object):
	def __init__(self):
		self.x = 0
		self.y = 0
		self.resources = tiledtmxloader.helperspygame.ResourceLoaderPygame()
		self.renderer = tiledtmxloader.helperspygame.RendererPygame()
		self.renderer.set_camera_position_and_size(self.x, self.y, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, "topleft")
		self.sprite_layers = None
		
	def loadMap(self, name):		
		self.resources.load(tiledtmxloader.tmxreader.TileMapParser().parse_decode(name)) #map = tiledtmxloader.tmxreader.TileMapParser().parse_decode(name)
		self.sprite_layers = tiledtmxloader.helperspygame.get_layers_from_map(self.resources)		
		
	def render(self, screen):
		if self.sprite_layers is not None:
			for sprite_layer in self.sprite_layers:
				self.renderer.render_layer(screen, sprite_layer)
		