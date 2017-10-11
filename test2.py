import time
def negamax(game, depthLeft):
    #time.sleep(0.1)
    # If at terminal state or depth limit, return utility value and move None
    if game.isOver() or depthLeft == 0:
        return game.getUtility(), None
    # Find best move and its value from current state
    bestValue, bestMove = None, None
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
        if bestValue is None or value > bestValue:
            # Value for this move is better than moves tried so far from this state.
            bestValue, bestMove = value, move
    print("We're at depth: ", depthLeft)
    return bestValue, bestMove

class New(object):
    def __init__(self):
        self.movesExplored = 0
        self.board = 0
        self.player = 'A'
        self.playerLookAHead = self.player
        self.acount = 0
        self.bcount = 0 

    def getMoves(self):
        moves = range(1,10)
        moves = list(moves)
        for i in moves:
            n = self.board + i
            if n > 10:
                moves.remove(i)
        return moves

    def getUtility(self):
        if self.board == 10:
            # A wins
            if self.playerLookAHead == 'A':
                return 1
            # B wins
            else:
                return -1
        else:
            return None 

    def isOver(self):
        return self.getUtility() is not None

    # 'move' is a number between 0 and 9
    def makeMove(self, move):
        self.movesExplored += 1
        self.board += move
        
        self.playerLookAHead = 'A' if self.playerLookAHead == 'B' else 'B'

    def changePlayer(self):
        self.player = 'A' if self.player == 'B' else 'B'
        self.playerLookAHead = self.player

    def unmakeMove(self, move):
        self.board -= move
        self.playerLookAHead = 'A' if self.playerLookAHead == 'B' else 'B'

    def __str__(self):
        return str(self.board)
    def getNumberMovesExplored(self):
        return self.movesExplored
    def getWinningValue(self):
        return 1

    def incCount(self):
        if self.playerLookAHead == 'A':
            self.acount += 1
        else:
            self.bcount += 1

def negamaxab(game, depthLeft, alpha = -float('inf'), beta = float('inf')):
    # If at terminal state or depth limit, return utility value and move None
    if game.isOver() or depthLeft == 0:
        return game.getUtility(), None

    # Find best move and its value from current state
    bestValue, bestMove = None, None
    for move in game.getMoves():
        # Apply a move to current state
        game.makeMove(move)
        #print(game)
        # Use depth-first search to find eventual utility value and back it up.
        #  Negate it because it will come back in context of next player
        value, _ = negamaxab(game, depthLeft-1, -beta, -alpha)
        # Remove the move from current state, to prepare for trying a different move
        game.unmakeMove(move)
        if value is None:
            continue
        value = - value
        if bestValue is None or value > bestValue:
            # Value for this move is better than moves tried so far from this state.
            bestValue, bestMove = value, move
        alpha = max(bestValue, alpha)
        if bestValue >= beta:
            return bestValue, bestMove
    return bestValue, bestMove

# This function computes the Effective Branching Factor (EBF) for a tree with 'nNodes' nodes and depth 'depth'. 
# We use Binary Search to compute the EBF.

def ebf(nNodes, depth, precision = 0.01):
    # Initialize low and high values.
    left = 1
    right = nNodes
    # If no nodes in tree return 0
    if nNodes == 0:
        return 0
    # Keep iterating till the difference between left and right is lesser than the specified precision.
    b = 1.0
    while(True):
        # If the difference is lesser than the precision, then break out.
        if abs(right - left) <= precision:
            break
        # Get the middle value
        b = (left + right)/2
        
        # Solve equation to find n
        n = (pow(b, (depth+1)) - 1)/(b - 1)
        if nNodes < n:
            right = b - precision
        elif nNodes > n:
            left = b + precision
        else:
            return b
    return b    

def negamaxIDSab(game, maxDepth):
    for depth in range(maxDepth + 1):
        #print("We're at depth: ", depth)
        #print("Game: ", game)
        # CALLING negamax FOR EACH DEPTH VALUE
        result, move = negamaxab(game, depth)
        winVal = game.getWinningValue()
        if result == winVal:
            return result, move
    return result, move

def negamaxIDS(game, maxDepth):
    for depth in range(maxDepth + 1):
        #print("We're at depth: ", depth)
        #print("Game: ", game)
        # CALLING negamax FOR EACH DEPTH VALUE
        result, move = negamax(game, depth)
        winVal = game.getWinningValue()
        if result == winVal:
            return result, move
    return result, move

def playGames2(opponent, depthLimit, funlist):
    # Create an empty list to maintain a list of strings which are to be printed at the ned.
    strlst = []
    for fun in funlist:
        print(fun.__name__, ':')
        game = New()
        print(game)
        while not game.isOver():
            score,move = fun(game,depthLimit)
            if move == None :
                print('move is None. Stopping.')
                break
            game.incCount()
            game.makeMove(move)
            print('Player', game.player, 'to', move, 'for score' ,score)
            print(game)
            if not game.isOver():
                game.changePlayer()
                opponentMove = opponent(game)
                #print(opponentMove)
                game.makeMove(opponentMove)
                print('Player', game.player, 'to', opponentMove)   ### FIXED ERROR IN THIS LINE!
                print(game)
                game.changePlayer()
        # Get depth
        dep =  game.acount + game.bcount
        strlst.append(fun.__name__ + ' made ' + str(game.acount) + ' moves. ' + str(game.getNumberMovesExplored()) + ' moves explored for ebf(' + str(game.getNumberMovesExplored()) + ', ' + str(dep) + ') of ' + str(round(ebf(game.getNumberMovesExplored(), dep), 2)))
    for s in strlst:
        print(s)

import random as rd
def opponent2(game):
    diff = 10 - game.board
    if diff <= 8:
        r = rd.randint(1,diff)
    else:
        r = rd.randint(1, 9)
    return r

if __name__ == '__main__':
    playGames2(opponent2, 6, [negamax])
    #print(negamaxab(New(), 5))