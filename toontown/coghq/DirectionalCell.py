#Embedded file name: toontown.coghq.DirectionalCell
from toontown.coghq import ActiveCell
from direct.directnotify import DirectNotifyGlobal

class DirectionalCell(ActiveCell.ActiveCell):
    notify = DirectNotifyGlobal.directNotify.newCategory('DirectionalCell')

    def __init__(self, cr):
        ActiveCell.ActiveCell.__init__(self, cr)
