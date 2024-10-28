# Finds coloring vectors of polydiagonal subspaces invariant under the matrix Mat
from docplex.cp.model import CpoModel

Mat=[[int(x) for x in r.split()] for r in open('M.txt') if r.strip()]
n=len(Mat)
mdl=CpoModel(name='polydiagonal')

# coloring vector decision variables with domains
c=[mdl.integer_var(min=-i,max=i+1,name=f"c_{i}") for i in range(n)]
# maximums
m=[mdl.max([c[j] for j in range(i)]) for i in range(n)]
# spanning set
b={k:[(c[i]==k)-(c[i]==-k) for i in range(n)] for k in range(1,n)}
# image of spanning set
w={k:[mdl.sum(Mat[i][j]*b[k][j] for j in range(n) if Mat[i][j]!=0) for i in range(n)] for k in b}

# constraints
# coloring vector
for i in range(1,n):
    mdl.add(c[i]<=1+m[i],-m[i]<=c[i])
# M-invariance
for k in b:
    for i in range(n):
        mdl.add(mdl.if_then(c[i]==0,w[k][i]==0))
        for j in range(i):
            mdl.add(mdl.if_then(c[i]== c[j],w[k][i]== w[k][j]))
            mdl.add(mdl.if_then(c[i]==-c[j],w[k][i]==-w[k][j]))

# find all solutions
siter=mdl.start_search(SearchType='DepthFirst',Workers=1,LogVerbosity='Quiet')
for sol in siter:
    print(*[sol[c[i]] for i in range(n)])
