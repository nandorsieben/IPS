# Finds coloring vectors of polydiagonal subspaces invariant under the integer matrix Mat
from docplex.cp.model import CpoModel

Mat=[[int(x) for x in line.strip().split()] for line in open('M.txt')]
n=len(Mat)
mdl=CpoModel(name='polydiagonal')

# coloring vector decision variables
c=[mdl.integer_var(min=-i,max=i+1,name=f"c_{i}") for i in range(n)]
# max values
m=[mdl.max([c[j] for j in range(i)]) for i in range(n)]
# bases
b=[[mdl.conditional(c[i]==k,1,mdl.conditional(c[i]==-k,-1,0))
    for i in range(n)] for k in range(n+1)]
# Mat*bases
w=[[mdl.sum(Mat[i][j]*b[k][j] for j in range(n)) for i in range(n)] for k in range(n+1)]

# enforce coloring vector
mdl.add(0<=c[0],c[0]<=1)
for i in range(1,n):
    mdl.add(-m[i]<=c[i],c[i]<=1+m[i])

# enforce invariance
for k in range(1,n+1):
    for i in range(n):
        mdl.add(mdl.if_then(c[i]==0,w[k][i]==0))
        for j in range(i):
            mdl.add(mdl.if_then(c[i]==c[j],w[k][i]==w[k][j]))
            mdl.add(mdl.if_then(c[i]==-c[j],w[k][i]==-w[k][j]))

# mdl.print_information()

siter=mdl.start_search(SearchType='DepthFirst',Workers=1,LogVerbosity='Quiet')
for sol in siter:
    print(*[sol[c[i]] for i in range(n)])
