#Embedded file name: toontown.coghq.boardbothq.BoardOfficeLavaRoomFoyer_Battle01_Cogs
from toontown.coghq.SpecImports import *
from toontown.toonbase import ToontownGlobals
CogParent = 10000
BattleParent = 10005
BattleCellId = 0
BattleCells = {BattleCellId: {'parentEntId': BattleParent,
                'pos': Point3(0, 0, 0)}}
CogData = [{'parentEntId': CogParent,
  'boss': 1,
  'level': ToontownGlobals.BoardOfficeBossLevel,
  'battleCell': BattleCellId,
  'pos': Point3(-6, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 0,
  'revives': 1},
 {'parentEntId': CogParent,
  'boss': 0,
  'level': ToontownGlobals.BoardOfficeCogLevel + 1,
  'battleCell': BattleCellId,
  'pos': Point3(-2, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 0},
 {'parentEntId': CogParent,
  'boss': 0,
  'level': ToontownGlobals.BoardOfficeCogLevel,
  'battleCell': BattleCellId,
  'pos': Point3(2, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 0},
 {'parentEntId': CogParent,
  'boss': 0,
  'level': ToontownGlobals.BoardOfficeCogLevel,
  'battleCell': BattleCellId,
  'pos': Point3(6, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 0}]
ReserveCogData = []
