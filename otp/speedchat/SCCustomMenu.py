#Embedded file name: otp.speedchat.SCCustomMenu
from otp.speedchat.SCCustomTerminal import SCCustomTerminal
from otp.speedchat.SCMenu import SCMenu
from otp.otpbase.OTPLocalizer import CustomSCStrings

class SCCustomMenu(SCMenu):

    def __init__(self):
        SCMenu.__init__(self)
        self.accept('customMessagesChanged', self.__customMessagesChanged)
        self.__customMessagesChanged()

    def __customMessagesChanged(self):
        self.clearMenu()
        try:
            lt = base.localAvatar
        except:
            return

        for msgIndex in lt.customMessages:
            if msgIndex in CustomSCStrings:
                self.append(SCCustomTerminal(msgIndex))
