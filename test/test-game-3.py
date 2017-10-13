import time
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
    return bestValue, bestMove
def negamaxIDS(game, maxDepth):
    for depth in range(1, maxDepth):
        #print("We're at depth: ", depth)
        # CALLING negamax FOR EACH DEPTH VALUE
        result, move = negamax(game, depth)
        if result == 1:
            return result, move
    return result, move

class New(object):
    def __init__(self):
        self.movesExplored = 0
        self.board = 0
        self.player = 'A'
        self.playerLookAHead = self.player
        self.acount = 0
        self.bcount = 0 

    def getMoves(self):
        moves = range(10)
        moves = list(moves)
        for i in moves:
            n = self.board + i
            if n > 100:
                moves.remove(i)
        return moves

    def getUtility(self):
        if self.board == 100:
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
        if self.playerLookAHead == 'A':
            self.acount += 1
        else:
            self.bcount += 1
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

def negamaxab(game, depthLeft, alpha = -float('inf'), beta = float('inf')):
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



def negamaxIDSab(game, maxDepth):
    for depth in range(maxDepth + 1):
        #print("We're at depth: ", depth)
        # CALLING negamax FOR EACH DEPTH VALUE
        result, move = negamaxab(game, depth)
        winVal = game.getWinningValue()
        if result == winVal:
            return result, move
    return result, move

def playGames2(opponent2, depthLimit, funlist):
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
            game.makeMove(move)
            print('Player', game.player, 'to', move, 'for score' ,score)
            print(game)
            if not game.isOver():
                game.changePlayer()
                opponentMove = opponent(game.board)
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
def opponent2():
    #r = rd.randint(0, 9)
    return 1

def winRate(opponent, depthLimit, funlist, n):
    # Iterate through funlist
    for fun in funlist:
        # Print the name of the function being tried out currently.
        print()
        print('Now we are trying out function: ', fun.__name__)
        # Maintain a list to append the score of each game that is played.
        scorelist = []
        # Loop to play 'n' games.
        for i in range(n):
            # Instantiate TTT object
            print(i)
            game = TTT()
            while not game.isOver():
                # Call function (algorithm)
                score,move = fun(game,depthLimit)
                # If depthLimit is not sufficient
                if move == None :
                    print('Insufficient depth specified. Stopping game!')
                    break
                # Apply move
                game.makeMove(move)
                if not game.isOver():
                    # Change player and let opponent make move.
                    game.changePlayer()
                    opponentMove = opponent(game.board)
                    game.makeMove(opponentMove)
                    game.changePlayer()
            # Get score for the current game and append it to a score list.
            scorelist.append(score)
        # Here, we compute the average number of games won by player X. 
        # If the 'score' value returned is 1, then X has won the game. Otherwise, it's either a draw or a loss, in which
        # case, 0 or -1 is returned respectively.
        # We then divide the number of times X has won (number of occurances of 1 in scorelist) with the total 
        # number of games played which is n.  
        average = (scorelist.count(1)/n) * 100 # We multiply by 100 to express the fraction as a percentage.
        # Print the results.
        print('In', n, ' games, player X has won', average, "% of the times against player Y." )
        print()

def opponent3(board):
    # Find out empty positions in the game board.
    moves = [i for i, mark in enumerate(board) if mark == ' ']
    # Generate random integer. This shall be used as the index for 'moves' list, thereby producing a random move.
    r = rd.randint(0, len(moves)-1)
    # Return random move
    return moves[r]

if __name__ == '__main__':
    winRate(opponent3, 10, [negamaxIDS], 10)