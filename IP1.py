import sys
import math
from gurobipy import *


###############################################
# Read data function
###############################################
def read_data(f):
	f = open(sys.argv[1])

	params = f.readline().split()
	N = int(params[0])		# Number nodes

	#Read adjacency matrix
	A = []
	for i in range(N):
		aux = []
		params = f.readline().split()
		for j in range(N):
			aux.append(int(params[j]) )
		A.append(aux)

	return N, A

###############################################
# MAIN
###############################################

# Parse argument
if len(sys.argv) < 2:
    print('Usage: IP1.py file.txt')
    exit(1)
    

# Read file
file_name = open(sys.argv[1])
N, A = read_data(file_name)

print("Number of nodes = ", N)
print("Adjacency matrix = ", A)


n=N #number of nodes

# find value of K, K=max|A(i)|+1
K_array={}
for i in range(n):
    K_array[i]=sum(A[i])
    
K=max(K_array)


# define the set E of all edges
E=set()
for i in range (n):
    for j in range(i+1,n):
        if A[i][j]==1:
            a=(i+1,j+1)
            E.add(a)
        else:
            pass
        

# define the set of adjacent edges for node i is B(i)
B={}
for i in range(n):
    B[i]=set()
    for j in range(n):
        if A[i][j]==1 and i<j:
            a=(i+1,j+1)
            B[i].add(a)
        elif A[i][j]==1 and i>j:
            a=(j+1,i+1)
            B[i].add(a)
        else:
            pass
   
# Create a new model
model = Model("IP1")
    
m={}
M={}
x={}

# Create variables
for i in range(n): # is start from 0 to n-1
    m[i+1] = model.addVar(lb=1,ub=K,vtype=GRB.INTEGER,name="m[%s]"%(i+1))
    M[i+1] = model.addVar(lb=1,ub=K,vtype=GRB.INTEGER,name="M[%s]"%(i+1))
        
for e in E:
    for k in range (K):
        x[e,k+1] = model.addVar(vtype=GRB.BINARY, name="x[%s,%s]"%(e,k+1))
    
# Integrate new variables
model.update()
    
# Set objective
model.setObjective(quicksum(M[i+1]-m[i+1]-sum(A[i])+1 for i in range(n)),GRB.MINIMIZE)


# add constraint that no adjacent edges have the same number
for i in range(n):
    for k in range(K):
        model.addConstr(quicksum(x[e,k+1] for e in B[i]) <=1)

# add constraint that each edge should be assigned a number
for e in E:
    model.addConstr(quicksum(x[e,k+1]for k in range(K)) == 1)

# add constraint that define mi and Mi
for i in range(n):
    for e in B[i]:
        model.addConstr(quicksum((k+1)*x[e,k+1]for k in range(K)) >= m[i+1])
        model.addConstr(quicksum((k+1)*x[e,k+1]for k in range(K)) <= M[i+1])
        
# add constraint that define the relationship between Mi and mi
for i in range(n):
     model.addConstr(M[i+1]-m[i+1] >= sum(A[i])-1)
     
     
model.Params.timelimit = 600.0  
model.optimize()


model.write('IP1.lp')

print('')
print('Solution:')
print('')

for v in model.getVars():
      if v.X != 0:
        print("%s %f" % (v.Varname, v.X))

        


        
    
    