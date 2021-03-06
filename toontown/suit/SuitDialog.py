#Embedded file name: toontown.suit.SuitDialog
import random
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPLocalizer
notify = DirectNotifyGlobal.directNotify.newCategory('SuitDialog')

def getBrushOffIndex(suitName):
    if suitName in SuitBrushOffs:
        brushoffs = SuitBrushOffs[suitName]
    else:
        brushoffs = SuitBrushOffs[None]
    return random.randrange(len(brushoffs))


def getBrushOffText(suitName, index):
    if suitName in SuitBrushOffs:
        brushoffs = SuitBrushOffs[suitName]
    else:
        brushoffs = SuitBrushOffs[None]
    return brushoffs[index]


SuitBrushOffs = OTPLocalizer.SuitBrushOffs
