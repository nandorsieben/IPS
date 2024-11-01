## Python code to compute invariant polydiagonal subspaces

CPMpy: 
- Uses the CP-SAT solver of Google's ortools package as the default solver.
- Can use other solvers.
- Simple syntax makes it easy to modify the code.
- Not as fast as ORtools.

DOcplex: 
- Uses the CP Optimizer of IBM.
- Requires separate installation of the CP Optimizer (free academc licence).
- Simple syntax.
- Expect very fast solving time for simpler problems.
- Cannot handle some larger problems.

ORtools: 
- Uses the CP-SAT solver of Google's ortools package.
- More complex syntax.
- Best for larger problems.
- Not as fast as DOcplex for simpler problems.

Z3: 
- Uses Microsoft's Z3 Theorem Prover.
- Simple syntax.
- Fairly slow. Use it for simple problems.
