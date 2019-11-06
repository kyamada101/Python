import numpy as np
import matplotlib.pyplot as plt

#点の生成
#A = [1,2][0,1][-1,0][-1,2]
#B = [0,-1][-1,-2][-1,1][-2,0]
Np = 4
Nn = 4
A = np.ones((Np,2))
B = np.ones((Nn,2))
A[0,:] = [1,2]
A[1,:] = [0,1]
A[2,:] = [-1,0]
A[3,:] = [-1,2]
B[0,:] = [0,-1]
B[1,:] = [-1,-2]
B[2,:] = [-1,1]
B[3,:] = [-2,0]

X = np.concatenate([A,B])
y = np.concatenate([np.repeat(-1,Np),np.repeat(1,Nn)])

Xte = X
yte = y

max_iter = 1000
tol = 1e-7
Xtr = np.c_[np.ones(len(y)),X]
alpha = np.zeros(len(X)) #重みの初期値α

#R行列を作成
R = np.eye(len(X))
for i in range(len(X)):
    for j in range(len(X)):
        R[i,j] = np.dot(X[i],X[j])

#Y行列を作成
Y = np.eye(len(y))
for i in range(len(y)):
    for j in range(len(y)):
        Y[i,j] = np.dot(y[i],y[j])


c = 0.2 #ソフトマージン用ハイパーパラメータ
C = 100
tmp = np.zeros(alpha.shape)

A = R*Y

for iteration in range(max_iter):
    wold = alpha

    for i in range(len(alpha)):
        if alpha[i] > C:
            alpha[i] = C
        print(alpha)
        alpha += c*(((-1)*A[i,:])*alpha+1)
    print(alpha)
    print(np.sum(alpha-wold)**2)

    if np.sum((alpha-wold)**2)<=tol:
        break

Xte = np.c_[np.ones(len(yte)),Xte]
label = np.zeros(len(yte))
for i in range(len(label)):
    label[i] = 2*(Xte[i,0]*alpha[i]>=0)-1

print("accuracy:{}".format(np.sum(label==yte)/np.float(len(yte))))

colors = np.array(["r","b"])
cy = 1*(y==1)
plt.scatter(X[:,0],X[:,1],color = colors[cy])

nx,ny = Np,Nn
x_min,x_max = plt.xlim()
y_min,y_max = plt.ylim()
xx,yy = np.meshgrid(np.linspace(x_min,x_max,nx),np.linspace(y_min,y_max,ny))
PX = np.c_[xx.ravel(),yy.ravel()]
PX = np.c_[np.ones(PX.shape[0]),PX]

Z = PX.dot(alpha)
Z = Z.reshape(xx.shape)
plt.contour(xx,yy,Z,[0],linewidths = 2.,colors='black')
plt.tight_layout()
plt.show()