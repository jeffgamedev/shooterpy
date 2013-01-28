from Entity import Entity

class ItemEntity(Entity):
	def __init__(self, itemID, startX, startY, trigger = None):
		super (ItemEntity, self).__init__("item", startX, startY, "items.png", (24, 24), (32, 32), 1)
		self.currentAnimation = [0]
		self.collidable = False
		self.trigger = trigger