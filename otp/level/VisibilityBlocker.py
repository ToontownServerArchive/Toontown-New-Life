#Embedded file name: otp.level.VisibilityBlocker
from otp.level import Entity

class VisibilityBlocker:

    def __init__(self):
        self.__nextSetZoneDoneEvent = None

    def destroy(self):
        self.cancelUnblockVis()

    def requestUnblockVis(self):
        if self.__nextSetZoneDoneEvent is None:
            self.__nextSetZoneDoneEvent = self.level.cr.getNextSetZoneDoneEvent()
            self.acceptOnce(self.__nextSetZoneDoneEvent, self.okToUnblockVis)
            self.level.forceSetZoneThisFrame()

    def cancelUnblockVis(self):
        if self.__nextSetZoneDoneEvent is not None:
            self.ignore(self.__nextSetZoneDoneEvent)
            self.__nextSetZoneDoneEvent = None

    def isWaitingForUnblockVis(self):
        return self.__nextSetZoneDoneEvent is not None

    def okToUnblockVis(self):
        self.cancelUnblockVis()
