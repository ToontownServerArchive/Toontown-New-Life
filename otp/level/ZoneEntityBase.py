#Embedded file name: otp.level.ZoneEntityBase
from otp.level import Entity
from otp.level import LevelConstants

class ZoneEntityBase(Entity.Entity):

    def __init__(self, level, entId):
        Entity.Entity.__init__(self, level, entId)
        self.zoneId = None

    def destroy(self):
        del self.zoneId
        Entity.Entity.destroy(self)

    def isUberZone(self):
        return self.entId == LevelConstants.UberZoneEntId

    def setZoneId(self, zoneId):
        self.zoneId = zoneId

    def getZoneId(self):
        return self.zoneId

    def getZoneNum(self):
        return self.entId
