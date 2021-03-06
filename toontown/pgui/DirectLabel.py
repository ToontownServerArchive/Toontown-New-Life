#Embedded file name: toontown.pgui.DirectLabel
__all__ = ['DirectLabel']
from pandac.PandaModules import *
import DirectGuiGlobals as DGG
from DirectFrame import *

class DirectLabel(DirectFrame):

    def __init__(self, parent = None, **kw):
        optiondefs = (('pgFunc', PGItem, None),
         ('numStates', 1, None),
         ('state', self.inactiveInitState, None),
         ('activeState', 0, self.setActiveState))
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent)
        self.initialiseoptions(DirectLabel)

    def setActiveState(self):
        self.guiItem.setState(self['activeState'])
