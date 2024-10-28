# Finds coloring vectors of polydiagonal subspaces invariant under the matrix Mat
from z3 import *

def max(l):
  if len(l)==0:
    return 0
  m=l[0]
  for a in l[1:]:
    m=If(a>m,a,m)
  return m

# read integer matrix from file
Mat =[[int(x) for x in r.split()] for r in open('M.txt') if r.strip ()]
n=len(Mat)

s=Solver()
# coloring vector decision variables with domains
c=IntVector('c',n)
# maximums
m={i:max([c[j] for j in range(i)]) for i in range(1,n)}
# spanning set
b={k:[If(c[i]==k,1,If(c[i]==-k,-1,0)) for i in range(n)] for k in range(1,n)}
# image of spanning set
w={k:[Sum([Mat[i][j]*(b[k][j]) for j in range(n) if Mat[i][j]!=0]) for i in range(n)]  for k in b}

# constraints
# coloring vector
for i in range(n):
    s.add(-i<=c[i],c[i]<=i+1)
for i in range(1,n):
    s.add(-m[i]<=c[i])
    s.add(c[i]<=1+m[i])
# M-invariance
for k in b:
    for i in range(n):
        s.add(Implies(c[i]==0,w[k][i]==0))
        for j in range(i):
            s.add(Implies(c[i]==c[j],w[k][i]==w[k][j]))
            s.add(Implies(c[i]==-c[j],w[k][i]==-w[k][j])) 

# find all solutions
while s.check()==sat:
    mod=s.model()
    ss=[mod[c[i]] for i in range(n)]
    print(*ss)
    s.add(Or([c[i]!=mod[c[i]] for i in range(n)]))
