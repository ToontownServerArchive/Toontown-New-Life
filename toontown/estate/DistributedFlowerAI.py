#Embedded file name: toontown.estate.DistributedFlowerAI
from direct.directnotify import DirectNotifyGlobal
import time
from FlowerBase import FlowerBase
from otp.ai.MagicWordGlobal import *
from toontown.estate.DistributedPlantBaseAI import DistributedPlantBaseAI
import GardenGlobals

class DistributedFlowerAI(DistributedPlantBaseAI, FlowerBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedFlowerAI')

    def setTypeIndex(self, value):
        DistributedPlantBaseAI.setTypeIndex(self, value)
        FlowerBase.setSpecies(self, value)

    def calculate(self, lastCheck):
        now = int(time.time())
        if lastCheck == 0:
            lastCheck = now
        grown = 0
        elapsed = now - lastCheck
        while elapsed > 86400:
            if self.waterLevel >= 0:
                grown += 1
            elapsed -= 86400
            self.waterLevel -= 1

        self.waterLevel = max(self.waterLevel, -2)
        maxGrowth = self.growthThresholds[2]
        newGL = min(self.growthLevel + grown, maxGrowth)
        self.setGrowthLevel(newGL)
        self.lastCheck = now - elapsed
        self.update()

    def update(self):
        mdata = map(list, self.mgr.data['flowers'])
        mdata[self.flowerIndex] = [self.getSpecies(),
         self.waterLevel,
         self.lastCheck,
         self.getGrowthLevel(),
         self.getVariety()]
        self.mgr.data['flowers'] = mdata
        self.mgr.update()

    def removeItem(self, usingGardenPickAll = 0):
        avId = self.air.getAvatarIdFromSender()
        if not usingGardenPickAll:
            if avId != self.ownerDoId:
                self.air.writeServerEvent('suspicious', avId, 'Attempted to remove someone elses flower!!!!')
                return
            self.d_setMovie(GardenGlobals.MOVIE_REMOVE)
        action = 'remove'
        if self.getGrowthLevel() >= self.growthThresholds[2]:
            action = 'pick'

        def _remove(task):
            if not self.air:
                return
            av = self.air.doId2do.get(self.ownerDoId)
            if not av:
                return
            plot = self.mgr.placePlot(self.flowerIndex)
            plot.flowerIndex = self.flowerIndex
            plot.setPlot(self.plot)
            plot.setOwnerIndex(self.ownerIndex)
            plot.generateWithRequired(self.zoneId)
            index = (0, 1, 2, 2, 2, 3, 3, 3, 4, 4)[self.flowerIndex]
            idx = (0, 0, 0, 1, 2, 0, 1, 2, 0, 1)[self.flowerIndex]
            plot.sendUpdate('setBoxDoId', [self.mgr._boxes[index].doId, idx])
            self.air.writeServerEvent('%s-flower' % action, avId, plot=self.plot)
            self.requestDelete()
            self.mgr.flowers.remove(self)
            mdata = map(list, self.mgr.data['flowers'])
            mdata[self.flowerIndex] = self.mgr.getNullPlant()
            self.mgr.data['flowers'] = mdata
            self.mgr.update()
            if action == 'pick':
                av.b_setShovelSkill(av.getShovelSkill() + self.getValue())
                av.addFlowerToBasket(self.getSpecies(), self.getVariety())
            if task:
                return task.done

        if usingGardenPickAll:
            _remove(None)
        else:
            taskMgr.doMethodLater(7, _remove, self.uniqueName('do-remove'))


@magicWord(category=CATEGORY_PROGRAMMER)
def gardenGrowFlowers():
    av = spellbook.getTarget()
    estate = av.air.estateManager._lookupEstate(av)
    if not estate:
        return 'Estate not found!'
    garden = estate.gardenManager.gardens.get(av.doId)
    if not garden:
        return 'Garden not found!'
    now = int(time.time())
    i = 0
    for flower in garden.flowers:
        flower.b_setWaterLevel(5)
        flower.b_setGrowthLevel(2)
        flower.update()
        i += 1

    return 'Grew %d Flowers' % i


@magicWord(category=CATEGORY_PROGRAMMER)
def gardenPickAll():
    av = spellbook.getTarget()
    estate = av.air.estateManager._lookupEstate(av)
    if not estate:
        return 'Estate not found!'
    garden = estate.gardenManager.gardens.get(av.doId)
    if not garden:
        return 'Garden not found!'
    i = 0
    for flower in garden.flowers.copy():
        if flower.getGrowthLevel() >= flower.growthThresholds[2]:
            flower.removeItem(1)
            i += 1

    return 'Picked %d Flowers' % i
