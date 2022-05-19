from itertools import product
from PyMiniSolvers import minisolvers
import os

def req1(num_gates_n: int, num_gates_N: int, disjunctions_list):
    i_range = range(num_gates_n, num_gates_N + num_gates_n)
    for i in i_range:
        clauses = [(f"t_{i}_0_0_" ), (f"t_{i}_0_1_" ),
                   (f"t_{i}_1_0_" ), (f"-t_{i}_1_1_" )]
        disjunctions_list.extend(clauses)


def req2(num_gates_n: int, num_gates_N: int, disjunctions_list):
    i_range = range(num_gates_n, num_gates_n + num_gates_N)
    k_range = range(2)
    j_range = range(num_gates_N + num_gates_n)
    for (i, k) in product(i_range, k_range):
        existence_cond_variables = list((f"c_{i}_{k}_{j}_" for j in range(i)))  # range(i)))
        disjunctions_list.append(existence_cond_variables)
        for j_1 in j_range:
            for j_2 in range(num_gates_n, num_gates_N + num_gates_n):
                if j_2 < j_1:
                    disjunction_clause = [f"-c_{i}_{k}_{j_1}_", f"-c_{i}_{k}_{j_2}_"]
                    disjunctions_list.append(disjunction_clause)
            
def req2_(num_gates_n: int, num_gates_N: int, disjunctions_list):
    i_range = range(num_gates_n, num_gates_n + num_gates_N)
    k_range = range(2)
    j_range = range(num_gates_N + num_gates_n)
    for (i, k) in product(i_range, k_range):
        existence_cond_variables = list((f"c_{i}_{k}_{j}_" for j in range(i)))  # range(i)))
        disjunctions_list.append(existence_cond_variables)
        for j_1 in range(i + 1, num_gates_N + num_gates_n):
            for j_2 in range(i + 1, num_gates_N + num_gates_n):
                if j_2 == j_1:
                    continue
                disjunction_clause = [f"-c_{i}_{k}_{j_1}_", f"-c_{i}_{k}_{j_2}_"]
                disjunctions_list.append(disjunction_clause)

def req3(num_gates_n: int, num_gates_N: int, output_size_m: int, disjunctions_list):
    i_range = range(num_gates_n, num_gates_n + num_gates_N)
    j_range = range(output_size_m)
    for j in j_range:
        existence_cond = list(f"o_{i}_{j}_" for i in i_range)
        disjunctions_list.append(existence_cond)
        for i_1 in i_range:
            # for i_2 in range(i_1 + 1, num_gates_n + num_gates_N):
            for i_2 in i_range:
                if i_1 == i_2:
                    continue
            # if i_1 < i_2:
                disjunction_clause = [f"-o_{i_1}_{j}_", f"-o_{i_2}_{j}_"]
                disjunctions_list.append(disjunction_clause)





def req4(num_gates_n: int, input_sets, disjunctions_list):
    i_range = range(num_gates_n)
    t_range = range(2 ** num_gates_n)
    assert len(input_sets) == 2 ** num_gates_n
    for (i, t) in product(i_range, t_range):
        input_value = input_sets[t][i]
        sign = '' if input_value == 1 else '-'
        clause = (f"{sign}v_{i}_{t}_")
        disjunctions_list.append(clause)


def req5(num_gates_n: int, num_gates_N: int, disjunctions_list):
    i_range = range(num_gates_n, num_gates_N + num_gates_n)
    t_range = range(2 ** num_gates_n)
    bit_range = range(2)
    for (i, r, i_0, i_1) in product(i_range, t_range, bit_range, bit_range):
        for j_0 in range(0, i):
        # for j_0 in i_range:    
            for j_1 in range(0, i):
                i_0_sign = '-' if i_0 == 1 else ''
                i_1_sign = '-' if i_1 == 1 else ''

                clause_1 = [f"-c_{i}_{0}_{j_0}_", f"-c_{i}_{1}_{j_1}_", f"{i_0_sign}v_{j_0}_{r}_",
                            f"{i_1_sign}v_{j_1}_{r}_", f"v_{i}_{r}_", f"-t_{i}_{i_0}_{i_1}_"]
                clause_2 = [f"-c_{i}_{0}_{j_0}_", 
                            f"-c_{i}_{1}_{j_1}_", 
                            f"{i_0_sign}v_{j_0}_{r}_",
                            f"{i_1_sign}v_{j_1}_{r}_", 
                            f"-v_{i}_{r}_", 
                            f"t_{i}_{i_0}_{i_1}_"]
                disjunctions_list.append(clause_1)
                disjunctions_list.append(clause_2)


def req6(num_gates_n: int, num_gates_N: int, output_size_m: int, values, disjunctions_list):
    i_range = range(num_gates_n, num_gates_N + num_gates_n)
    r_range = range(2 ** num_gates_n)
    k_range = range(output_size_m)
    for (i, r, k) in product(i_range, r_range, k_range):
        value = values[r][k]
        sign = '' if value == 0 else '-'
        clause = [f"-o_{i}_{k}_", f"{sign}v_{i}_{r}_"]
        disjunctions_list.append(clause)








# например
# 1101
# 11011101
# 11011001
# old
vectorOfValue = "1110"
vectorOfValue = vectorOfValue.replace("1", "a").replace("0", "1").replace("a", "0")
# print(vectorOfValue)
# exit()
quantityOfElement = 2


import math
numOfVars = int(math.log2(len(vectorOfValue)))
if 2 ** numOfVars != len(vectorOfValue):
    raise ValueError("bad length")
print(numOfVars)
dis_list = []
req1(quantityOfElement, numOfVars, dis_list)
string_clause = ""
string_clause += "Λ".join(dis_list)
dis_list = []
req2_(numOfVars, quantityOfElement, dis_list)
string_clause +=  "Λ" + "Λ".join([ "V".join(dis) for dis in dis_list])
dis_list = []
req3(numOfVars, quantityOfElement, 1, dis_list)
string_clause +=  "Λ" +  "Λ".join([ "V".join(dis) for dis in dis_list])
dis_list = []
input_sets = list(product((0, 1), repeat=numOfVars))
req4(numOfVars, input_sets, dis_list)
string_clause +=  "Λ" + "Λ".join(dis_list)
dis_list = []
req5(numOfVars, quantityOfElement, dis_list)
string_clause +=  "Λ" +  "Λ".join([ "V".join(dis) for dis in dis_list])
dis_list = []
values = [(int(value),) for value in vectorOfValue]
req6(numOfVars, quantityOfElement, 1,values,dis_list)


string_clause +=  "Λ" +  "Λ".join([ "V".join(dis) for dis in dis_list])  
# string_clause += f"Λo_{numOfVars + quantityOfElement - 1}_0_"
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


# os.system("rm scheme.dot")
# os.system("rm scheme.dot.png")

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