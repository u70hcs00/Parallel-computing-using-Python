# Hello World ! Again
from mpi4py import MPI

comm   = MPI.COMM_WORLD
#myrank = comm.rank
#npes   = comm.size

npes = comm.Get_size()
myrank = comm.Get_rank()

print("Hello world from %i out of %i!"
      %(myrank, npes))
