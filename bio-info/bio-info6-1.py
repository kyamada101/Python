import math

def logsumexp_list(lst):
    while len(lst)>1:
        b=lst.pop(0)
        a=lst.pop(0)
        c = b + math.log(math.exp(a-b)+1)
        lst.insert(0,c)
    return lst[0]

def forward(X):
    K=2
    F0=[]
    E=[[1/6,1/6,1/6,1/6,1/6,1/6],[1/10,1/10,1/10,1/10,1/10,1/2]]
    a=[[0.95,0.1],[0.05,0.9]]
    for i in range(K):
        if i==0:
            F0.append(0)
        else:
            F0.append(-1000000)
    Fi=F0
    
    for i,xi in enumerate(X):
        nextfi=[]
        
        for l,el in enumerate(E):
            
            logsumexplst=[]
            for k,f in enumerate(Fi):
                if i==0:
                    logsumexplst.append(f+math.log(0.5))
                else:
                    logsumexplst.append(f+math.log(a[l][k]))
            sumf1 = logsumexp_list(logsumexplst)
            
            nextfi.append(math.log(el[xi-1])+sumf1)
        Fi = nextfi
    summation=0
    for f in Fi:
        summation+=math.exp(f)
    print(summation)

X="315116246446644245311321631164152133625144543631656626566666651166453132651245636664631636663162326455236266666625151631222555441666566563564324364131513465146353411126414626253356366163666466232534413661661163252562462255265252266435353336233121625364414432335163243633665562466662632666612355245242"
X=[int(i) for i in X]

forward(X)