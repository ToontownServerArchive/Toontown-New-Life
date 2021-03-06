#Embedded file name: toontown.classicchars.DistributedSockHopDaisy
from direct.showbase.ShowBaseGlobal import *
from toontown.classicchars import DistributedCCharBase
from toontown.classicchars import DistributedDaisy
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM
from direct.fsm import State
from toontown.classicchars import CharStateDatas
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.hood import TTHood

class DistributedSockHopDaisy(DistributedDaisy.DistributedDaisy):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSockHopDaisy')

    def __init__(self, cr):
        try:
            self.DistributedSockHopDaisy_initialized
            return
        except:
            self.DistributedSockHopDaisy_initialized = 1

        DistributedCCharBase.DistributedCCharBase.__init__(self, cr, TTLocalizer.SockHopDaisy, 'shdd')
        self.fsm = ClassicFSM.ClassicFSM(self.getName(), [State.State('Off', self.enterOff, self.exitOff, ['Neutral']), State.State('Neutral', self.enterNeutral, self.exitNeutral, ['Walk']), State.State('Walk', self.enterWalk, self.exitWalk, ['Neutral'])], 'Off', 'Off')
        self.fsm.enterInitialState()
        self.nametag.setText(TTLocalizer.Daisy)
        self.handleHolidays()
