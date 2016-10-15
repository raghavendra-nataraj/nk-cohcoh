import sys
import time
import calendar
cache = {}
waitfor = 0

class State():
    def __init__(self,board,depth):
        self.board = board
        self.depth = depth

def printBoard(board):
    for i in range(0,n):
        print " ".join(board[i*n:i*n+n])

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
    
def successors(st):
    chance = whoChance(board)
    return [State(add_marble(st.board,idx,chance),st.depth+1) for idx,i in enumerate(st.board) if i=='.']

def isTerminal(board,chance):
    num = 0
    num = len([i for i in board if i!='.'])
    if num == n**2: return 1
    for i in range (0,n):
        for j in range(0,n):
            h = 0;v = 0;d1 = 0;d2 = 0
            for k1 in range(0,k):
                hc = i*n+j +k1
                vc = ((i+k1)*n+j)
                d1c = ((i+k1)*n + j+k1)
                d2c = ((i+k1)*n + n-j-k1-1)
                if hc < n**2 and j+k1<n and board[hc] == chance: h+=1
                else : h=0
                if vc < n**2 and board[vc] == chance: v +=1
                else : v=0
                if d1c < n**2 and j+k1<n and board[d1c] == chance: d1 +=1
                else : d1=0                
                if d2c <n**2 and j+k1<n and board[d2c] == chance: d2 +=1
                else : d2=0
            #print i,j,k1,h,v,d1,d2
            if d1==k or d2==k or h==k or v==k:
                return True
    return False

def checkStat(hl):
    n=0;w=0;l=0
    result = False
    hl = sorted(set(hl))
    if hl == ['.','w']:
        w+=2;n+=1
    if hl == ['w']:
       n+=1;w+=3;result = True 
    if hl == ['.','b']:
        l+=2;n+=1
    if hl == ['b']:
        n+=1;l+=3;result = True
    if hl == ['.']:
        n+=1;l+=1;w+=1
    if hl == ['b','w'] or hl == ['.','b','w']:
        n+=1
    return [n,w,l,result]

def evalFunc(board,chance):
    result = False
    num = 0;w=0;l=0
    for i in range (0,n):
        for j in range(0,n):
            h = 0;v = 0;d1 = 0;d2 = 0
            hl=[];vl=[];d1l=[];d2l=[]
            for k1 in range(0,k):
                hc = i*n+j +k1
                vc = ((i+k1)*n+j)
                d1c = ((i+k1)*n + j+k1)
                d2c = ((i+k1)*n + n-j-k1-1)
                if hc < n**2 and j+k1<n: h+=1;hl.append(board[hc])
                if vc < n**2: v +=1;vl.append(board[vc])
                if d1c <n**2 and j+k1<n:d1 +=1;d1l.append(board[d1c])
                if d2c <n**2 and j+k1<n: d2 +=1;d2l.append(board[d2c])
            if len(hl)==k :
                val = checkStat(hl)
                num+=val[0];w+=val[1];l+=val[2]
                if not result: result = val[3]
            if len(vl)==k :
                val = checkStat(vl)
                num+=val[0];w+=val[1];l+=val[2]
                if not result: result = val[3]
            if len(d1l)==k :
                val = checkStat(d1l)
                num+=val[0];w+=val[1];l+=val[2]
                if not result: result = val[3]
            if len(d2l)==k :
                val = checkStat(d2l)
                num+=val[0];w+=val[1];l+=val[2]
                if not result: result = val[3]
    #printBoard(board)
    #print chance
    #print w,l
    if  len([i for i in board if i!='.']) == n**2:
        result = True
    if chance =='w':
        return [num-w-l,result]
    else:
        return [num-l-w,result]

def min_value(st,alpha,beta):
    global waitfor
    chance = whoChance(st.board)
    name = "".join(st.board)
    if name not in cache:
        status = cache[name] = evalFunc(st.board,chance)
    status = cache[name]
    #if isTerminal(board,chance):
    if status[1]:
        return status[0]
    vals = [max_value(state,alpha,beta) for state in successors(st) if st.depth < depth]
    vals.append(beta)
    val = min(vals)
    beta = min(beta,val)
    if alpha>=beta:return beta
    return val

def max_value(st,alpha,beta):
    global waitfor
    chance = whoChance(st.board)
    name = "".join(st.board)
    if name not in cache:
        status = cache[name] = evalFunc(st.board,chance)
    status = cache[name]
    if status[1]:
        return status[0]
    vals = [min_value(state,alpha,beta) for state in successors(st) if st.depth < depth]
    vals.append(alpha)
    val = max(vals)
    alpha = max(alpha,val)
    if alpha>=beta:return alpha
    return val

def solve(st):
    evalVal  = -sys.maxint - 1
    bb = []
    chance = whoChance(st.board)
    for state in successors(st):
        tempVal = max_value(state,-sys.maxint,sys.maxint)
        #print tempVal
        #printBoard(state)
        if tempVal > evalVal:
            evalVal = tempVal
            bb = state
    return bb
depth = 2
print sys.argv
n = int(sys.argv[1])
k = int(sys.argv[2])
board = list(sys.argv[3])
t = int(sys.argv[4])
waitfor =  calendar.timegm(time.gmtime())+t-1
if whoChance(board)=="w":
    chance = "b"
else:
    chance = "w"
if isTerminal(board,chance):
    print "Hey you lost"
else:
    while waitfor>calendar.timegm(time.gmtime()):
        depth+=1
        goal = solve(State(board,0)).board
printBoard(goal)
