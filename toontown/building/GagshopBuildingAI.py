#Embedded file name: toontown.building.GagshopBuildingAI
from toontown.building import DistributedDoorAI
from toontown.building import DistributedGagshopInteriorAI
from toontown.building import DoorTypes
from pandac.PandaModules import *
from toontown.toon import NPCToons

class GagshopBuildingAI:

    def __init__(self, air, exteriorZone, interiorZone, blockNumber):
        self.air = air
        self.exteriorZone = exteriorZone
        self.interiorZone = interiorZone
        self.blockNumber = blockNumber
        self.setup(blockNumber)

    def cleanup(self):
        for npc in self.npcs:
            npc.requestDelete()

        del self.npcs
        self.door.requestDelete()
        del self.door
        self.insideDoor.requestDelete()
        del self.insideDoor
        self.interior.requestDelete()
        del self.interior

    def setup(self, blockNumber):
        self.interior = DistributedGagshopInteriorAI.DistributedGagshopInteriorAI(blockNumber, self.air, self.interiorZone)
        self.interior.generateWithRequired(self.interiorZone)
        self.npcs = NPCToons.createNpcsInZone(self.air, self.interiorZone)
        door = DistributedDoorAI.DistributedDoorAI(self.air, blockNumber, DoorTypes.EXT_STANDARD)
        insideDoor = DistributedDoorAI.DistributedDoorAI(self.air, blockNumber, DoorTypes.INT_STANDARD)
        door.setOtherDoor(insideDoor)
        insideDoor.setOtherDoor(door)
        door.zoneId = self.exteriorZone
        insideDoor.zoneId = self.interiorZone
        door.generateWithRequired(self.exteriorZone)
        insideDoor.generateWithRequired(self.interiorZone)
        self.door = door
        self.insideDoor = insideDoor

    def getBlock(self):
        return (self.blockNumber, self.interiorZone)

    def isSuitBlock(self):
        return False

    def isEstablishedSuitBlock(self):
        return False
