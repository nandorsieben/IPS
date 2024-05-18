# Finds coloring vectors of synchrony subspaces invariant under the matrix Mat
from ortools.sat.python import cp_model
from read_matrix import read_matrix

class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count=0
    def on_solution_callback(self):
        sol=[self.Value(v) for v in self.__variables]
        self.__solution_count+=1
        print(*sol)
    def solution_count(self):
        return self.__solution_count

# b <=> expr
def reiff(model,expr,not_expr):
    b = model.NewBoolVar("bb_" + str(expr))
    model.Add(expr).OnlyEnforceIf(b)
    model.Add(not_expr).OnlyEnforceIf(b.Not())
    return b

Mat=read_matrix('M.txt')
n=len(Mat)
model=cp_model.CpModel()

# coloring vector decision variables
c=[model.NewIntVar(1, n, f'c_{i}') for i in range(n)]
# bases
b=[[model.NewIntVar(0, 1, f'b_{k}_{i}') for i in range(n)] for k in range(1,n + 1)]
b.insert(0,[0 for i in range(n)])
for k in range(1,n+1):
  for i in range(n):
    bb=reiff(model,c[i]==k,c[i]!=k)
    model.Add(b[k][i]==1).OnlyEnforceIf(bb)
    model.Add(b[k][i]==0).OnlyEnforceIf(bb.Not())
# Application of Mat
w=[[sum(Mat[i][j]*b[k][j] for j in range(n)) for i in range(n)] for k in range(n+1)]

# Enforce coloring vector
model.Add(c[0]==1)
for i in range(1,n):
  model.Add(c[i] <= i+1)
  model.AddBoolOr([reiff(model,c[i]<=c[j]+1,c[i]>c[j]+1) for j in range(i)])

# Enforce invariance
for k in range(1, n + 1):
  for i in range(n):
    for j in range(i):
      # If c[i] == c[j], then w[k][i] == w[k][j]
      model.Add(w[k][i]==w[k][j]).OnlyEnforceIf(reiff(model,c[i]==c[j],c[i]!=c[j]))

def SolveSingle(model):
  solver = cp_model.CpSolver()
  solution_printer = VarArraySolutionPrinter(c)
  solver.parameters.enumerate_all_solutions = True
  solver.parameters.cp_model_presolve = False
  solver.parameters.search_branching=cp_model.FIXED_SEARCH
  status = solver.Solve(model, solution_printer)

SolveSingle(model)
