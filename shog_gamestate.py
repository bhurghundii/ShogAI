class shog_gamestate():
    def __init__(self, board_size, gameMatrix):
            self.board_size = board_size
            self.isBlackTurn = True
            self.isCheck = False
            self.gameState = 0
            self.newMatrixPosX = None
            self.newMatrixPosY = None
            self.oldMatrixPosX = None
            self.oldMatrixPosY = None
            self.pieceSelected = None
            self.possibleMoveMatrix = []
            self.gameMatrix = gameMatrix
            self.blackcaptured = []
            self.whitecaptured = []
            self.droprank = 0
            self.isLoad = False
            self.isAI = False
