#Embedded file name: toontown.ai.WelcomeValleyManager
from pandac.PandaModules import *
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import ToonPythonUtil as PythonUtil

class WelcomeValleyManager(DistributedObject.DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('WelcomeValleyManager')
    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

    def generate(self):
        if base.cr.welcomeValleyManager != None:
            base.cr.welcomeValleyManager.delete()
        base.cr.welcomeValleyManager = self
        DistributedObject.DistributedObject.generate(self)

    def disable(self):
        self.ignore(ToontownGlobals.SynchronizeHotkey)
        base.cr.welcomeValleyManager = None
        DistributedObject.DistributedObject.disable(self)

    def delete(self):
        self.ignore(ToontownGlobals.SynchronizeHotkey)
        base.cr.welcomeValleyManager = None
        DistributedObject.DistributedObject.delete(self)

    def requestZoneId(self, origZoneId, callback):
        context = self.getCallbackContext(callback)
        self.sendUpdate('requestZoneIdMessage', [origZoneId, context])

    def requestZoneIdResponse(self, zoneId, context):
        self.doCallbackContext(context, [zoneId])
