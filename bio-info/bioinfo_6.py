import math
from scipy.special import logsumexp

def logsumexp_list(lst):
    while len(lst)>1:
        a = lst.pop(0)
        b = lst.pop(0)
        c = b + math.log10(math.exp(a - b) + 1)
        lst.insert(0,c)
    return lst[0]

def forward(X):
    K = 2
    F0_1 = []
    F0_2 = []
    E = [[1/6,1/6,1/6,1/6,1/6,1/6], [1/10,1/10,1/10,1/10,1/10,1/2]]
    a = [[0.95,0.1], [0.05,0.9]]
    for i in range(K):
        if i == 0:
            F0_1.append(1)
            F0_2.append(0)
        else:
            F0_1.append(0)
            F0_2.append(-1000000)
    Fi_1 = F0_1
    Fi_2 = F0_2
    Slst = []
    
    for i,xi in enumerate(X):
        next_fi1 = []
        next_fi2 = []
        si = 0
        
        for l,el in enumerate(E):
            sumf = 0
            logsumexplst = []
            
            for k,fi in enumerate(Fi_1):
                if i == 0:
                    sumf += fi * (1/2)
                else:
                    sumf += fi * a[l][k]
            
            for k,fi in enumerate(Fi_2):
                if i == 0:
                    logsumexplst.append(fi + math.log(0.5))
                else:
                    logsumexplst.append(fi + math.log(a[l][k]))
            
            sumf1 = logsumexp_list(logsumexplst)
            next_fi1.append(el[xi-1]*sumf)
            si += el[xi-1]*sumf
            
            next_fi2.append(math.log10(el[xi-1]) + sumf1)
            
        Fi_2 = next_fi1
        
        next_fi2 = []
        Slst.append(si)
        for j in next_fi1:
            next_fi2.append(j/si)
        Fi_2 = next_fi2
        
    answer2 = 1
    for s in Slst:
        answer2 = answer2*s
    print(answer2)
    
    ans = 0
    for f in Fi_2:
        ans += math.exp(f)
    print(ans)

X = "315116246446644245311321631164152133625144543631656626566666651166453132651245636664631636663162326455236266666625151631222555441666566563564324364131513465146353411126414626253356366163666466232534413661661163252562462255265252266435353336233121625364414432335163243633665562466662632666612355245242"

X = [int(i) for i in X]
print(len(X))
forward(X)