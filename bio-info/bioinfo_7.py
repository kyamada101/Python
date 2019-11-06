import numpy as np 
import math
from scipy.special import logsumexp

log05 = np.log(0.5)

x_str = "315116246446644245311321631164152133625144543631656626566666651166453132651245636664631636663162326455236266666625151631222555441666566563564324364131513465146353411126414626253356366163666466232534413661661163252562462255265252266435353336233121625364414432335163243633665562466662632666612355245242"
x = np.array(list(x_str),dtype = np.float32)

#lが状態番号、bがx
def e(l,b):
    if l == 0.0: 
        return 1/6
    elif l == 1.0 and b == 6.0:
        return 1/2
    elif l == 1.0 and b != 6.0:
        return 1/10

#kとlは状態番号
def a(k,l):
    if k == 0.0 and l == 0.0:
        return 0.95
    elif k == 0.0 and l == 1.0:
        return 0.05
    elif k == 1.0 and l == 0.0:
        return 0.1
    elif k == 1.0 and l == 1.0:
        return 0.9

#lは状態番号、bはx
def le(l,b):
    if l == 0.0:
        return np.log(1/6)
    elif l == 1.0 and b == 6.0:
        return np.log(1/2)
    elif l == 1.0 and b != 6.0:
        return np.log(1/10)

#kとlは状態番号
def la(k,l):
    if k == 0.0 and l == 0.0:
        return np.log(0.95)
    elif k == 0.0 and l == 1.0:
        return np.log(0.05)
    elif k == 1.0 and l == 0.0:
        return np.log(0.1)
    elif l == 1.0 and l == 1.0:
        return np.log(0.9)

def Back_Log(x):
    
    x = np.insert(x,0,0)
    n = x.shape[0]
    b = np.zeros([2,n])
    
    b[0,n-1] = np.log(1)
    b[1,n-1] = np.log(1)
    
    for i in range(1,n-1):
        j = (n-1)-i
        for k in range(0,2):
            b[k,j] = logsumexp([la(k,0) + le(0,x[j+1]) + b[0,j+1], la(k,1) + le(1,x[j+1]) + b[1,j+1]])
            
    lp = logsumexp([log05 + le(0,x[1]) + b[0,1], log05 + le(1,x[1]) + b[1,1]])
    
    return np.exp(lp)

def Back_Scale(x):
    x = np.insert(x,0,0)
    
    n = x.shape[0]
    b = np.zeros([2,n])
    s = np.zeros(n)
    
    b[0,n-1] = 1
    b[1,n-1] = 1
    
    for i in range(1,n):
        j = (n-1)-i
        
        if j == 0:
            s[j+1] = 0.5*e(0,x[j+1])*b[0,j+1] + 0.5*e(1,x[j+1])*b[1,j+1]
        else:
            s[j+1] = (a(0,0)+a(1,0))*e(0,x[j+1])*b[0,j+1] + (a(0,1)+a(1,1))*e(1,x[j+1])*b[1,j+1]
        
        for k in range(0,2):
            
            b[k,j] = (1/s[j+1]) * (a(k,0)*e(0,x[j+1])*b[0,j+1] + a(k,1) * e(1,x[j+1])*b[1,j+1])
    
    return np.prod(s[1:])

print("Back_Log_result:{}".format(Back_Log(x)))
print("Back_Scale_result:{}".format(Back_Scale(x)))