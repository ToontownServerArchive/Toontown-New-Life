#Embedded file name: toontown.minigame.Maze
from toontown.minigame.MazeBase import MazeBase
from toontown.minigame import MazeData

class Maze(MazeBase):

    def __init__(self, mapName, mazeData = MazeData.mazeData, cellWidth = MazeData.CELL_WIDTH):
        model = loader.loadModel(mapName)
        mData = mazeData[mapName]
        self.treasurePosList = mData['treasurePosList']
        self.numTreasures = len(self.treasurePosList)
        MazeBase.__init__(self, model, mData, cellWidth)
