class state_persistent():
    def __init__(self, gameMatrix, isBlackTurn, blackcaptured, whitecaptured):
            self.isBlackTurn = True
            self.gameMatrix = gameMatrix
            self.blackcaptured = []
            self.whitecaptured = []

    def getGameState():
        with open('AI_layer/movetoplay.txt') as f:
            print f.read()
