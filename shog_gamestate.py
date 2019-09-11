class shog_gamestate():
    def __init__(self, board_size, gameMatrix):
            self.board_size = board_size
            self.isBlackTurn = False
            self.isCheck = False
            self.gameState = 0
            self.newMatrixPosX = None
            self.newMatrixPosY = None
            self.oldMatrixPosX = None
            self.oldMatrixPosY = None
            self.pieceSelected = None
            self.possibleMoveMatrix = []
            self.gameMatrix = gameMatrix

    def run(self):
        print self.board_size
        print self.gameMatrix
