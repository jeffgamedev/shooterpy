import settings

class Camera(object):
	def __init__(self, renderer):		
		self.position = 0, 0
		self.lastPosition = 0, 0
		self.mode = "follow"
		self.target = None
		self.bounds = 0, 0, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT		
		self.renderer = renderer
		self.renderer.set_camera_position_and_size(self.position[0], self.position[1], settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, "topleft")
	
	def SetBoundaries(self, left, top, width, height):
		self.bounds = left, top, width, height
	
	def SetTarget(self, entity):
		self.target = entity
		
	def Update(self):
		if self.mode == "follow" and self.target != None:
			self.position = (self.target.mapLocation[0] - (self.target.size[0])/2) - (settings.SCREEN_WIDTH/2), (self.target.mapLocation[1] - (self.target.size[1])/2) - (settings.SCREEN_HEIGHT/2)

		if self.position != self.lastPosition:
			self.position = max(self.bounds[0], min((self.position[0]), self.bounds[2])), max(self.bounds[1], min((self.position[1]), self.bounds[3]))
			self.renderer.set_camera_position(self.position[0], self.position[1], 'topleft')
			self.lastPosition = self.position
			print self.position