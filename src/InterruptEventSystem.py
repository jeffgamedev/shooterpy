import Queue

class InterruptEventSystem:
	"""Handles interrupt Event functionality and user interaction for the main game loop"""

	def __init__(self, windowSurfaceObject):
		self.windowSurfaceObject = windowSurfaceObject
		self.currentEvent = None
		self.eventQueue = Queue.Queue()

	def Display(self):
		"""Put this in the main game loop. Will only display if the textbox has focus."""
		if self.HasActiveEvent():
			self.currentEvent.Show()

	def Dismiss(self):
		"""Dismisses the InterruptEvent."""
		self.currentEvent = None
	
	def HasActiveEvent(self):
		"""Returns whether or there is an event waiting to be dismissed"""
		return self.currentEvent <> None
	
	def Update(self):
		if self.currentEvent == None and not self.eventQueue.empty():
			self.currentEvent = self.eventQueue.get()
			print "DEBUG: getting from queue"

	# depricated!
	def GetInput(self):
		"""DEPRICATED: Works for pygame in general. But functionality has been replaced in the input.py file"""
		if Input.keyboard[pygame.K_RETURN]:
			self.currentEvent = None

	# Truly polymorphic as opposed to separate addTextBox and addNotificationBox Classes
	def Add(self, eventObject):
		"""Adds an event to the queue"""
		self.eventQueue.put(eventObject)