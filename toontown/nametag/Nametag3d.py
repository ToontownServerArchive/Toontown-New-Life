#Embedded file name: toontown.nametag.Nametag3d
import math
from direct.task.Task import Task
from panda3d.core import BillboardEffect, Vec3, Point3, PGButton, VBase4
from panda3d.core import DepthWriteAttrib
from toontown.chat.ChatBalloon import ChatBalloon
from toontown.nametag import NametagGlobals
from toontown.nametag.Nametag import Nametag
from toontown.toontowngui.Clickable3d import Clickable3d
from direct.interval.IntervalGlobal import Sequence

class Nametag3d(Nametag, Clickable3d):
    SCALING_MIN_DISTANCE = 1
    SCALING_MAX_DISTANCE = 200
    SCALING_FACTOR = 0.065

    def __init__(self):
        Nametag.__init__(self)
        Clickable3d.__init__(self, 'Nametag3d', self)
        self.distance = 0
        self.billboardOffset = 3
        self.doBillboardEffect()

    def destroy(self):
        self.ignoreAll()
        Nametag.destroy(self)
        Clickable3d.destroy(self)

    def getUniqueName(self):
        return 'Nametag3d-%s' % id(self)

    def getChatBalloonModel(self):
        return NametagGlobals.chatBalloon3dModel

    def getChatBalloonWidth(self):
        return NametagGlobals.chatBalloon3dWidth

    def getChatBalloonHeight(self):
        return NametagGlobals.chatBalloon3dHeight

    def setBillboardOffset(self, billboardOffset):
        self.billboardOffset = billboardOffset
        self.doBillboardEffect()

    def getBillboardOffset(self):
        return self.billboardOffset

    def setAvatar(self, avatar):
        Nametag.setAvatar(self, avatar)
        Clickable3d.setAvatar(self, avatar)

    def doBillboardEffect(self):
        billboardEffect = BillboardEffect.make(Vec3(0, 0, 1), True, False, self.billboardOffset, base.cam, Point3(0, 0, 0))
        self.contents.setEffect(billboardEffect)

    def updateClickRegion(self):
        if self.chatBalloon is not None:
            left = self.chatBalloon.center[0] - self.chatBalloon.width / 2
            right = left + self.chatBalloon.width
            bottom = NametagGlobals.chatBalloon3dHeight - 2.4
            top = bottom + self.chatBalloon.height
            self.setClickRegionFrame(left, right, bottom, top)
        elif self.panel is not None:
            centerX = (self.textNode.getLeft() + self.textNode.getRight()) / 2.0
            centerY = (self.textNode.getBottom() + self.textNode.getTop()) / 2.0
            left = centerX - self.panelWidth / 2.0
            right = centerX + self.panelWidth / 2.0
            bottom = centerY - self.panelHeight / 2.0
            top = centerY + self.panelHeight / 2.0
            self.setClickRegionFrame(left, right, bottom, top)

    def isClickable(self):
        if self.getChatText() and self.hasChatButton():
            return True
        return NametagGlobals.wantActiveNametags and Clickable3d.isClickable(self)

    def setClickState(self, clickState):
        if self.isClickable():
            self.applyClickState(clickState)
        else:
            self.applyClickState(PGButton.SInactive)
        Clickable3d.setClickState(self, clickState)

    def enterDepressed(self):
        if self.isClickable():
            base.playSfx(NametagGlobals.clickSound)

    def enterRollover(self):
        if self.isClickable() and self.lastClickState != PGButton.SDepressed:
            base.playSfx(NametagGlobals.rolloverSound)

    def update(self):
        self.contents.node().removeAllChildren()
        Nametag.update(self)

    def tick(self, task):
        distance = self.contents.getPos(base.cam).length()
        if distance < self.SCALING_MIN_DISTANCE:
            distance = self.SCALING_MIN_DISTANCE
        elif distance > self.SCALING_MAX_DISTANCE:
            distance = self.SCALING_MAX_DISTANCE
        if distance != self.distance:
            self.contents.setScale(math.sqrt(distance) * self.SCALING_FACTOR)
            self.distance = distance
        self.updateClickRegion()
        return Task.cont

    def drawChatBalloon(self, model, modelWidth, modelHeight):
        if self.chatFont is None:
            return
        if self.isClickable():
            foreground, background = self.chatColor[self.clickState]
        else:
            foreground, background = self.chatColor[PGButton.SInactive]
        if self.chatType == NametagGlobals.SPEEDCHAT:
            background = self.speedChatColor
        if background[3] > self.CHAT_BALLOON_ALPHA:
            background = VBase4(background[0], background[1], background[2], self.CHAT_BALLOON_ALPHA)
        self.chatBalloon = ChatBalloon(model, modelWidth, modelHeight, self.chatTextNode, foreground=foreground, background=background, reversed=self.chatReversed, button=self.chatButton[self.clickState])
        self.chatBalloon.reparentTo(self.contents)
        self.chatBalloon.setScale(0, 0, 0)
        Sequence(self.chatBalloon.scaleInterval(0.2, VBase3(1.1, 1.1, 1.1), blendType='easeInOut'), self.chatBalloon.scaleInterval(0.09, VBase3(1, 1, 1), blendType='easeInOut')).start()

    def drawNametag(self):
        if self.font is None:
            return
        if self.icon is not None:
            self.contents.attachNewNode(self.icon)
        if self.isClickable():
            foreground, background = self.nametagColor[self.clickState]
        else:
            foreground, background = self.nametagColor[PGButton.SInactive]
        self.textNode.setTextColor(foreground)
        textNodePath = self.contents.attachNewNode(self.textNode, 1)
        textNodePath.setTransparency(foreground[3] < 1)
        textNodePath.setAttrib(DepthWriteAttrib.make(0))
        textNodePath.setY(-0.1)
        self.panel = NametagGlobals.cardModel.copyTo(self.contents, 0)
        self.panel.setColor(background)
        self.panel.setTransparency(background[3] < 1)
        x = (self.textNode.getLeft() + self.textNode.getRight()) / 2.0
        z = (self.textNode.getBottom() + self.textNode.getTop()) / 2.0
        self.panel.setPos(x, 0, z)
        self.panelWidth = self.textNode.getWidth() + self.PANEL_X_PADDING
        self.panelHeight = self.textNode.getHeight() + self.PANEL_Z_PADDING
        self.panel.setScale(self.panelWidth, 1, self.panelHeight)
