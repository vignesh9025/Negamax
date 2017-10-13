# Objective is to implement Negamax game playing algorithm for a game of Tic-Tac-Toe.

### Assumes that the argument 'game' is an object with the following methods
# game.getMoves()
# game.makeMove(move)    changes lookahead player
# game.unmakeMove(move)  changes lookahead player
# game.changePlayer()    changes next turn player
# game.getUtility()
# game.isOver()
# game.__str__()

inf = float('infinity')

def negamax(game, depthLeft):
    # If at terminal state or depth limit, return utility value and move None
    if game.isOver() or depthLeft == 0:
        return game.getUtility(), None
    # Find best move and its value from current state
    bestValue = -inf
    bestMove = None
    for move in game.getMoves():
        # Apply a move to current state
        game.makeMove(move)
        # print('trying',game)
        # Use depth-first search to find eventual utility value and back it up.
        #  Negate it because it will come back in context of next player
        value, _ = negamax(game, depthLeft-1)
        value = - value
        # Remove the move from current state, to prepare for trying a different move
        game.unmakeMove(move)
        if value > bestValue:
            # Value for this move is better than moves tried so far from this state.
            bestValue = value
            bestMove = move
    return bestValue, bestMove

# To apply NM with TTT, we use the following game class definition.

class TTT(object):

	# Initializes the game board with 9 blanks and current player as X.
    def __init__(self):
        self.movesExplored = 0
        self.board = [' ']*9
        self.player = 'X'
        if False:
            self.board = ['X', 'X', ' ', 'X', 'O', 'O', ' ', ' ', ' ']
            self.player = 'O'
        # Another variable used for ?
        self.playerLookAHead = self.player

    # Searches the board list and returns the all the locations of either X or O (specified in c). 
    def locations(self, c):
        return [i for i, mark in enumerate(self.board) if mark == c]

    # Returns the blank locations in the game board. ie possible places to make a move. 
    def getMoves(self):
        moves = self.locations(' ')
        return moves

    # To get the utility value of a state if it's a terminal state. Returns 1, -1 or 0.
    def getUtility(self):
    	# Find where all the Xs are.
        whereX = self.locations('X')
        # Find where all the Os are.
        whereO = self.locations('O')

        # All possible winning states. That is, if either X or O is in any of these straight lines, it's a win.
        wins = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
                [0, 3, 6], [1, 4, 7], [2, 5, 8],
                [0, 4, 8], [2, 4, 6]]

        # Find out if either X or O won. If X or O are in the locations specified in 'wins' then they have won.
        isXWon = any([all([wi in whereX for wi in w]) for w in wins])
        isOWon = any([all([wi in whereO for wi in w]) for w in wins])

        # In Negamax, we return from the perspective of the current players playing. 
        # if X has won, return 1 if current player is X otherwise return -1.
        if isXWon:
            return 1 if self.playerLookAHead is 'X' else -1
        # if O has won, return 1 if current player is O otherwise return -1.
        elif isOWon:
            return 1 if self.playerLookAHead is 'O' else -1

        # No more moves left and neither X or O has won, then it's a draw.
        elif ' ' not in self.board:
            return 0

        # No terminal state has been reached.
        else:
            return None

    # To check if game is over. If yes, returns the utility value of final.
    def isOver(self):
        return self.getUtility() is not None

    # Takes in the board and position which is empty. Initializes the current player with empty position specified.
    def makeMove(self, move):
        self.movesExplored += 1
        self.board[move] = self.playerLookAHead
        self.playerLookAHead = 'X' if self.playerLookAHead == 'O' else 'O'

    # Changes the current player
    def changePlayer(self):
        self.player = 'X' if self.player == 'O' else 'O'
        self.playerLookAHead = self.player

    # Undo the move made.
    def unmakeMove(self, move):
        self.board[move] = ' '
        self.playerLookAHead = 'X' if self.playerLookAHead == 'O' else 'O'

    # For printing the game board in a neat format.
    def __str__(self):
        s = '{}|{}|{}\n-----\n{}|{}|{}\n-----\n{}|{}|{}'.format(*self.board)
        return s

    def getNumberMovesExplored(self):
    	return self.movesExplored

# We play it using the following function
def playGameNegamax(game):
    print(game)
    while not game.isOver():
        value, move = negamax(game, 9)
        if move is None:
            print('move is None. Stopping')
            break
        game.makeMove(move)
        print("\nPlayer", game.player, "to", move, "for value", value)
        print(game)
        game.changePlayer()
    print("Number: ", game.getNumberMovesExplored())

if __name__ == '__main__':
	playGameNegamax(TTT())