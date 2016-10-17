'''
(1) Abstraction for problem 1:

a. Valid State, S = A nxn board with any possible arrangement of 'w' and 'b' such that number of 'w' and 'b' is the same or the number of 'w' is one more than 'b'. Also the number of continuous 'w' or 'b' in any row, column or diagonal cannot be greater than k.

b. Initial State, S0 = A nxn board with a give combination of 'w' and 'b' such that number of 'w' and 'b' are same or the number of 'w' is one more than 'b'. Also the number of continuous 'w' or 'b'  in any row, column or diagonal is not greater than k. 

c. Cost : The cost is constant since placing each marble has the same cost.

d. Successors, Succ(S) = {S' | S' is a list of all possible ways the next 'w' (or 'b', based on input) can be placed in empty slots('.') on the given board}

e. Goal State, G = {S | S has continuous k number of w's (or b's, whichever represents the opponent) in any row, column or diagonal of the board}
number of 'w' or 'b' in state is not greater than k in any row, column or diagonal

f. Heuristics : Taking different combinations of k marbles after adding the new marble and calculating the desirability of the state and deciding the most favorable state is the heuristics. For eg. [w,w,w] for a k value of 3 is very bad for while marble. So we give high negative weightage to the evaluation function. Similarly for the same value of k [.,.,.] is a favorable situation and also it does not prevent the opponent from losing. So it has a positive weightage. So we do this for all possible combinations and of states and add the wining and loosing chances and decide the most favorable state. 

 
(2) Description of how the program works:
Initially we take the current state and check if it is already a terminal state. If not, we generate successors. For each Successor, we call the the min_value for each state. The min_value will generate successors again and call max_value for each of the successors. This recursion will continue as long as the state is terminal state or the iteration depth has reached its limit. At each iteration we print the max of all min nodes for that depth. Then we increase the depth and try solving the problem again. This is repeated till the terminal is reached. The max value takes the max out of all the min_value functions. Similarly, the min_Value takes a minimum of all the max_value. We also prune the tree when the the min_value returns a value lesser than the parent max node. Similarly, we prune it when the max_value returns a value greater than the parent min node. I have not followed any logic is assigning weigtage to combination while calculating the evaluation function rather I have assigned the weights intuitively.

(3) Problems faced and design decisions made:
At certain times, the states had the same evaluation value but states in that ended in lesser depth than the others. So, it was not returning the most favorable state despite giving faster results. So, I introduced the depth factor in the evaluation function and that returned me the most favorable state. 

'''


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
    chance = whoChance(st.board)
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
        n+=1;w+=-0.8;l+=0.3
    if hl == ['w']:
       n+=1;w-=2;l+=0.5;result = True 
    if hl == ['.','b']:
        l+=-0.8;n+=1;w+=0.3
    if hl == ['b']:
        n+=1;l-=2;w+=0.5;result = True
    if hl == ['.']:
        n+=1;l+=0.5;w+=0.5
    if hl == ['b','w'] or hl == ['.','b','w']:
        n+=1;l+=1;w+=1
    return [n,w,l,result]

def evalFunc(board,chance,depth):
    result = False
    num = 0;w=0;l=0
    extra = 0
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
    if  len([i for i in board if i!='.']) == n**2:
        result = True
    #printBoard(board)
    #print w,l
    if ch =='w':
        return [(l-w)+depth,result]
    else:
        return [(w-l)+depth,result]

def min_value(st,alpha,beta):
    global waitfor
    chance = whoChance(st.board)
    name = "".join(st.board)
    if name not in cache:
        status = cache[name] = evalFunc(st.board,chance,st.depth)
    status = cache[name]
    #if isTerminal(board,chance):
    if status[1]  or st.depth>=depth:
        return status[0]
    vals = [max_value(state,alpha,beta) for state in successors(st) if st.depth <=depth]
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
        status = cache[name] = evalFunc(st.board,chance,st.depth)
    status = cache[name]
    if status[1] or st.depth>=depth:
        return status[0]
    vals = [min_value(state,alpha,beta) for state in successors(st) if st.depth <=depth]
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
        #print state.board
        tempVal = min_value(state,-sys.maxint,sys.maxint)
        #print tempVal
        #printBoard(state.board)
        if tempVal > evalVal:
            evalVal = tempVal
            bb = state
    return bb
depth = 0
print sys.argv
n = int(sys.argv[1])
k = int(sys.argv[2])
board = list(sys.argv[3])
t = int(sys.argv[4])
waitfor =  calendar.timegm(time.gmtime())+t-1
if whoChance(board)=="w":
    ch = "b"
else:
    ch = "w"
if isTerminal(board,ch):
    print "Game Over"
else:
    while waitfor>calendar.timegm(time.gmtime()) and depth<board.count('.'):
        depth+=1
        goal = solve(State(board,0)).board
        #printBoard(goal)
	print "".join(goal)
        print "\n"
