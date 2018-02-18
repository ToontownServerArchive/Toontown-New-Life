#Embedded file name: toontown.coghq.DistributedCashbotBossTreasure
from toontown.safezone import DistributedTreasure
from toontown.toonbase import ToontownGlobals
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import Point3
Models = {ToontownGlobals.ToontownCentral: 'phase_4/models/props/icecream',
 ToontownGlobals.DonaldsDock: 'phase_6/models/props/starfish_treasure',
 ToontownGlobals.TheBrrrgh: 'phase_8/models/props/snowflake_treasure',
 ToontownGlobals.MinniesMelodyland: 'phase_6/models/props/music_treasure',
 ToontownGlobals.DaisyGardens: 'phase_8/models/props/flower_treasure',
 ToontownGlobals.DonaldsDreamland: 'phase_8/models/props/zzz_treasure'}

class DistributedCashbotBossTreasure(DistributedTreasure.DistributedTreasure):

    def __init__(self, cr):
        DistributedTreasure.DistributedTreasure.__init__(self, cr)
        self.grabSoundPath = 'phase_4/audio/sfx/SZ_DD_treasure.mp3'

    def setStyle(self, hoodId):
        newModel = Models[hoodId]
        self.modelPath = newModel
        if self.modelPath != newModel:
            if self.modelPath:
                self.loadModel(newModel)

    def setGoonId(self, goonId):
        self.goonId = goonId

    def setFinalPosition(self, x, y, z):
        if not self.nodePath:
            self.makeNodePath()
        if self.treasureFlyTrack:
            self.treasureFlyTrack.finish()
            self.treasureFlyTrack = None
        startPos = None
        goon = self.cr.doId2do[self.goonId]
        if goon:
            startPos = goon.getPos()
        lerpTime = 1
        self.treasureFlyTrack = Sequence(Func(self.collNodePath.stash), Parallel(ProjectileInterval(self.treasure, startPos=Point3(0, 0, 0), endPos=Point3(0, 0, 0), duration=lerpTime, gravityMult=2.0), LerpPosInterval(self.nodePath, lerpTime, Point3(x, y, z), startPos=startPos)), Func(self.collNodePath.unstash))
        self.treasureFlyTrack.start()