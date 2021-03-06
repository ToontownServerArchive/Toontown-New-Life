#Embedded file name: toontown.ai.QuestManagerAI
from toontown.toon.DistributedNPCSpecialQuestGiverAI import DistributedNPCSpecialQuestGiverAI
from toontown.building import FADoorCodes
from otp.ai.MagicWordGlobal import *
from toontown.hood import ZoneUtil
from toontown.toonbase import ToontownGlobals
from toontown.quest import Quests
QuestIdIndex = 0
QuestFromNpcIdIndex = 1
QuestToNpcIdIndex = 2
QuestRewardIdIndex = 3
QuestProgressIndex = 4

class QuestManagerAI():
    notify = directNotify.newCategory('QuestManagerAI')

    def __init__(self, air):
        self.air = air

    def __toonQuestsList2Quests(self, quests):
        return [ Quests.getQuest(x[0]) for x in quests ]

    def __incrementQuestProgress(self, quest):
        quest[4] += 1

    def requestInteract(self, avId, npc):
        av = self.air.doId2do.get(avId)
        if not av:
            return
        avQuestPocketSize = av.getQuestCarryLimit()
        avQuests = av.getQuests()
        fakeTier = 0
        avTrackProgress = av.getTrackProgress()
        for i in xrange(0, len(avQuests), 5):
            questDesc = avQuests[i:i + 5]
            questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc
            questClass = Quests.getQuest(questId)
            if questClass:
                completeStatus = questClass.getCompletionStatus(av, questDesc, npc)
            else:
                continue
            if isinstance(questClass, Quests.DeliverGagQuest):
                if npc.npcId == toNpcId:
                    track, level = questClass.getGagType()
                    currItems = av.inventory.numItem(track, level)
                    if currItems >= questClass.getNumGags():
                        av.inventory.setItem(track, level, av.inventory.numItem(track, level) - questClass.getNumGags())
                    else:
                        npc.rejectAvatar(avId)
                    av.b_setInventory(av.inventory.makeNetString())
            if completeStatus == Quests.COMPLETE:
                av.toonUp(av.maxHp)
                if isinstance(questClass, Quests.TrackChoiceQuest):
                    npc.presentTrackChoice(avId, questId, [0,
                     1,
                     2,
                     3,
                     4,
                     5,
                     6,
                     7])
                    break
                if Quests.getNextQuest(questId, npc, av)[0] != Quests.NA:
                    self.nextQuest(av, npc, questId)
                    if avId in self.air.tutorialManager.avId2fsm:
                        self.air.tutorialManager.avId2fsm[avId].demand('Tunnel')
                    break
                else:
                    npc.completeQuest(avId, questId, rewardId)
                    self.completeQuest(av, questId)
                break
        else:
            if len(avQuests) == avQuestPocketSize * 5:
                npc.rejectAvatar(avId)
                return
            if isinstance(npc, DistributedNPCSpecialQuestGiverAI):
                self.tutorialQuestChoice(avId, npc)
                return
            choices = self.avatarQuestChoice(av, npc)
            if choices != []:
                for choice in choices:
                    questClass = Quests.QuestDict.get(choice[0])
                    for required in questClass[0]:
                        if required not in av.getQuestHistory():
                            choices.remove(choice)
                        else:
                            continue

                npc.presentQuestChoice(avId, choices)
            else:
                npc.rejectAvatar(avId)

    def npcGiveTrackChoice(self, av, tier):
        trackQuest = Quests.chooseTrackChoiceQuest(tier, av)
        return [(trackQuest, 400, Quests.ToonHQ)]

    def avatarQuestChoice(self, av, npc):
        # Get the best quests for an avatar/npc.
        return Quests.chooseBestQuests(av.getRewardTier(), npc, av)

    def avatarChoseQuest(self, avId, npc, questId, rewardId, toNpcId):
        av = self.air.doId2do.get(avId)
        if not av:
            return
        if len(av.quests) > av.getQuestCarryLimit():
            return
        fromNpcId = npc.npcId
        if toNpcId == 0:
            toNpcId = Quests.getQuestToNpcId(questId)
        transformedRewardId = Quests.transformReward(rewardId, av)
        av.addQuest([questId,
         fromNpcId,
         toNpcId,
         rewardId,
         0], transformedRewardId)
        taskMgr.remove(npc.uniqueName('clearMovie'))
        npc.assignQuest(avId, questId, rewardId, toNpcId)

    def avatarChoseTrack(self, avId, npc, pendingTrackQuest, trackId):
        av = self.air.doId2do.get(avId)
        if not av:
            return
        taskMgr.remove(npc.uniqueName('clearMovie'))
        npc.completeQuest(avId, pendingTrackQuest, Quests.getRewardIdFromTrackId(trackId))
        self.completeQuest(av, pendingTrackQuest)
        av.b_setTrackProgress(trackId, 0)

    def avatarCancelled(self, npcId):
        npc = self.air.doId2do.get(npcId)
        if not npc:
            return
        taskMgr.remove(npc.uniqueName('clearMovie'))

    def nextQuest(self, av, npc, questId):
        nextQuestId, toNpcId = Quests.getNextQuest(questId, npc, av)
        avQuests = av.getQuests()
        questList = []
        for i in xrange(0, len(avQuests), 5):
            questDesc = avQuests[i:i + 5]
            if questDesc[QuestIdIndex] == questId:
                questDesc[QuestIdIndex] = nextQuestId
                questDesc[QuestToNpcIdIndex] = toNpcId
                questDesc[QuestProgressIndex] = 0
            questList.append(questDesc)

        npc.incompleteQuest(av.doId, nextQuestId, Quests.QUEST, toNpcId)
        av.b_setQuests(questList)

    def completeQuest(self, av, completeQuestId):
        avQuests = av.getQuests()
        for i in xrange(0, len(avQuests), 5):
            questDesc = avQuests[i:i + 5]
            questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc
            questClass = Quests.getQuest(questId)
            questMoney = Quests.getQuestMoney(questId)
            if questId == completeQuestId:
                av.removeQuest(questId)
                self.giveReward(av, questId, rewardId)
                if questMoney != 0:
                    av.addMoney(questMoney)
                av.addStat(ToontownGlobals.STATS_TASKS)
                av.addToQuestHistory(questId)
                break

    def giveReward(self, av, questId, rewardId):
        rewardClass = Quests.getReward(rewardId)
        if rewardClass is None:
            self.notify.warning('rewardClass was None for rewardId: %s.' % rewardId)
        else:
            rewardClass.sendRewardAI(av)

    def tutorialQuestChoice(self, avId, npc):
        av = self.air.doId2do.get(avId)
        if not av:
            return
        choices = self.avatarQuestChoice(av, npc)
        if len(choices) == 0:
            npc.rejectAvatar(avId)
            return
        quest = choices[0]
        self.avatarChoseQuest(avId, npc, quest[0], quest[1], 0)
        if avId in self.air.tutorialManager.avId2fsm:
            self.air.tutorialManager.avId2fsm[avId].demand('Battle')

    def toonRodeTrolleyFirstTime(self, av):
        self.toonPlayedMinigame(av, [])

    def toonPlayedMinigame(self, av, toons):
        avQuests = av.getQuests()
        questList = []
        for i in xrange(0, len(avQuests), 5):
            questDesc = avQuests[i:i + 5]
            questClass = Quests.getQuest(questDesc[QuestIdIndex])
            if isinstance(questClass, Quests.TrolleyQuest):
                questDesc[QuestProgressIndex] = 1
            questList.append(questDesc)

        av.b_setQuests(questList)

    def toonMadeFriend(self, avId):
        av = self.air.doId2do.get(avId)
        if not av:
            return
        avQuests = av.getQuests()
        questList = []
        for i in xrange(0, len(avQuests), 5):
            questDesc = avQuests[i:i + 5]
            questClass = Quests.getQuest(questDesc[QuestIdIndex])
            if isinstance(questClass, Quests.FriendQuest):
                questDesc[QuestProgressIndex] = 1
            questList.append(questDesc)

        av.b_setQuests(questList)

    def toonUsedPhone(self, avId):
        av = self.air.doId2do.get(avId)
        if not av:
            return
        avQuests = av.getQuests()
        questList = []
        for i in xrange(0, len(avQuests), 5):
            questDesc = avQuests[i:i + 5]
            questClass = Quests.getQuest(questDesc[QuestIdIndex])
            if isinstance(questClass, Quests.PhoneQuest):
                questDesc[QuestProgressIndex] += 1
            questList.append(questDesc)

        av.b_setQuests(questList)

    def toonCaughtFishingItem(self, av):
        avQuests = av.getQuests()
        fishingItem = -1
        questList = []
        for i in xrange(0, len(avQuests), 5):
            questDesc = avQuests[i:i + 5]
            questClass = Quests.getQuest(questDesc[QuestIdIndex])
            if fishingItem != -1:
                questList.append(questDesc)
                continue
            if isinstance(questClass, Quests.RecoverItemQuest):
                if not hasattr(questClass, 'getItem'):
                    questList.append(questDesc)
                    continue
                if questClass.getHolder() == Quests.AnyFish:
                    if not questClass.getCompletionStatus(av, questDesc) == Quests.COMPLETE:
                        baseChance = questClass.getPercentChance()
                        amountRemaining = questClass.getNumItems() - questDesc[QuestProgressIndex]
                        chance = Quests.calcRecoverChance(amountRemaining, baseChance)
                        if chance >= baseChance:
                            questDesc[QuestProgressIndex] += 1
                            fishingItem = questClass.getItem()
            questList.append(questDesc)

        av.b_setQuests(questList)
        return fishingItem

    def hasTailorClothingTicket(self, av, npc):
        avQuests = av.getQuests()
        for i in xrange(0, len(avQuests), 5):
            questDesc = avQuests[i:i + 5]
            questClass = Quests.getQuest(questDesc[QuestIdIndex])
            if isinstance(questClass, Quests.DeliverItemQuest):
                if questClass.getCompletionStatus(av, questDesc, npc) == Quests.COMPLETE:
                    return 1

        return 0

    def removeClothingTicket(self, av, npc):
        avQuests = av.getQuests()
        for i in xrange(0, len(avQuests), 5):
            questDesc = avQuests[i:i + 5]
            questClass = Quests.getQuest(questDesc[QuestIdIndex])
            if isinstance(questClass, Quests.DeliverItemQuest):
                if questClass.getCompletionStatus(av, questDesc, npc) == Quests.COMPLETE:
                    av.removeQuest(questDesc[QuestIdIndex])
                    break

    def recoverItems(self, toon, suitsKilled, zoneId):
        recovered, notRecovered = ([] for i in xrange(2))
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            if isinstance(quest, Quests.RecoverItemQuest):
                isComplete = quest.getCompletionStatus(toon, toon.quests[index])
                if isComplete == Quests.COMPLETE:
                    continue
                if quest.isLocationMatch(zoneId):
                    if quest.getHolder() == Quests.Any or quest.getHolderType() in ('type', 'track', 'level'):
                        for suit in suitsKilled:
                            if quest.getCompletionStatus(toon, toon.quests[index]) == Quests.COMPLETE:
                                break
                            if quest.getHolder() == Quests.Any or quest.getHolderType() == 'type' and quest.getHolder() == suit['type'] or quest.getHolderType() == 'track' and quest.getHolder() == suit['track'] or quest.getHolderType() == 'level' and quest.getHolder() <= suit['level']:
                                progress = toon.quests[index][4] & pow(2, 16) - 1
                                completion = quest.testRecover(progress)
                                if completion[0]:
                                    recovered.append(quest.getItem())
                                    self.__incrementQuestProgress(toon.quests[index])
                                else:
                                    notRecovered.append(quest.getItem())

        toon.d_setQuests(toon.getQuests())
        return (recovered, notRecovered)

    def toonKilledBuilding(self, av, type, difficulty, floors, zoneId, activeToons):
        avQuests = av.getQuests()
        questList = []
        zoneId = ZoneUtil.getBranchZone(zoneId)
        for i in xrange(0, len(avQuests), 5):
            questDesc = avQuests[i:i + 5]
            questClass = Quests.getQuest(questDesc[QuestIdIndex])
            if questClass.getCompletionStatus(av, questDesc) == Quests.INCOMPLETE:
                if isinstance(questClass, Quests.BuildingQuest):
                    if questClass.isLocationMatch(zoneId):
                        if questClass.doesBuildingTypeCount(type):
                            if questClass.doesBuildingCount(av, activeToons):
                                if floors >= questClass.getNumFloors():
                                    questDesc[QuestProgressIndex] += 1
            questList.append(questDesc)

        av.b_setQuests(questList)

    def toonKilledCogdo(self, av, type, difficulty, zoneId, activeToons):
        self.notify.debug("toonKilledCogdo(%s, '%s', %s, %d, %s)" % (str(av),
         type,
         str(difficulty),
         zoneId,
         str(activeToons)))
        avQuests = av.getQuests()
        questList = []
        zoneId = ZoneUtil.getBranchZone(zoneId)
        for i in xrange(0, len(avQuests), 5):
            questDesc = avQuests[i:i + 5]
            questClass = Quests.getQuest(questDesc[QuestIdIndex])
            if questClass.getCompletionStatus(av, questDesc) == Quests.INCOMPLETE:
                if isinstance(questClass, Quests.CogdoQuest):
                    if questClass.isLocationMatch(zoneId):
                        if questClass.doesCogdoTypeCount(type):
                            if questClass.doesCogdoCount(av, activeToons):
                                questDesc[QuestProgressIndex] += 1
            questList.append(questDesc)

        av.b_setQuests(questList)

    def toonCollectedExp(self, av, expArray):
        avQuests = av.getQuests()
        questList = []
        for i in xrange(0, len(avQuests), 5):
            questDesc = avQuests[i:i + 5]
            questClass = Quests.getQuest(questDesc[QuestIdIndex])
            if isinstance(questClass, Quests.TrackExpQuest):
                if questClass.doesExpCount(av, expArray):
                    questDesc[QuestProgressIndex] += expArray[questClass.getTrackType()]
            questList.append(questDesc)

        av.b_setQuests(questList)

    def toonDefeatedFactory(self, av, factoryId, activeVictors):
        avQuests = av.getQuests()
        questList = []
        for i in xrange(0, len(avQuests), 5):
            questDesc = avQuests[i:i + 5]
            questClass = Quests.getQuest(questDesc[QuestIdIndex])
            if isinstance(questClass, Quests.FactoryQuest):
                if questClass.doesFactoryCount(av, factoryId, activeVictors):
                    questDesc[QuestProgressIndex] += 1
            questList.append(questDesc)

        av.b_setQuests(questList)

    def toonDefeatedMint(self, av, mintId, activeVictors):
        avQuests = av.getQuests()
        questList = []
        for i in xrange(0, len(avQuests), 5):
            questDesc = avQuests[i:i + 5]
            questClass = Quests.getQuest(questDesc[QuestIdIndex])
            if isinstance(questClass, Quests.MintQuest):
                if questClass.doesMintCount(av, mintId, activeVictors):
                    questDesc[QuestProgressIndex] += 1
            questList.append(questDesc)

        av.b_setQuests(questList)

    def toonDefeatedStage(self, av, stageId, activeVictors):
        avQuests = av.getQuests()
        questList = []
        for i in xrange(0, len(avQuests), 5):
            questDesc = avQuests[i:i + 5]
            questClass = Quests.getQuest(questDesc[QuestIdIndex])
            if isinstance(questClass, Quests.StageQuest):
                if questClass.doesStageCount(av, stageId, activeVictors):
                    questDesc[QuestProgressIndex] += 1
            questList.append(questDesc)

        av.b_setQuests(questList)

    def toonDefeatedCountryClub(self, av, clubId, activeVictors):
        avQuests = av.getQuests()
        questList = []
        for i in xrange(0, len(avQuests), 5):
            questDesc = avQuests[i:i + 5]
            questClass = Quests.getQuest(questDesc[QuestIdIndex])
            if isinstance(questClass, Quests.ClubQuest):
                if questClass.doesClubCount(av, clubId, activeVictors):
                    questDesc[QuestProgressIndex] += 1
            questList.append(questDesc)

        av.b_setQuests(questList)

    def toonDefeatedBoardOffice(self, av, clubId, activeVictors):
        pass

    def toonKilledCogs(self, av, suitsKilled, zoneId, activeToonList):
        avQuests = av.getQuests()
        questList = []
        activeToonDoIds = [ toon.doId for toon in activeToonList if not None ]
        for i in xrange(0, len(avQuests), 5):
            questDesc = avQuests[i:i + 5]
            questClass = Quests.getQuest(questDesc[QuestIdIndex])
            if isinstance(questClass, Quests.CogQuest):
                for suit in suitsKilled:
                    if questClass.doesCogCount(av.doId, suit, zoneId, activeToonList):
                        if questClass.getCompletionStatus(av, questDesc) != Quests.COMPLETE:
                            questDesc[QuestProgressIndex] += 1

            questList.append(questDesc)

        av.b_setQuests(questList)


@magicWord(category=CATEGORY_PROGRAMMER, types=[str, int, int])
def quests(command, arg0 = 0, arg1 = 0):
    invoker = spellbook.getTarget()
    currQuests = invoker.getQuests()
    currentQuestIds = []
    for i in xrange(0, len(currQuests), 5):
        currentQuestIds.append(currQuests[i])

    pocketSize = invoker.getQuestCarryLimit()
    carrying = len(currQuests) / 5
    canCarry = False
    if carrying < pocketSize:
        canCarry = True
    if command == 'clear':
        invoker.b_setQuests([])
        return 'Cleared quests'
    if command == 'clearHistory':
        invoker.d_setQuestHistory([])
        return 'Cleared quests history'
    if command == 'add':
        if arg0:
            if canCarry:
                if arg0 in Quests.QuestDict.keys():
                    return 'Added QuestID %s' % arg0
                else:
                    return 'Invalid QuestID %s' % arg0
            else:
                return 'Cannot take anymore quests'
        else:
            return 'add needs 1 argument.'
    elif command == 'remove':
        if arg0:
            if arg0 in currentQuestIds:
                invoker.removeQuest(arg0)
                return 'Removed QuestID %s' % arg0
            if arg0 < pocketSize and arg0 > 0:
                if len(currentQuestIds) <= arg0:
                    questIdToRemove = currentQuestIds[arg0 - 1]
                    invoker.removeQuest(questIdToRemove)
                    return 'Removed quest from slot %s' % arg0
                else:
                    return 'Invalid quest slot'
            else:
                return 'Cannot remove quest %s' % arg0
        else:
            return 'remove needs 1 argument.'
    elif command == 'list':
        if arg0:
            if arg0 > 0 and arg0 <= pocketSize:
                start = (arg0 - 1) * 5
                questDesc = currQuests[start:start + 5]
                return 'QuestDesc in slot %s: %s.' % (arg0, questDesc)
            else:
                return 'Invalid quest slot %s.' % arg0
        else:
            return 'CurrentQuests: %s' % currentQuestIds
    elif command == 'bagSize':
        if arg0 > 0 and arg0 < 5:
            invoker.b_setQuestCarryLimit(arg0)
            return 'Set carry limit to %s' % arg0
        else:
            return 'Argument 0 must be between 1 and 4.'
    elif command == 'progress':
        if arg0 and arg1:
            if arg0 > 0 and arg0 <= pocketSize:
                questList = []
                wantedQuestId = currentQuestIds[arg0 - 1]
                for i in xrange(0, len(currQuests), 5):
                    questDesc = currQuests[i:i + 5]
                    if questDesc[0] == wantedQuestId:
                        questDesc[4] = arg1
                    questList.append(questDesc)

                invoker.b_setQuests(questList)
                return 'Set quest slot %s progress to %s' % (arg0, arg1)
            if arg0 in Quests.QuestDict.keys():
                if arg0 in currentQuestIds:
                    questList = []
                    for i in xrange(0, len(currQuests), 5):
                        questDesc = currQuests[i:i + 5]
                        if questDesc[0] == arg0:
                            questDesc[4] = arg1
                        questList.append(questDesc)

                    invoker.b_setQuests(questList)
                    return 'Set QuestID %s progress to %s' % (arg0, arg1)
                else:
                    return 'Cannot progress QuestID: %s.' % arg0
            else:
                return 'Invalid quest or slot id'
        else:
            return 'progress needs 2 arguments.'
    else:
        if command == 'getHistory':
            return invoker.getQuestHistory()
        if command == 'getQuests':
            return invoker.getQuests()
        return 'Invalid first argument.'
