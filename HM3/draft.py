import random
from time import sleep
from mpi4py import MPI
import os

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
# паралельно
# mpiexec -n 2 python draft.py
# обычно просто кнопка

# print(rank)

# print('My rank is ',rank)


graph_string = open("graph.txt", "r").read()
graph = [ [int(i) for i in s.split(" ")] for s in graph_string.split("\n")]
τ = [ [float(1) for i in s ] for s in graph]
η = [ [1 / i for i in s ] for s in graph]
α = 1
β = 1
p = 0.1
Q = 100

def print_tau(τ)->str:
    return "\n".join([ " ".join([ f"{item:.{2}f}" for item in st]) for st in τ])
# file = open('tau.txt', 'w')
# file.write(print_tau([ [1 for i in s ] for s in graph]))
# file.close()

def sum_and_half_it(a, b):
    ans = τ = [ [float(0) for i in s ] for s in graph]
    for i, item in enumerate(a):
        for j, jtem in enumerate(item):
            ans[i][j] = (a[i][j]+b[i][j])/2
    return ans

def play_the_probability(list_of_prob):
    value = random.random()
    current_value = 0
    for num, prob in list_of_prob:
        current_value += prob 
        if value < current_value:
            return num

def sworm(graph, τ) -> list[int]:
    antitabu = list(range(len(graph)))
    initial_node = random.choice(antitabu)
    current_node = initial_node
    # antitabu.append(current_node)
    path = []
    while len(antitabu)!= 0:
        antitabu.remove(current_node)
        path.append(current_node)
        if len(antitabu) == 0:
            return path
        i = current_node
        # adj_nodes = (graph[current_node])
        
        # print([ ((η[i][k]**β) * (τ[i][k]**α)) for k, item in enumerate(graph[i]) if k in antitabu])
        denominator = sum([ (η[i][k]**β) * (τ[i][k]**α) for k, item in enumerate(graph[i]) if k in antitabu])
        probs = [(j, (η[i][j]**β) * (τ[i][j]**α)/ (denominator)) for j, item in enumerate(graph[i]) if j in antitabu]
        current_node = play_the_probability(probs)
        # print(current_node, end="")
    if graph[path[-1]][initial_node] != 0:
        path.append(initial_node)
        return path
    else:
        return None

while True:
    try:
        # f = open("tau.txt", "r")
        # tau_string = f.read()
        # τ = [ [float(i) for i in s.split(" ")] for s in graph_string.split("\n")]
        # f.close()
        path = sworm(graph, τ)
        # print(path)
        # print(int(len(path), len(graph))
        # if len(path) + 1 == len(graph) :
        if path:
            # path легитимный
            # print(path)
            L = 0
            # τ_for_add = [ [ 0.0 for _ in s ] for s in graph]
            edges = []   
            for i in range(len(path)-1):
                edge = (path[i], path[i+1])
                edges.append(edge)
                L += graph[edge[0]][edge[1]]
            
            for i, item in enumerate(τ):
                for j, jtem in enumerate(item):
                    # print(Q/L)
                    if (i, j) in edges:
                        τ[i][j] = (1-p)*τ[i][j] + Q/L
                    else:
                        τ[i][j] = (1-p)*τ[i][j]
        # print("**"*6)
            if size == 2:
                if rank == 0:
                    data = τ

                    comm.send(data, dest=1, tag=11)
                    data = comm.recv(source=1, tag=11)
                    τ = sum_and_half_it(data, τ)
                elif rank == 1:
                    data = τ
                    comm.send(data, dest=0, tag=11)
                    data = comm.recv(source=0, tag=11)
                    τ = sum_and_half_it(data, τ)


            os.system('clear')
            
            
            file = open('tau.txt', 'w')
            file.write(print_tau(τ))
            file.close()
            if rank == 0:
                print(f"Цена цикла равна: {L}")
                print(print_tau(τ))
                print("**"*6)
                sleep(1)
            else:
                print(f"Цена цикла равна: {L}")
                print(print_tau(τ))
                print("**"*6)
                sleep(1)
    except KeyboardInterrupt:
        break
    