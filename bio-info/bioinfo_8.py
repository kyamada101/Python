import numpy as np 
import math
from scipy.special import logsumexp
from tqdm import tqdm

log05 = np.log(0.5)

test_num = 100
xlength = 10000

final_viterbi_acc = 0
final_post_acc = 0

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

def DICE(n):
    
    #Fairならpi=0,Loadedならpi=1
    
    pi = np.array([1]*(n+1))
    x = np.zeros(n+1)
    
    ef = np.zeros(n+1)
    el = np.zeros(n+1)
    
    pi[0] = np.random.choice([0,1], p = [0.5,0.5])
    
    for i in range(0,n):
        if pi[i] == 0:
            x[i] = np.random.choice([1,2,3,4,5,6],p = [1/6,1/6,1/6,1/6,1/6,1/6])
            pi[i+1] = np.random.choice([0,1],p = [0.95,0.05])
        if pi[i] == 1:
            x[i] = np.random.choice([1,2,3,4,5,6],p = [1/10,1/10,1/10,1/10,1/10,1/2])
            pi[i+1] = np.random.choice([0,1],p = [0.1,0.9])
    
    return x[:n-1],pi[:n-1]

def Viterbi(x):
    x = np.insert(x,0,0)
    n = x.shape[0]
    v = np.zeros([2,n])
    ptr = np.zeros([2,n])
    tr = np.zeros(n)
    
    v[0,0] = 0
    v[1,0] = -float('inf')
    
    for i in range(1,n):
        for l in range(0,2):
            if i == 1:
                v[l,i] = le(l,x[i]) + np.max([v[0,i-1] + log05, v[1,i-1] + log05])
                ptr[l,i] = np.argmax([v[0,i-1] + log05, v[1,i-1] + log05])
            else:
                v[l,i] = le(l,x[i]) + np.max([v[0,i-1] + la(0,l), v[1,i-1] + la(1,l)])
                ptr[l,i] = np.argmax([v[0,i-1] + la(0,l), v[1,i-1] + la(1,l)])
            
    tr[n-1] = np.argmax([v[0,n-1], v[1,n-1]])
        
    for i in range(1,n):
        j = (n-1)-i
        tr[j-1] = ptr[int(tr[j]),j]
        
    return tr[:n-1]

def Forward_Log(x):
    x = np.insert(x,0,0)
    n = x.shape[0]
    f = np.zeros([2,n])
    
    f[0,0] = 0
    f[1,0] = -float('inf')
    
    for i in range(1,n):
        for l in range(0,2):
            if i == 1:
                f[l,i] = le(l,x[i]) + logsumexp([f[0,i-1] + log05, f[1,i-1] + log05])
            else:
                f[l,i] = le(l,x[i]) + logsumexp([f[0,i-1] + la(0,l), f[1,i-1] + la(1,l)])
    
    return f[0][1:f.shape[1]], f[1][1:f.shape[1]]

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

    return b[0][1:b.shape[1]], b[1][1:b.shape[1]]

for j in tqdm(range(test_num)):

    X,pi = DICE(xlength)

    true_ans = pi
    viterbi_ans = Viterbi(X)

    F = Forward_Log(X)
    B = Back_Log(X)
    P = [F[0] + B[0], F[1] + B[1]]
    post_ans = [np.argmax([P[0][i], P[1][i]]) for i in range(len(X))]

    viterbi_acc = 0
    post_acc = 0

    viterbi_acc = np.sum([int(viterbi_ans[i] == true_ans[i]) for i in range(len(true_ans))])/xlength
    post_acc = np.sum([int(post_ans[i] == true_ans[i]) for i in range(len(true_ans))])/xlength

    final_viterbi_acc += viterbi_acc
    final_post_acc += post_acc
    
final_viterbi_acc /= test_num
final_post_acc /= test_num 

print('Viterbi: {:.0%}'.format(final_viterbi_acc))
print('post: {:.0%}'.format(final_post_acc))