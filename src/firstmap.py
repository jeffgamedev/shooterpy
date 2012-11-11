from map import Map
from overlay import TextBoxHelper

def Start(parent):
	print "start"
	Tarshan = Map.CurrentMap.AddEntity(210, 170, 1, "tarshan.png")
	TimeHero = Map.CurrentMap.AddEntity(210, 170, 1, "timehero.png")
	Blane = Map.CurrentMap.AddEntity(170, 150, 1, "blane.png")
	Blane.SetControl(True)
	Map.CurrentMap.camera.SetTarget(Blane)	
	Tarshan.SetFollowTarget(Blane, 6)
	TimeHero.SetFollowTarget(Blane, 12)

def Test(parent):
	Map.CurrentMap.RemoveEntity(parent)
	TextBoxHelper.Instance.Notification("Picked up Computer Chip")
	
def GuardJoin(parent):
	TextBoxHelper.Instance.TextBox("TL_port_blu.bmp", "Hello sir Blane. I shall join you on your journey.")
	TextBoxHelper.Instance.Notification("GUARD Joined the Group")
	parent.trigger = None
	parent.SetFollowTarget(Map.CurrentMap.GetPlayer(), 18)