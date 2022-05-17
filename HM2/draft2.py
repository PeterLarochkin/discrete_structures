variables = []
from itertools import product
from PyMiniSolvers import minisolvers
# from timeit import repeat
# https://logic.pdmi.ras.ru/~arist/papers/sat09.pdf
# basis is {Sheffer stroke}

# N - quantity of element
# n - input variables
def Sheffer_stroke(a, b):
    if a and b:
        return 1
    else:
        return 0
N = 2

def stupid_match(bin):
    if bin == 0:
        return "0_0_"
    if bin == 1:
        return "0_1_"
    if bin == 2:
        return "1_0_"
    if bin == 3:
        return "1_1_"

def support(binum:str):
    for i in range(len(binum)//4):
        if binum[i:i + 4] == "1110":
            return True
    return False
def requirement1_(N: int, n: int):
    final_clause = []
    for num in range(2**(4*N)):
        binNum =  "{}".format(bin(num))[2:]
        binNum = (("0"*((4*N) - len(binNum)))+binNum)
        if not support(binNum):
            localClause = []
            for i, item in enumerate(binNum):
                sign = "-" if item else ""
                localClause.append(f"{sign}t_{n + i // 4}_{stupid_match(i % 3)}")
            final_clause.append("V".join(localClause))
    return("Λ".join(final_clause))  
n = 1  
print(requirement1_(N, n))