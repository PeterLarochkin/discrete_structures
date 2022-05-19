from typing import final
from PyMiniSolvers import minisolvers
import os
from itertools import product

variables = []
# https://logic.pdmi.ras.ru/~arist/papers/sat09.pdf
# basis is {Sheffer stroke}

# N - quantity of element
# n - input variables
# n = 0



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
        if binum[i:i + 4] != "1110":
            return False
    return True
def requirement1_(N: int, n: int):
    final_clause = []
    for num in range(2**(4*N)):
        binNum =  "{}".format(bin(num))[2:]
        binNum = (("0"*((4*N) - len(binNum)))+binNum)
        if support(binNum):
            localClause = []
            for i, item in enumerate(binNum):
                sign = "-" if item else ""
                localClause.append(f"{sign}t_{n + i // 4}_{stupid_match(i % 4)}")
            
            final_clause.append("V".join(localClause))
    return("Λ".join(final_clause))  





def requirement1(N, n=0):
    temp2 = []
    for i in range(n, n + N):
        # variables.append("t_{}_0_0_".format(i))
        # variables.append("t_{}_0_1_".format(i))
        # variables.append("t_{}_1_0_".format(i))
        # variables.append("t_{}_1_1_".format(i))
        temp = []
        temp2.append(f"t_{i}_0_0_")
        temp2.append(f"t_{i}_0_1_")
        temp2.append(f"t_{i}_1_0_")
        temp2.append(f"-t_{i}_1_1_")
        # temp2.append("V".join(temp))
    return "Λ".join(temp2)



# def requirement2_(N, n=0):
#     temp = []
#     finalClause = []
    
def requirement2_(num_gates_N: int, num_gates_n: int):
    disjunctions_list = []
    i_range = range(num_gates_n, num_gates_n + num_gates_N)
    k_range = range(2)
    j_range = range(num_gates_N + num_gates_n)
    for (i, k) in product(i_range, k_range):
        existence_cond_variables = [f"c_{i}_{k}_{j}_" for j in range(i)]  # range(i)))
        disjunctions_list.append(existence_cond_variables)
        for j_1 in j_range:
            for j_2 in range(j_1 + 1, num_gates_N + num_gates_n):
                if j_1 < j_2:
                    disjunction_clause = [f"-c_{i}_{k}_{j_1}_", f"-c_{i}_{k}_{j_2}_"]
                    disjunctions_list.append(disjunction_clause)
    return "Λ".join(([ "V".join(dis) for dis in disjunctions_list]))

def requirement2(N, n=0):
    finalClause = []
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
                        clause = replaced+"c_{}_{}_{}_".format(i, k, j)
                        temp2.append(clause)
                    
                    finalClause.append("V".join(temp2))
    # print(vars)
    return "Λ".join(finalClause)


def requirement2__(N, n):
    finalClause = []
    for i in range(n, n + N):
        for k in range(0, 2):
            for num in range(2**(n+N)):
                binNum =  "{}".format(bin(num))[2:]
                binNum = (("0"*((n+N) - len(binNum)))+binNum)
                if binNum.count("1") != 1:
                    localClause = []
                    for j, jtem in enumerate(binNum):
                        sign = "" if jtem == "0" else "-"
                        localClause.append(f"{sign}c_{i}_{k}_{j}_")
                    finalClause.append("V".join(localClause))
    return "Λ".join(finalClause)


# print(requirement2__(2, 2))
# exit()
def requirement3(N, n=0):
    finalClause = []
    # for i in range(n, n + N):
    #     variables.append("o_{}_{}_".format(i, 0))
    for num in range(2**(n+N)):
        binNum =  "{}".format(bin(num))[2:]
        binNum = (("0"*((n+N) - len(binNum)))+binNum)
        if binNum.count("1") != 1:
            temp2 = []
            for i, item in enumerate(binNum):
                replaced = "-" if item == "1" else ""
                # variables.append("o_{}_{}_".format(i, 0))
                clause = replaced+"o_{}_{}_".format(i, 0)
                temp2.append(clause)
            finalClause.append(""+ "V".join(temp2) + "")
    return "Λ".join(finalClause)


def requirement3_(num_gates_N: int, num_gates_n: int,  output_size_m: int = 1):
    disjunctions_list = []
    i_range = range(num_gates_n, num_gates_n + num_gates_N)
    j_range = range(output_size_m)
    for j in j_range:
        existence_cond = [f"o_{i}_{j}_" for i in i_range]
        disjunctions_list.append(existence_cond)
        for i_1 in i_range:
            for i_2 in range(i_1 + 1, num_gates_n + num_gates_N):
                if i_1 < i_2:
                    disjunction_clause = [f"-o_{i_1}_{j}_", f"-o_{i_2}_{j}_"]
                    disjunctions_list.append(disjunction_clause)
    for dis in disjunctions_list:
        for var in dis:
            if var[0] == "-":
                variables.append(var[1:])
            else:
                variables.append(var)
    return "Λ".join(["V".join(dis) for dis in disjunctions_list])






def requirement4_(N, num_gates_n: int):
    disjunctions_list = []
    input_sets = list(product((0, 1), repeat=num_gates_n))
    i_range = range(num_gates_n)
    t_range = range(2 ** num_gates_n)
    assert len(input_sets) == 2 ** num_gates_n
    for (i, t) in product(i_range, t_range):
        input_value = input_sets[t][i]
        sign = '' if input_value == 1 else '-'
        clause = (f"{sign}v_{i}_{t}_")
        disjunctions_list.append(clause)
    return "Λ".join(disjunctions_list)


def requirement4(N, n=0):
    finalClause = []
    for t in range(2**n):
        binNum =  "{}".format(bin(t))[2:]
        binNum = (("0" * (n - len(binNum))) + binNum)
        for i, item in enumerate(binNum):
            # variables.append("v_{}_{}_".format(i, t))
            negation = "-" if item == "0" else ""
            finalClause.append(negation + "v_{}_{}_".format(i, t))
    return "Λ".join(finalClause)


def requirement5(N, n=0):
    ""
    finalClause = []
    i_range = range(n, N + n)
    t_range = range(2 ** n)
    bit_range = range(2)
    for (i, r, i0, i1) in product(i_range, t_range, bit_range, bit_range):
        for j0 in range(0, i):
            for j1 in range(j0, i):
                i_0_sign = '-' if i0 == 1 else ''
                i_1_sign = '-' if i1 == 1 else ''
                clause_1 = f"-c_{i}_{0}_{j0}_V-c_{i}_{1}_{j1}_V{i_0_sign}v_{j0}_{r}_V{i_1_sign}v_{j1}_{r}_Vv_{i}_{r}_V-t_{i}_{i0}_{i1}_"
                clause_2 = f"-c_{i}_{0}_{j0}_V-c_{i}_{1}_{j1}_V{i_0_sign}v_{j0}_{r}_V{i_1_sign}v_{j1}_{r}_V-v_{i}_{r}_Vt_{i}_{i0}_{i1}_"
                finalClause.append(clause_1)
                finalClause.append(clause_2)
    return "Λ".join(finalClause)                       

def requirement6_(values, num_gates_n: int, num_gates_N: int, output_size_m: int = 1):
    disjunctions_list = []
    values = [(int(i),) for i in values]
    i_range = range(num_gates_n, num_gates_N + num_gates_n)
    r_range = range(2 ** num_gates_n)
    k_range = range(output_size_m)
    for (i, r, k) in product(i_range, r_range, k_range):
        value = values[r][k]
        sign = '' if value == 1 else '-'
        clause = [f"-o_{i}_{k}_", f"{sign}v_{i}_{r}_"]
        disjunctions_list.append(clause)
    return "Λ".join(["V".join(dis) for dis in disjunctions_list])



def requirement6(vectorValue, n, N):
    finalClause = []
    for k in range(1):
        for r in range(0, 2**n):
            for i in range(n, n + N):
                if vectorValue[r] == "1":
                    v = "v_{}_{}_".format(i, r)
                    o = "-o_{}_{}_".format(i, k)
                    finalClause.append("{}V{}".format(v, o))
                else:
                    v = "-v_{}_{}_".format(i, r)
                    o = "-o_{}_{}_".format(i, k)
                    finalClause.append("{}V{}".format(v, o))
    return "Λ".join(finalClause)    



vectorOfValue = "10011001"
# print()
quantityOfElement = 2
# print("{}".format(bin(len(vectorOfValue)-1)))
numOfVars = len("{}".format(bin(len(vectorOfValue)-1)))-2

isPow2 = lambda n: ((n&(n-1)==0) and n) and (True) or (False)
if not isPow2(len(vectorOfValue)):
        raise Exception("bad valueVector length")

fclause = [
    requirement1(quantityOfElement, numOfVars), 
    requirement2_(quantityOfElement, numOfVars), 
    requirement3_(quantityOfElement, numOfVars), 
    requirement4_(quantityOfElement, numOfVars), 
    requirement5(quantityOfElement, numOfVars), 
    requirement6_(vectorOfValue, numOfVars, quantityOfElement)
    ]


string_clause = "Λ".join(fclause)# + f"Λo_{numOfVars + quantityOfElement - 1}_0_"
final = string_clause
fclause = [ [element for element in dis.split("V")] for dis in string_clause.split("Λ")]
# print(fclause)
variables = set()
for dis in fclause:
    for element in dis:
        if element[0]=="-":
            variables.add(element[1:])
        else:
            variables.add(element)

variables = (list(variables))
map_index_to_item = {}
map_item_to_index = {}

for i, var in enumerate(variables):
    map_index_to_item[i+1] = var
    map_item_to_index[var] = i + 1
    final = final.replace(var, str(map_item_to_index[var]))


lens = len(string_clause.split("Λ"))
for_minisat = f"p cnf {len(map_index_to_item)} {lens} \n"
for dis in string_clause.split("Λ"):
    if "V" in dis:
        for elem in dis.split("V"):
            sign = (-1 if elem[0]=="-" else 1)
            for_minisat += str(sign * map_item_to_index[elem[1:] if elem[0]=="-" else elem]) + " "
    else:
        for_minisat += str((-1 if dis[0]=="-" else 1) * map_item_to_index[dis[1:] if dis[0]=="-" else dis]) + " "
    for_minisat+="0\n"
# print(for_minisat)
file_str = for_minisat
file = open("for_minisat", 'w')
file.write(file_str)
file.close()
minisat_solution = {}
def from_minisat(output_minisat):
    output_minisat = output_minisat.split(" ")[:-1]
    print(output_minisat)
    for item in output_minisat:
        if item[0] == "-":
            minisat_solution[map_index_to_item[int(item[1:])]] = False
        else:
            minisat_solution[map_index_to_item[int(item)]] = True
os.system("minisat for_minisat output")
file = open("output", 'r')


output_minisat= file.read().split("\n")[1]
file.close()
from_minisat(output_minisat)
# print(minisat_solution)
body_string = "\n"
print(minisat_solution)
for key in minisat_solution.keys():
    if minisat_solution[key]:
        if key[0] == "c":
            c = key
            print(c)
            c = c[2:-1]
            c = c.split("_")
            from_ = ("x"+c[2]) if int(c[2]) < numOfVars else ("element"+c[2])
            to_ = ("x"+c[0]) if int(c[0]) < numOfVars else ("element"+c[0])
            body_string = body_string + """ "{}" -> "{}";\n""".format(from_, to_)


        if key[0] == "o":
            o = key
            print(o)
            o = o[2:-1]
            o = o.split("_")
            o[0] = ("x"+o[0]) if int(o[0])< numOfVars else ("element"+o[0])
            body_string = body_string + """ "{}" -> "{}";\n""".format(o[0], "end")


os.system("rm scheme.dot")
os.system("rm scheme.dot.png")
# exit()
file_name = "scheme.dot"
file_str = """digraph G {\n""" + body_string + """\n}"""
file = open(file_name, 'w')
file.write(file_str)
file.close()
os.system("dot -T png -O " + file_name)
exit()

S = minisolvers.MinisatSolver()
for i in range(len(map_index_to_item)):
    S.new_var()  

for dis in final.split("Λ"):
    clause = [ int(elem) for elem in dis.split("V")]
    S.add_clause(clause)  
print(S.solve())
solution = (list(S.get_model()))
print(solution)
exit()
















variables = []
for dis in string_clause.split("Λ"):
    for elem in dis.split("V"):
        if elem[0] == "-":
            variables.append(elem[1:])
        else:
            variables.append(elem)

variables = list(dict.fromkeys(variables))[::-1]

map_index_to_item = {}
map_item_to_index = {}

for i, item in enumerate(variables):
    # string_clause = string_clause.replace(item, str(i+1))
    map_item_to_index[item] = i+1
    map_index_to_item[i] = item

# print(var_map)
# clauses = [ [ (1 if item[0]!="-" else -1) * map_item_to_index[item if item[0]!="-" else item[1:] ]  for item in dis.split("V")] for dis in string_clause.split("Λ") ]
# clauses = [ [int(item) for item in dis.split("V")] for dis in string_clause.split("Λ")]
S = minisolvers.MinisatSolver()
neededIndices = []

for i in range(len(map_index_to_item)):
    S.new_var()  
for dis in  string_clause.split("Λ"):
    clause = dis.split("V")
    clause = [(-1 if item[0]=="-" else 1) * map_item_to_index[item if item[0] != "-" else item[1:]] for item in clause]
# for clause in clauses:
#     print(clause)
    S.add_clause(clause)  
print(S.solve())
# решение
solution = (list(S.get_model()))
body_string = "\n"

for i, item in enumerate(solution):
    if item and (i in map_index_to_item.keys()):
        
        var = map_index_to_item[i]
        # print(var)
        if var[0] == "c":
            c = var
            print(c)
            c = c[2:-1]
            c = c.split("_")
            from_ = ("x"+c[2]) if int(c[2]) < numOfVars else ("element"+c[2])
            to_ = ("x"+c[0]) if int(c[0]) < numOfVars else ("element"+c[0])
            body_string = body_string + """ "{}" -> "{}";\n""".format(from_, to_)


        if var[0] == "o":
            o = var
            print(o)
            o = o[2:-1]
            o = o.split("_")
            o[0] = ("x"+o[0]) if int(o[0])< numOfVars else ("element"+o[0])
            body_string = body_string + """ "{}" -> "{}";\n""".format(o[0], "end")


file_name = "scheme.dot"
file_str = """digraph G {\n""" + body_string + """\n}"""
file = open(file_name, 'w')
file.write(file_str)
file.close()
os.system("dot -T png -O " + file_name)
exit()
