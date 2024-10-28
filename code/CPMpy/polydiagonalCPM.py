from cpmpy import *

# read integer matrix from file
Mat=[[int(x) for x in r.split()] for r in open('M.txt') if r.strip()]
n=len(Mat)

mdl=Model()
# coloring vector decision variables with domains
c=[intvar(-i,i+1,name=f"c_{i}") for i in range(n)]
# spanning set
b={k:[intvar(-1,1,name=f"b_{k}_{i}") for i in range(n)] 
   for k in range(1,n)}
for k in b:
  for i in range(n):
    mdl+=(c[i]== k).implies(b[k][i]== 1)
    mdl+=(c[i]==-k).implies(b[k][i]==-1)
    mdl+=((c[i]!=k) & (c[i]!=-k)).implies(b[k][i]== 0)
# image of spanning set
w={k:[sum(Mat[i][j]*b[k][j] for j in range(n) if Mat[i][j]!=0)
   for i in range(n)] for k in b}

# constraints
# coloring vector
for i in range(1,n):
    mdl+=any([c[i]<=1+c[j] for j in range(i)])
    mdl+=any([c[i]>=0]+[c[i]==-c[j] for j in range(i)])
# M-invariance
for i in range(n):
  mdl+=(c[i]==0).implies(all([w[k][i]==0 for k in b]))
  for j in range(i):
    mdl+=(c[i]== c[j]).implies(all([w[k][i]== w[k][j] for k in b]))
    mdl+=(c[i]==-c[j]).implies(all([w[k][i]==-w[k][j] for k in b]))

# find all solutions
mdl.solveAll(display=lambda: print(*[a.value() for a in c]))