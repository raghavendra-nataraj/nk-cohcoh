import sys

def printBoard(board):
    for i in range(0,n):
        print board[i*n:i*n+n]

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
    num = 0
    h=0
    v=0
    d1 =0
    d2 =0
    num = len([i for i in board if i!='.'])
    if num == n**2-1: return 1
    for i in range (0,n):
        for j in range(0,n):
            h = 0
            v = 0
            d1 = 0
            d2 = 0
            for k1 in range(0,k):
                hc = i*n+j +k1
                vc = ((i+k1)*n+j)
                d1c = ((i+k1)*n + j+k1)
                d2c = ((i+k1)*n + j-k1)
                if hc < n**2 and j+k<n and board[hc] == chance: h+=1
                else : h=0
                if vc < n**2 and board[vc] == chance: v +=1
                else : v=0
                if d1c < n**2 and board[d1c] == chance: d1 +=1
                else : d1=0                
                if d2c <n**2 and board[d2c] == chance: d2 +=1
                else : d2=0
            #print i,j,k1,h,v,d1,d2
            if d1==k or d2==k or h==k or v==k:
                return True
    return False

def min_value(board):
    chance = whoChance(board)
    if isTerminal(board,chance):
        return -1
    return min([max_value(state) for state in successors(board)])

def max_value(board):
    chance = whoChance(board)
    if isTerminal(board,chance):
        return 1
    return max([min_value(state) for state in successors(board)])
              
def solve(board):
    evalVal  = -sys.maxint - 1
    bb = []
    chance = whoChance(board)
    for state in successors(board):
        if isTerminal(state,chance):
            return state
        tempVal = min_value(state)
        if tempVal >= evalVal:
            evalVal = tempVal
            bb = state
    return bb

n = int(sys.argv[1])
k = int(sys.argv[2])
board = list(sys.argv[3])
printBoard(solve(board))
#printBoard(board)
#print isTerminal(board,'w')
#for succ in successors(board):
t = sys.argv[4]
