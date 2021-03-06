#Embedded file name: toontown.hood.DDHood
from pandac.PandaModules import Vec4
from toontown.safezone.DDSafeZoneLoader import DDSafeZoneLoader
from toontown.town.DDTownLoader import DDTownLoader
from toontown.toonbase import ToontownGlobals
from toontown.hood.ToonHood import ToonHood

class DDHood(ToonHood):
    notify = directNotify.newCategory('DDHood')
    ID = ToontownGlobals.DonaldsDock
    TOWNLOADER_CLASS = DDTownLoader
    SAFEZONELOADER_CLASS = DDSafeZoneLoader
    STORAGE_DNA = 'phase_6/dna/storage_DD.pdna'
    SKY_FILE = 'phase_3.5/models/props/BR_sky'
    SPOOKY_SKY_FILE = 'phase_3.5/models/props/BR_sky'
    TITLE_COLOR = (0.8, 0.6, 0.5, 1.0)
    HOLIDAY_DNA = {ToontownGlobals.WINTER_DECORATIONS: ['phase_6/dna/winter_storage_DD.pdna'],
     ToontownGlobals.WACKY_WINTER_DECORATIONS: ['phase_6/dna/winter_storage_DD.pdna'],
     ToontownGlobals.HALLOWEEN_PROPS: ['phase_6/dna/halloween_props_storage_DD.pdna'],
     ToontownGlobals.SPOOKY_PROPS: ['phase_6/dna/halloween_props_storage_DD.pdna']}

    def __init__(self, parentFSM, doneEvent, dnaStore, hoodId):
        ToonHood.__init__(self, parentFSM, doneEvent, dnaStore, hoodId)
        self.underwaterColor = Vec4(0, 0, 0.6, 1)

    def load(self):
        ToonHood.load(self)
        self.fog = Fog('DDFog')
        base.setBackgroundColor(Vec4(0.4, 0.588, 1, 1))

    def unload(self):
        ToonHood.unload(self)
        base.setBackgroundColor(ToontownGlobals.DefaultBackgroundColor)
