#Embedded file name: toontown.coghq.boardbothq.BoardOfficeInterior
from direct.directnotify import DirectNotifyGlobal
from toontown.battle import BattlePlace
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.showbase import BulletinBoardWatcher
from pandac.PandaModules import *
from otp.distributed.TelemetryLimiter import RotationLimitToH, TLGatherAllAvs
from toontown.toon import Toon
from toontown.toonbase import ToontownGlobals
from toontown.hood import ZoneUtil
from toontown.toonbase import TTLocalizer
from toontown.toontowngui import TTDialog
from toontown.toonbase import ToontownBattleGlobals
from toontown.coghq.boardbothq import DistributedBoardOffice
from toontown.nametag import NametagGlobals

class BoardOfficeInterior(BattlePlace.BattlePlace):
    notify = DirectNotifyGlobal.directNotify.newCategory('BoardOfficeInterior')

    def __init__(self, loader, parentFSM, doneEvent):
        BattlePlace.BattlePlace.__init__(self, loader, doneEvent)
        self.parentFSM = parentFSM
        self.zoneId = loader.boardofficeId
        self.fsm = ClassicFSM.ClassicFSM('BoardOfficeInterior', [State.State('start', self.enterStart, self.exitStart, ['walk', 'teleportIn', 'fallDown']),
         State.State('walk', self.enterWalk, self.exitWalk, ['push',
          'sit',
          'stickerBook',
          'WaitForBattle',
          'battle',
          'died',
          'teleportOut',
          'squished',
          'DFA',
          'fallDown',
          'stopped']),
         State.State('stopped', self.enterStopped, self.exitStopped, ['walk', 'teleportOut', 'stickerBook']),
         State.State('sit', self.enterSit, self.exitSit, ['walk', 'died', 'teleportOut']),
         State.State('push', self.enterPush, self.exitPush, ['walk', 'died', 'teleportOut']),
         State.State('stickerBook', self.enterStickerBook, self.exitStickerBook, ['walk',
          'battle',
          'DFA',
          'WaitForBattle',
          'died',
          'teleportOut']),
         State.State('WaitForBattle', self.enterWaitForBattle, self.exitWaitForBattle, ['battle',
          'walk',
          'died',
          'teleportOut']),
         State.State('battle', self.enterBattle, self.exitBattle, ['walk', 'teleportOut', 'died']),
         State.State('fallDown', self.enterFallDown, self.exitFallDown, ['walk', 'died', 'teleportOut']),
         State.State('squished', self.enterSquished, self.exitSquished, ['walk', 'died', 'teleportOut']),
         State.State('teleportIn', self.enterTeleportIn, self.exitTeleportIn, ['walk',
          'teleportOut',
          'quietZone',
          'died']),
         State.State('teleportOut', self.enterTeleportOut, self.exitTeleportOut, ['teleportIn',
          'FLA',
          'quietZone',
          'WaitForBattle']),
         State.State('DFA', self.enterDFA, self.exitDFA, ['DFAReject', 'teleportOut']),
         State.State('DFAReject', self.enterDFAReject, self.exitDFAReject, ['walkteleportOut']),
         State.State('died', self.enterDied, self.exitDied, ['teleportOut']),
         State.State('FLA', self.enterFLA, self.exitFLA, ['quietZone']),
         State.State('quietZone', self.enterQuietZone, self.exitQuietZone, ['teleportIn']),
         State.State('final', self.enterFinal, self.exitFinal, ['start'])], 'start', 'final')

    def load(self):
        self.parentFSM.getStateNamed('boardofficeInterior').addChild(self.fsm)
        BattlePlace.BattlePlace.load(self)
        self.music = base.loader.loadMusic('phase_14/audio/bgm/BD_office_bg.ogg')

    def unload(self):
        self.parentFSM.getStateNamed('boardofficeInterior').removeChild(self.fsm)
        del self.music
        del self.fsm
        del self.parentFSM
        BattlePlace.BattlePlace.unload(self)

    def enter(self, requestStatus):
        self.fsm.enterInitialState()
        base.transitions.fadeOut(t=0)
        base.localAvatar.inventory.setRespectInvasions(0)
        base.cr.forbidCheesyEffects(1)
        self._telemLimiter = TLGatherAllAvs('BoardOfficeInterior', RotationLimitToH)

        def commence(self = self):
            NametagGlobals.setWant2dNametags(True)
            self.fsm.request(requestStatus['how'], [requestStatus])
            base.playMusic(self.music, looping=1, volume=0.8)
            base.transitions.irisIn()
            mint = bboard.get(DistributedBoardOffice.DistributedBoardOffice.ReadyPost)
            self.loader.hood.spawnTitleText(mint.boardofficeId, mint.floorNum)

        self.mintReadyWatcher = BulletinBoardWatcher.BulletinBoardWatcher('BoardOfficeReady', DistributedBoardOffice.DistributedBoardOffice.ReadyPost, commence)
        self.mintDefeated = 0
        self.acceptOnce(DistributedBoardOffice.DistributedBoardOffice.WinEvent, self.handleBoardOfficeWinEvent)
        if __debug__ and 0:
            self.accept('f10', lambda : messenger.send(DistributedBoardOffice.DistributedBoardOffice.WinEvent))
        self.confrontedBoss = 0

        def handleConfrontedBoss(self = self):
            self.confrontedBoss = 1

        self.acceptOnce('localToonConfrontedBoardOfficeBoss', handleConfrontedBoss)

    def exit(self):
        NametagGlobals.setWant2dNametags(False)
        bboard.remove(DistributedBoardOffice.DistributedBoardOffice.ReadyPost)
        self._telemLimiter.destroy()
        del self._telemLimiter
        base.cr.forbidCheesyEffects(0)
        base.localAvatar.inventory.setRespectInvasions(1)
        self.fsm.requestFinalState()
        self.loader.music.stop()
        self.music.stop()
        self.ignoreAll()
        del self.mintReadyWatcher

    def enterWalk(self, teleportIn = 0):
        BattlePlace.BattlePlace.enterWalk(self, teleportIn)
        self.ignore('teleportQuery')
        base.localAvatar.setTeleportAvailable(0)

    def enterPush(self):
        BattlePlace.BattlePlace.enterPush(self)
        self.ignore('teleportQuery')
        base.localAvatar.setTeleportAvailable(0)

    def enterWaitForBattle(self):
        BoardOfficeInterior.notify.debug('enterWaitForBattle')
        BattlePlace.BattlePlace.enterWaitForBattle(self)
        if base.localAvatar.getParent() != render:
            base.localAvatar.wrtReparentTo(render)
            base.localAvatar.b_setParent(ToontownGlobals.SPRender)

    def exitWaitForBattle(self):
        BoardOfficeInterior.notify.debug('exitWaitForBattle')
        BattlePlace.BattlePlace.exitWaitForBattle(self)

    def enterBattle(self, event):
        BoardOfficeInterior.notify.debug('enterBattle')
        self.music.stop()
        BattlePlace.BattlePlace.enterBattle(self, event)
        self.ignore('teleportQuery')
        base.localAvatar.setTeleportAvailable(0)

    def enterTownBattle(self, event):
        mult = ToontownBattleGlobals.getBoardOfficeCreditMultiplier(self.zoneId)
        base.localAvatar.inventory.setBattleCreditMultiplier(mult)
        self.loader.townBattle.enter(event, self.fsm.getStateNamed('battle'), bldg=1, creditMultiplier=mult)

    def exitBattle(self):
        BoardOfficeInterior.notify.debug('exitBattle')
        BattlePlace.BattlePlace.exitBattle(self)
        self.loader.music.stop()
        base.playMusic(self.music, looping=1, volume=0.8)

    def enterStickerBook(self, page = None):
        BattlePlace.BattlePlace.enterStickerBook(self, page)
        self.ignore('teleportQuery')
        base.localAvatar.setTeleportAvailable(0)

    def enterSit(self):
        BattlePlace.BattlePlace.enterSit(self)
        self.ignore('teleportQuery')
        base.localAvatar.setTeleportAvailable(0)

    def enterZone(self, zoneId):
        pass

    def enterTeleportOut(self, requestStatus):
        BoardOfficeInterior.notify.debug('enterTeleportOut()')
        BattlePlace.BattlePlace.enterTeleportOut(self, requestStatus, self.__teleportOutDone)

    def __processLeaveRequest(self, requestStatus):
        hoodId = requestStatus['hoodId']
        if hoodId == ToontownGlobals.MyEstate:
            self.getEstateZoneAndGoHome(requestStatus)
        else:
            self.doneStatus = requestStatus
            messenger.send(self.doneEvent)

    def __teleportOutDone(self, requestStatus):
        BoardOfficeInterior.notify.debug('__teleportOutDone()')
        messenger.send('leavingBoardOffice')
        messenger.send('localToonLeft')
        if self.mintDefeated and not self.confrontedBoss:
            self.fsm.request('FLA', [requestStatus])
        else:
            self.__processLeaveRequest(requestStatus)

    def exitTeleportOut(self):
        BoardOfficeInterior.notify.debug('exitTeleportOut()')
        BattlePlace.BattlePlace.exitTeleportOut(self)

    def handleBoardOfficeWinEvent(self):
        BoardOfficeInterior.notify.debug('handleBoardOfficeWinEvent')
        if base.cr.playGame.getPlace().fsm.getCurrentState().getName() == 'died':
            return
        self.mintDefeated = 1
        zoneId = ZoneUtil.getHoodId(self.zoneId)
        self.fsm.request('teleportOut', [{'loader': ZoneUtil.getLoaderName(zoneId),
          'where': ZoneUtil.getToonWhereName(zoneId),
          'how': 'teleportIn',
          'hoodId': zoneId,
          'zoneId': zoneId,
          'shardId': None,
          'avId': -1}])

    def enterDied(self, requestStatus, callback = None):
        BoardOfficeInterior.notify.debug('enterDied')

        def diedDone(requestStatus, self = self, callback = callback):
            if callback is not None:
                callback()
            messenger.send('leavingBoardOffice')
            self.doneStatus = requestStatus
            messenger.send(self.doneEvent)

        BattlePlace.BattlePlace.enterDied(self, requestStatus, diedDone)

    def enterFLA(self, requestStatus):
        BoardOfficeInterior.notify.debug('enterFLA')
        self.flaDialog = TTDialog.TTGlobalDialog(message=TTLocalizer.ForcedLeaveBoardOfficeAckMsg, doneEvent='FLADone', style=TTDialog.Acknowledge, fadeScreen=1)

        def continueExit(self = self, requestStatus = requestStatus):
            self.__processLeaveRequest(requestStatus)

        self.accept('FLADone', continueExit)
        self.flaDialog.show()

    def exitFLA(self):
        BoardOfficeInterior.notify.debug('exitFLA')
        if hasattr(self, 'flaDialog'):
            self.flaDialog.cleanup()
            del self.flaDialog
