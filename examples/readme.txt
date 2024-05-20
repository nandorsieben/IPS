=== Example names: 
Buckyball: Adjacency matrix of the Buckyball graph (Example 6.3)
BuckyballQuotient: Adjacency matrix of a quotient digraph of the Buckyball graph (Example 6.3)
Cycle50: Laplacian of the cycle graph with 50 vertices (Table 5.1)
Path100: Laplacian of the path graph with 100 vertices (Example 6.2)
Petersen: Adjacency matrix of the Petersen graph (Example 6.1)
basic: basic example (Example 4.4)

=== File types:
M.txt: matrix
output.txt: coloring vectors of M-invariant polydiagonal subspaces

=== File types created by post-processing.  (The post-processing software is not available.)
poset.pdf: lattice of M-invariant polydiagonal subspaces
posetOrbit.pdf: poset of orbit classes of M-invariant polydiagonal subspaces
summary.txt: summary of the information computed in post-processing in human-readable form
graph.pdf: graph whose adjacency matrix is M

=== Details of summary.txt file:
The first line of the summary.txt file labels the columns
The classes (group orbits) are computed and given a label c, the first column in human.txt. These are the numbers in posetOrbit.pdf
The second column indicates if the polydiagonal subspaces in this class are AIS.  If not, they are fixed point subspaces.
The third column indicates the dimension of the polydiagonal subspaces in this class.
The fourth column indicates the size of the point stabilizer of the polydiagonal subspaces in this class.
The fifth column indicates how many polydiagonal subspaces are in this class.
Then the numbers of the polydiagonal subspaces (listed in output.txt) are listed.
