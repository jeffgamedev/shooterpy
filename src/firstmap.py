from map import Map
from overlay import TextBoxHelper

def Start(parent):
	print "start"
	Blane = Map.CurrentMap.AddEntity(170, 150)
	Blane.SetControl(True)
	Map.CurrentMap.camera.SetTarget(Blane)
	Map.CurrentMap.AddEntity(210, 170)
	Map.CurrentMap.AddEntity(240, 180)

def Test(parent):
	Map.CurrentMap.RemoveEntity(parent)
	TextBoxHelper.Instance.Notification("Picked up Computer Chip")
	TextBoxHelper.Instance.TextBox("TL_port_blu.bmp", "Hey sir doobus. This is pretty neato!")