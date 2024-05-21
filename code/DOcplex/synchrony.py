# Finds coloring vectors of synchrony subspaces invariant under the matrix Mat
from docplex.cp.model import CpoModel

Mat=[[int(x) for x in line.strip().split()] for line in open('M.txt')]
n=len(Mat)
mdl=CpoModel(name='synchrony')

# coloring vector decision variables
c=[mdl.integer_var(min=1,max=i+1,name=f"c_{i}") for i in range(n)]
# bases
b=[[mdl.conditional(c[i]==k,1,0) for i in range(n)] for k in range(n+1)]
# application of Mat on the bases
w=[[mdl.sum(Mat[i][j]*b[k][j] for j in range(n)) for i in range(n)] for k in range(n+1)]

# enforce coloring vector
mdl.add_constraint(c[0]==1)
for i in range(1, n):
    mdl.add(c[i]<=i + 1)
    mdl.add(mdl.logical_or([c[i]<=c[j]+1 for j in range(i)]))

# enforce invariance
for k in range(1,n+1):
    for i in range(1, n):
        for j in range(i):
            mdl.add(mdl.if_then(c[i]==c[j],w[k][i]==w[k][j]))

siter=mdl.start_search(SearchType='DepthFirst',Workers=1,LogVerbosity='Quiet')
for sol in siter:
    print(*[sol[c[i]] for i in range(n)])
