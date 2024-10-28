# Finds coloring vectors of polydiagonal subspaces invariant under the matrix Mat
from ortools.sat.python import cp_model

class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables=variables
        self.__solution_count=0
    def on_solution_callback(self):
        sol=[self.Value(v) for v in self.__variables]
        self.__solution_count+=1
        print(*sol)
    def solution_count(self):
        return self.__solution_count

# b <=> expr
def reiff(expr,deny):
    global model
    b=model.NewBoolVar("bb_"+str(expr))
    model.Add(expr).OnlyEnforceIf(b)
    model.Add(deny).OnlyEnforceIf(b.Not())
    return b

Mat=[[int(x) for x in r.split()] for r in open('M.txt') if r.strip()]
n=len(Mat)

model=cp_model.CpModel()
# coloring vector decision variables with domains
c=[model.NewIntVar(1,i+1,f'c_{i}') for i in range(n)]
# spanning set
b={k:[model.NewIntVar(0,1,f'b_{k}_{i}') for i in range(n)] for k in range(1,n)}
for k in b:
  for i in range(n):
    b1=reiff(c[i]== k,c[i]!= k)
    model.Add(b[k][i]== 1).OnlyEnforceIf(b1)
    model.Add(b[k][i]== 0).OnlyEnforceIf(b1.Not())
# image of spanning set
w={k:[sum(Mat[i][j]*b[k][j] for j in range(n) if Mat[i][j]!=0) for i in range(n)] for k in b}

# constraints
# coloring vector
for i in range(1,n):
  model.AddBoolOr([reiff(c[i]<=c[j]+1,c[i]>c[j]+1) for j in range(i)])
# M-invariance
for i in range(n):
  for j in range(i):
    model.AddBoolAnd([reiff(w[k][i]== w[k][j],w[k][i]!= w[k][j]) for k in b]).OnlyEnforceIf(reiff(c[i]== c[j],c[i]!= c[j]))

# find all solutions
solver=cp_model.CpSolver()
solution_printer=VarArraySolutionPrinter(c)
solver.parameters.enumerate_all_solutions=True
solver.parameters.cp_model_presolve=False
solver.parameters.search_branching=cp_model.FIXED_SEARCH
solver.Solve(model,solution_printer)
