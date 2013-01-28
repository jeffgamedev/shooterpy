class InterruptEvent:
	"""Interrupt Events are events that occur in the UI such as a text box that must be dismissed before 
	other game logic can continue"""
	def __init___ (self):
		self.tempSurface = None
		self.destinationSurface = None
		self.rect = None
	
	def Show(self):
		"""Does not need to be overridden if the following fields are instantiated."""
		if self.tempSurface == None:
			raise Exception("tempSurface has not yet been instantiated.")
		elif self.destinationSurface == None:
			raise Exception("destinationSurface has not yet been instantiated.")
		elif self.rect == None:
			raise Exception("rect has not yet been instantiated.")
		else:
			self.destinationSurface.blit(self.tempSurface, self.rect)
		
