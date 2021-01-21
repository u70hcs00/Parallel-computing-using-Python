from mpi4py import MPI
import numpy as np
import socket
import os

pid  = os.getpid()
comm = MPI.COMM_WORLD
host = socket.gethostname()

d = np.zeros(1, dtype='float64')

def myrank():
    return comm.rank

def hostname():
    return host

def mypid():
    return pid

def mysendOneToZero():
    if comm.rank == 1:
        comm.Send([a, 1, MPI.DOUBLE], dest = 0, tag=1)
    if comm.rank == 0:
        comm.Recv(d, source = 1, tag=1)
    return True
