#Embedded file name: toontown.coghq.boardbothq.DistributedBoardOfficeElevatorExtAI
from otp.ai.AIBase import *
from toontown.toonbase import ToontownGlobals
from direct.distributed.ClockDelta import *
from toontown.building.ElevatorConstants import *
from toontown.building import DistributedElevatorExtAI
from direct.fsm import ClassicFSM
from direct.fsm import State
from direct.task import Task
from toontown.coghq import CogDisguiseGlobals

class DistributedBoardOfficeElevatorExtAI(DistributedElevatorExtAI.DistributedElevatorExtAI):

    def __init__(self, air, bldg, boardofficeId, antiShuffle = 0, minLaff = 0):
        DistributedElevatorExtAI.DistributedElevatorExtAI.__init__(self, air, bldg, antiShuffle=antiShuffle, minLaff=minLaff)
        self.boardofficeId = boardofficeId
        self.cogDept = ToontownGlobals.cogHQZoneId2deptIndex(self.boardofficeId)
        self.type = ELEVATOR_BOARD_OFFICE
        self.countdownTime = ElevatorData[self.type]['countdown']

    def getBoardOfficeId(self):
        return self.boardofficeId

    def avIsOKToBoard(self, av):
        if not DistributedElevatorExtAI.DistributedElevatorExtAI.avIsOKToBoard(self, av):
            return False
        return True

    def elevatorClosed(self):
        numPlayers = self.countFullSeats()
        if numPlayers > 0:
            players = []
            for i in self.seats:
                if i not in (None, 0):
                    players.append(i)

            boardofficeZone = self.bldg.createBoardOffice(self.boardofficeId, players)
            for seatIndex in xrange(len(self.seats)):
                avId = self.seats[seatIndex]
                if avId:
                    self.sendUpdateToAvatarId(avId, 'setBoardOfficeInteriorZone', [boardofficeZone])
                    self.clearFullNow(seatIndex)

        else:
            self.notify.warning('The elevator left, but was empty.')
        self.fsm.request('closed')

    def enterClosed(self):
        DistributedElevatorExtAI.DistributedElevatorExtAI.enterClosed(self)
        self.fsm.request('opening')

    def sendAvatarsToDestination(self, avIdList):
        if len(avIdList) > 0:
            boardofficeZone = self.bldg.createBoardOffice(self.boardofficeId, avIdList)
            for avId in avIdList:
                if avId:
                    self.sendUpdateToAvatarId(avId, 'setBoardOfficeInteriorZoneForce', [boardofficeZone])
