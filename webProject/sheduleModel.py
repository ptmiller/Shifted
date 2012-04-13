class SchedulePage(object):
    """Schedule Object for Interactions"""

    shifts = {}

    def __init__(slef, name):
        self.name = name
        self.shifts = []
        self.users = []
        ChatRoom.rooms[name] = self

    def addSubscriber(self, subscriber):
        self.users.append(subscriber)
        subscriber.send
