#Embedded file name: otp.distributed.DistributedDirectoryAI
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedDirectoryAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedDirectoryAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
