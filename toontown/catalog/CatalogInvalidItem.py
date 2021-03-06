#Embedded file name: toontown.catalog.CatalogInvalidItem
from toontown.catalog import CatalogItem
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToonPythonUtil as PythonUtil
from toontown.toonbase import ToontownGlobals

class CatalogInvalidItem(CatalogItem.CatalogItem):

    def requestPurchase(self, phone, callback):
        self.notify.error('Attempt to purchase invalid item.')

    def acceptItem(self, mailbox, index, callback):
        self.notify.error('Attempt to accept invalid item.')

    def output(self, store = -1):
        return 'CatalogInvalidItem()'
