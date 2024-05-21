# Finds coloring vectors of polydiagonal subspaces invariant under the matrix Mat
from z3 import *

def max(l):
  if len(l)==0:
    return 0
  m=l[0]
  for a in l[1:]:
    m=If(a>m,a,m)
  return m

Mat=[[int(x) for x in line.strip().split()] for line in open('M.txt')]
n=len(Mat)

# coloring vector
c=IntVector('c',n)
# max values
m=[max([c[j] for j in range(i)]) for i in range(n)]
# bases
b=[[If(c[j]==i,1,If(c[j]==-i,-1,0)) for j in range(n)] for i in range(n+1)]
# Mat*bases
w=[[Sum([Mat[i][j]*(b[k][j]) for j in range(n)]) for i in range(n)] for k in range(n+1)]

s=Solver()

# enforce coloring vector
s.add(Or(c[0]==0,c[0]==1))
for i in range(1,n):
    s.add(-m[i]<=c[i])
    s.add(c[i]<=1+m[i])

# enforce invariance
for k in range(1,n+1):
    for i in range(n):
        s.add(Implies(c[i]==0,w[k][i]==0))
        for j in range(i):
            s.add(Implies(c[i]==c[j],w[k][i]==w[k][j]))
            s.add(Implies(c[i]==-c[j],w[k][i]==-w[k][j])) 

while s.check()==sat:
    mod=s.model()
    ss=[mod[c[i]] for i in range(n)]
    print(*ss)
    s.add(Or([c[i]!=mod[c[i]] for i in range(n)]))
