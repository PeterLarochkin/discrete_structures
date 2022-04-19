from typing import final
from PyMiniSolvers import minisolvers
# S = minisolvers.MinisatSolver()
# for i in range(4):
#     S.new_var()  
# for clause in [1], [-2], [-1, 2, -3], [3, 4]:
#     S.add_clause(clause)  
# S.solve()
# получим решение
# print(list(S.get_model()))


variables = []
# https://logic.pdmi.ras.ru/~arist/papers/sat09.pdf
# basis is {Sheffer stroke}

# N - quantity of element
# n - input variables
n = 0
def requirement1(N):
    temp = []
    for i in range(n, n + N):
        variables.append("t_{}_0_0".format(i))
        variables.append("t_{}_0_1".format(i))
        variables.append("t_{}_1_0".format(i))
        variables.append("t_{}_1_1".format(i))

        temp.append("t_{}_0_0".format(i))
        temp.append("t_{}_0_1".format(i))
        temp.append("t_{}_1_0".format(i))
        temp.append("-t_{}_1_1".format(i))
    return "Λ".join(temp)

def requirement2(N):
    temp = []
    finalClause = []
    vars = []
    for i in range(n, n + N):
        for j in range(0, n + N):
            variables.append("c_{}_0_{}".format(i, j))
            variables.append("c_{}_1_{}".format(i, j))

            vars.append("c_{}_0_{}".format(i, j))
            vars.append("c_{}_1_{}".format(i, j))

            temp.append("{}_0_{}'c_{}_0_{}".format(i, j, i, j))
            temp.append("{}_1_{}'c_{}_1_{}".format(i, j, i, j))
    for i in range(n, n + N):
        for k in range(0, 2):
            # localVars = list(filter(lambda var: var[:3] == "{}_{}".format(i, k), temp))
            # clause = "("+"V".join(localVars)+")"
            # количество j переменной n+N
            for num in range(2**(n+N)):
                binNum =  "{}".format(bin(num))[2:]
                binNum = (("0"*((n+N) - len(binNum)))+binNum)
                if binNum.count("1") != 1:
                    temp2 = []
                    for j, item in enumerate(binNum):
                        replaced = "-" if item == "1" else ""
                        clause = replaced+"c_{}_{}_{}".format(i, k, j)
                        temp2.append(clause)
                    finalClause.append("("+ "V".join(temp2) + ")")
    print(vars)
    return "Λ".join(finalClause)

def requirement3(N):
    finalClause = []
    for i in range(n, n + N):
        variables.append("o_{}_{}".format(i, 0))
    for num in range(2**(n+N)):
        binNum =  "{}".format(bin(num))[2:]
        binNum = (("0"*((n+N) - len(binNum)))+binNum)
        if binNum.count("1") != 1:
            temp2 = []
            for i, item in enumerate(binNum):
                replaced = "-" if item == "1" else ""
                clause = replaced+"o_{}_{}".format(i, 0)
                temp2.append(clause)
            finalClause.append("("+ "V".join(temp2) + ")")
    return "Λ".join(finalClause)



exit()














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
    