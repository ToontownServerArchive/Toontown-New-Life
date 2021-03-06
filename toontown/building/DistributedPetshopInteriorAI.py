#Embedded file name: toontown.building.DistributedPetshopInteriorAI
from direct.distributed import DistributedObjectAI

class DistributedPetshopInteriorAI(DistributedObjectAI.DistributedObjectAI):

    def __init__(self, block, air, zoneId):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        self.block = block
        self.zoneId = zoneId

    def generate(self):
        DistributedObjectAI.DistributedObjectAI.generate(self)

    def getZoneIdAndBlock(self):
        return [self.zoneId, self.block]
