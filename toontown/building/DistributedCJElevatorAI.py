#Embedded file name: toontown.building.DistributedCJElevatorAI
from toontown.building.ElevatorConstants import *
from toontown.building import DistributedBossElevatorAI

class DistributedCJElevatorAI(DistributedBossElevatorAI.DistributedBossElevatorAI):

    def __init__(self, air, bldg, zone, antiShuffle = 0, minLaff = 0):
        DistributedBossElevatorAI.DistributedBossElevatorAI.__init__(self, air, bldg, zone, antiShuffle=antiShuffle, minLaff=minLaff)
        self.type = ELEVATOR_CJ
        self.countdownTime = ElevatorData[self.type]['countdown']
