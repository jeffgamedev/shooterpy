from map import Map
from overlay import TextBoxHelper

def Start(parent):
	if len(Map.CurrentMap.GetParty()) == 0:
		Tarshan = Map.CurrentMap.AddCharacterEntity(210, 170, 1, "tarshan.png")
		TimeHero = Map.CurrentMap.AddCharacterEntity(210, 170, 1, "timehero.png")
		Blane = Map.CurrentMap.AddCharacterEntity(170, 150, 1, "blane.png")
		Blane.SetControl(True)
		Map.CurrentMap.camera.SetTarget(Blane)
		Tarshan.SetFollowTarget(Blane, 6)
		TimeHero.SetFollowTarget(Blane, 12)

def Test(parent):
	#TextBoxHelper.Instance.Notification("Picked up Computer Chip")
	Map.CurrentMap.ChangeMap("elmappo.tmx", (610, 170))
	Map.CurrentMap.RemoveEntity(parent)
	
def GuardJoin(parent):
	#TextBoxHelper.Instance.TextBox("TL_port_blu.bmp", "Hello sir Blane. I shall join you on your journey.")
	#TextBoxHelper.Instance.Notification("GUARD Joined the Group")
	parent.trigger = None
	parent.SetFollowTarget(Map.CurrentMap.GetPlayer(), 18)