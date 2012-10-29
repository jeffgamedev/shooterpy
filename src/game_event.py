# # #
### DO NOT USE! Idea replaced in overlay.py by InterruptEventSystem.
### This might be used later for non-interrupt events.
# # #

import Queue

class GameEventTypes:
    TextBoxEvent = 1

class GameEvent:
    """This is a single game event such as a textbox or scripted character movement"""
    def __init__(self, type, function_call, arguments):
        self.type = type
        self.function_call = function_call
        self.arguments = arguments
    
class GameEventQueue:
    """This holds a queue of game events that will wait for execution of the first one before moving on to the next"""
    def __init__(self):
        self.eventQueue = Queue.Queue()
        
    def Next(self):
        """This will pop a new event off the queue and call the method with supplied arguments"""
        
        
q = GameEventQueue()
q.eventQueue.put(GameEvent(GameEventTypes.TextBoxEvent, "", ""))