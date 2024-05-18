# Finds coloring vectors of synchrony subspaces invariant under the matrix Mat
from z3 import *
from read_matrix import read_matrix

Mat=read_matrix('M.txt')
n=len(Mat)

# coloring vector
c=IntVector('x',n)
# bases
b=[[If(c[j] == i,1,0) for j in range(n)] for i in range(n+1)]
# Mat*bases
w=[[Sum([Mat[i][j]*(b[k][j]) for j in range(n)]) for i in range(n)] for k in range(n+1)]

s=Solver()

# enforce coloring vector
s.add(c[0]==1)
for i in range(1,n):
    s.add(1<=c[i],c[i]<=i+1)
    s.add(Or([c[i]<=c[j]+1 for j in range(i)]))

# enforce invariance
for k in range(1,n+1):
    for i in range(n):
        for j in range(i):
            s.add(Implies(c[i]==c[j],w[k][i]==w[k][j]))

while s.check()==sat:
    mod=s.model()
    ss=[mod[c[i]] for i in range(n)]
    print(*ss)
    s.add(Or([c[i]!=mod[c[i]] for i in range(n)]))
