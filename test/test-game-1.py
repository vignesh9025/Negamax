class TTT(object):

    def __init__(self):
        self.movesExplored = 0
        self.board = [' ']*9
        self.player = 'X'
        if False:
            #self.board = ['O', 'X', 'X', 'O', 'O', ' ', ' ', 'X', ' ']
            self.board = ['O', 'O', ' ', 'X', ' ', ' ', ' ', ' ', 'X']
            self.player = 'O'
        self.playerLookAHead = self.player

    def locations(self, c):
        return [i for i, mark in enumerate(self.board) if mark == c]

    def getMoves(self):
        moves = self.locations(' ')
        return moves

    def getUtility(self):
        whereX = self.locations('X')
        whereO = self.locations('O')
        wins = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
                [0, 3, 6], [1, 4, 7], [2, 5, 8],
                [0, 4, 8], [2, 4, 6]]
        isXWon = any([all([wi in whereX for wi in w]) for w in wins])
        isOWon = any([all([wi in whereO for wi in w]) for w in wins])
        if isXWon:
            return 1 if self.playerLookAHead is 'X' else -1
        elif isOWon:
            return 1 if self.playerLookAHead is 'O' else -1
        elif ' ' not in self.board:
            return 0
        else:
            return None  ########################################################## CHANGED FROM -0.1

    def isOver(self):
        return self.getUtility() is not None

    def makeMove(self, move):
        self.movesExplored += 1
        self.board[move] = self.playerLookAHead
        self.playerLookAHead = 'X' if self.playerLookAHead == 'O' else 'O'

    def changePlayer(self):
        self.player = 'X' if self.player == 'O' else 'O'
        self.playerLookAHead = self.player

    def unmakeMove(self, move):
        self.board[move] = ' '
        self.playerLookAHead = 'X' if self.playerLookAHead == 'O' else 'O'

    def __str__(self):
        s = '{}|{}|{}\n-----\n{}|{}|{}\n-----\n{}|{}|{}'.format(*self.board)
        return s
    def getNumberMovesExplored(self):
        return self.movesExplored
    def getWinningValue(self):
        return 1

def negamax(game, depthLeft):
    # If at terminal state or depth limit, return utility value and move None
    if game.isOver() or depthLeft == 0:
        return game.getUtility(), None
    # Find best move and its value from current state
    bestValue = -float('infinity')
    bestMove = None
    for move in game.getMoves():
        # Apply a move to current state
        game.makeMove(move)
        # Use depth-first search to find eventual utility value and back it up.
        #  Negate it because it will come back in context of next player
        value, _ = negamax(game, depthLeft-1)
        # Remove the move from current state, to prepare for trying a different move
        game.unmakeMove(move)
        if value is None:
            continue
        value = - value
        if value > bestValue:
            # Value for this move is better than moves tried so far from this state.
            bestValue = value
            bestMove = move
    return bestValue, bestMove

def negamaxIDS(game, maxDepth):
    for depth in range(1, maxDepth):
        print("We're at depth: ", depth)
        # CALLING negamax FOR EACH DEPTH VALUE
        result, move = negamax(game, depth)
        if result == 1:
            return result, move
    return result, move

def opponent(board):
    return board.index(' ')

def playGame(game,opponent,depthLimit):
    print(game)
    while not game.isOver():
        score,move = negamaxIDSab(game,depthLimit)
        if move == None :
            #print('move is None. Stopping.')
            continue
        game.makeMove(move)
        print('Player', game.player, 'to', move, 'for score' ,score)
        print(game)
        if not game.isOver():
            game.changePlayer()
            opponentMove = opponent(game.board)
            game.makeMove(opponentMove)
            print('Player', game.player, 'to', opponentMove)   ### FIXED ERROR IN THIS LINE!
            print(game)
            game.changePlayer()
    print('Number of moves explored', game.getNumberMovesExplored())

def negamaxab(game, depthLeft, alpha = -float('inf'), beta = float('inf')):
    # If at terminal state or depth limit, return utility value and move None
    if game.isOver() or depthLeft == 0:
        return game.getUtility(), None

    # Find best move and its value from current state
    bestValue = -float('infinity')
    bestMove = None
    for move in game.getMoves():

        # Negate and swap values of alpha and beta
        #alpha = -alpha
        #beta = -beta
        #temp = alpha
        #alpha = beta
        #beta = temp
        
        # Apply a move to current state
        game.makeMove(move)
        # Use depth-first search to find eventual utility value and back it up.
        #  Negate it because it will come back in context of next player
        value, _ = negamaxab(game, depthLeft-1, -beta, -alpha)
        # Remove the move from current state, to prepare for trying a different move
        game.unmakeMove(move)
        if value is None:
            continue
        value = - value
        if value > bestValue:
            # Value for this move is better than moves tried so far from this state.
            bestValue = value
            bestMove = move
        alpha = max(bestValue, alpha)
        if bestValue >= beta:
            return bestValue, bestMove
    return bestValue, bestMove


def negamaxIDSab(game, maxDepth):
    for depth in range(1, maxDepth):
        print("We're at depth: ", depth)
        # CALLING negamax FOR EACH DEPTH VALUE
        result, move = negamaxab(game, depth)
        if result == 1:
            return result, move
    return result, move

if __name__ == '__main__':
    game = TTT()
    #print(negamaxIDSab(game,20))
    print("negaIDSab")
    playGame(game, opponent, 10)
    