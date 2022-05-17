from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    data = "pivo"
    comm.send(data, dest=1, tag=11)
    print(f"send pivo by {0}")
    data = comm.recv(source=1, tag=11)
    print(f"get by {0}: {data}")
elif rank == 1:
    data = "vodka"
    comm.send(data, dest=0, tag=11)
    print(f"send vodka by {1}")
    data = comm.recv(source=0, tag=11)
    print(f"get by {1}: {data}")