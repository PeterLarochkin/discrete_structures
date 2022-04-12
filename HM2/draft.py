from PyMiniSolvers import minisolvers
# S = minisolvers.MinisatSolver()
# for i in range(4):
#     S.new_var()  
# for clause in [1], [-2], [-1, 2, -3], [3, 4]:
#     S.add_clause(clause)  
# S.solve()
# получим решение
# print(list(S.get_model()))
isPow2 = lambda n: ((n&(n-1)==0) and n) and (True) or (False)

vectorOfValue = "1110001011100010"
numOfVars = len("{}".format(bin(len(vectorOfValue)-1)))-2
print(numOfVars)
ans = 0
nums = []
edges = []
if not isPow2(len(vectorOfValue)):
    raise Exception("bad length")

for num in range(len(vectorOfValue)):
    if not int(vectorOfValue[num]):
        binNum = "{}".format(bin(num))[2:]
        nums.append(num)
        print(("0"*(numOfVars - len(binNum)))+binNum, vectorOfValue[num])
        ans = ans | num
brackets = []
for inum, num in enumerate(nums):
    binNum = "{}".format(bin(num))[2:]
    varInBrackets = []
    for i, item in enumerate((("0"*(numOfVars - len(binNum)))+binNum)):
        if item == "0":
            varInBrackets.append(" x{} ".format(i))
        else:
            varInBrackets.append(" -x{} ".format(i))
    for i in range(len(varInBrackets)):
        if i <=1:
            edges.append(((varInBrackets[i]), "V{}/0".format(inum)))
        else:
            edges.append(("V{}/{}".format(inum,i-2),"V{}/{}".format(inum,i-1)))
            edges.append((varInBrackets[i],"V{}/{}".format(inum,i-1)))
    if inum <=1:
        edges.append(("V{}/{}".format(inum,((len(varInBrackets))-2)), "Λ0".format(inum)))
    elif inum < len(nums):
        edges.append(("Λ{}".format(inum-2),"Λ{}".format(inum-1)))
        edges.append(("V{}/{}".format(inum,((len(varInBrackets))-2)),"Λ{}".format(inum-1)))
    
    brackets.append("("+"V".join(varInBrackets)+")")

# print("Λ".join(brackets))  
for i in range((numOfVars)):
    edges.append((" x{} ".format(i)," -x{} ".format(i))) 
print(edges)


# libraries
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
 
# Build a dataframe with your connections
df = pd.DataFrame({ 'from':[a for a,_ in edges], 'to':[a for _,a in edges]})
 
# Build your graph
G=nx.from_pandas_edgelist(df, 'from', 'to')
 
# Graph with Custom nodes:
nx.draw(G, with_labels=True, node_size=1500, node_color="skyblue", node_shape="s", alpha=0.5, linewidths=40)
plt.show()
    