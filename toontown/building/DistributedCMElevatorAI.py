#Embedded file name: toontown.building.DistributedCMElevatorAI
from toontown.building.ElevatorConstants import *
from toontown.building import DistributedBossElevatorAI

class DistributedCMElevatorAI(DistributedBossElevatorAI.DistributedBossElevatorAI):

    def __init__(self, air, bldg, zone, antiShuffle = 0, minLaff = 0):
        DistributedBossElevatorAI.DistributedBossElevatorAI.__init__(self, air, bldg, zone, antiShuffle=antiShuffle, minLaff=minLaff)
        self.type = ELEVATOR_CM
        self.countdownTime = ElevatorData[self.type]['countdown']
