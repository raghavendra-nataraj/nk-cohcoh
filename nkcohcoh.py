import sys

def whoChance(board):
    w =0
    b =0
    for c in board:
        if c=='w': w+=1
        if c=='b': b+=1
    if b==w: return 'w'
    else: return 'b'

def add_marble(board,index,chance):
    tmpBoard = board[:]
    tmpBoard[index] = chance
    return tmpBoard
    
def successors(board):
    chance = whoChance(board)
    return [add_marble(board,idx,chance) for idx,i in enumerate(board) if i=='.']

def evalFn(b):
    return 1

def isTerminal(board,chance):
    h=0
    v=0
    d1=0
    d2=0
    num = 0
    num = len([i for i in board if i!='.'])
    if num == n**2-1: return 1
    for i in range (0,n):
        if board[i] == chance: h+=1
        else: h=0
        if board[i*n] == chance: v+=1
        else: v=0
        if board[i*n+i] == chance: d1+=1
        else: d1=0
        if board[i*n +(n-1-i)] == chance: d2+=1
        else: d2=0
        if h==k or v==k or d1==k or d2==k:
            return 1
    return 0

def min_value(board):
    if isTerminal(board,'b'):
        return -1#evalFn(b)
    return min([max_value(state) for state in successors(board)])

def max_value(board):
    if isTerminal(board,'w'):
        return 1#evalFn(b)
    return max([min_value(state) for state in successors(board)])
              
def solve(board):
    evalVal  = -sys.maxint - 1
    bb = []
    for state in successors(board):
        tempVal = min_value(state)
        if tempVal > evalVal:
            evalVal = tempVal
            bb = state
    return bb

n = int(sys.argv[1])
k = int(sys.argv[2])
board = list(sys.argv[3])
print solve(board)
#for succ in successors(board):
t = sys.argv[4]
