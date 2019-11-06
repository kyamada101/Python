import numpy as np

with open("./dice.txt",'r') as f:
    input_str = f.read()
    input_data=list(map(int,input_str))

inf = -float('inf')

class box():
    def __init__(self):
        self.v = inf
        self.root = -1
    def __repr__(self):
        return str(self.v)

def run_viterbi(n,k):
    if X[n][k].v != inf: 
        return X[n][k].v
    if n == 0:
        v = dice_t[k][input_data[n]-1] + np.log(0.5)
        X[n][k].v = v
        X[n][k].root = 0
        return v
    v = dice_t[k][input_data[n]-1] + np.max([run_viterbi(n-1,l) + transition_t[k][l] for l in range(K)])
    X[n][k].v = v
    X[n][k].root = np.argmax([run_viterbi(n-1,l) + transition_t[k][l] for l in range(K)])
    return v

N = len(input_data)-1

K = 2
trans_p = np.array([[0.95,0.1],[0.05,0.9]])
dice_p = np.array([[1/6,1/6,1/6,1/6,1/6,1/6],[1/10,1/10,1/10,1/10,1/10,1/2]])
transition_t = np.log(trans_p)
dice_t = np.log(dice_p)

X = np.array([[box() for l in range(K)] for k in range(N+1)])
run_viterbi(N,0)

with open('./dice_result.txt','w') as f:
    f.write("Eyes of dice：{}".format(input_str))
    f.write("\n")
    f.write("Anticipation is following： \n")
    def trace(n,k):
        if n > 0:trace(n-1,X[n][k].root)
        if X[n][k].root == 0:
            f.write("F")
        else:
            f.write("L")
        return 0

    trace(N,0)