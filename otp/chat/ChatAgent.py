#Embedded file name: otp.chat.ChatAgent
from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from panda3d.core import *
from panda3d.direct import *
from otp.otpbase import OTPGlobals
from otp.ai.MagicWordGlobal import *

class ChatAgent(DistributedObjectGlobal):

    def __init__(self, cr):
        DistributedObjectGlobal.__init__(self, cr)
        self.chatMode = 0

    def delete(self):
        self.ignoreAll()
        self.cr.chatManager = None
        DistributedObjectGlobal.delete(self)

    def adminChat(self, aboutId, message):
        self.notify.warning('Admin Chat(%s): %s' % (aboutId, message))
        messenger.send('adminChat', [aboutId, message])

    def sendChatMessage(self, message):
        self.sendUpdate('chatMessage', [message, self.chatMode])

    def kickForSpam(self, av):
        self.sendUpdate('kickForSpam', [av.doId])


@magicWord(category=CATEGORY_MODERATOR, types=[int])
def chatmode(mode = -1):
    mode2name = {0: 'user',
     1: 'moderator',
     2: 'administrator',
     3: 'system administrator'}
    if base.cr.chatAgent is None:
        return 'No ChatAgent found.'
    if mode == -1:
        return 'You are currently talking in the %s chat mode.' % mode2name.get(base.cr.chatAgent.chatMode, 'N/A')
    if not 0 <= mode <= 3:
        return 'Invalid chat mode specified.'
    if mode == 3 and spellbook.getInvoker().getAdminAccess() < 500:
        return 'Chat mode 3 is reserved for system administrators.'
    if mode == 2 and spellbook.getInvoker().getAdminAccess() < 400:
        return 'Chat mode 2 is reserved for administrators.'
    if mode == 1 and spellbook.getInvoker().getAdminAccess() < 200:
        return 'Chat mode 1 is reserved for moderators.'
    base.cr.chatAgent.chatMode = mode
    return 'You are now talking in the %s chat mode.' % mode2name.get(mode, 'N/A')
