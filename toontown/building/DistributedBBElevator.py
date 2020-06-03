#Embedded file name: toontown.building.DistributedBBElevator
from toontown.building import DistributedElevator
from toontown.building import DistributedBossElevator
from toontown.building.ElevatorConstants import *
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import TTLocalizer

class DistributedBBElevator(DistributedBossElevator.DistributedBossElevator):

    def __init__(self, cr):
        DistributedBossElevator.DistributedBossElevator.__init__(self, cr)
        self.type = ELEVATOR_BB
        self.countdownTime = ElevatorData[self.type]['countdown']
        self.elevatorPoints = BossbotElevatorPoints

    def setupElevator(self):
        geom = base.cr.playGame.hood.loader.geom
        self.elevatorModel = loader.loadModel('phase_5/models/cogdominium/tt_m_ara_csa_elevatorB')
        self.leftDoor = self.elevatorModel.find('**/left-door')
        if self.leftDoor.isEmpty():
            self.leftDoor = self.elevatorModel.find('**/left_door')
        self.rightDoor = self.elevatorModel.find('**/right-door')
        if self.rightDoor.isEmpty():
            self.rightDoor = self.elevatorModel.find('**/right_door')
        locator = geom.find('**/elevator_locator')
        self.elevatorModel.reparentTo(locator)
        self.elevatorModel.setScale(2)
        self.elevatorModel.setPos(0, -4.5, 0)
        DistributedElevator.DistributedElevator.setupElevator(self)

    def getDestName(self):
        return TTLocalizer.ElevatorBossBotBoss
