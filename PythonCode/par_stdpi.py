"""Calculate statistics on the digits of pi in parallel.

This program uses the functions in :file:`pidigits.py` to calculate
the frequencies of 2 digit sequences in the digits of pi. The
results are plotted using matplotlib.

To run, text files from http://www.super-computing.org/
must be installed in the working directory of the IPython engines.
The actual filenames to be used can be set with the ``filestring``
variable below.

The dataset we have been using for this is the 200 million digit one here:
ftp://pi.super-computing.org/.2/pi200m/

and the files used will be downloaded if they are not in the working directory
of the IPython engines.
"""
from __future__ import print_function

from ipyparallel import Client
from matplotlib import pyplot as plt
import numpy as np
from stdpidigits import *
from timeit import default_timer as clock
import math 
import sys
# Files with digits of pi (10m digits each)
filestring = 'pi1000m.ascii.%(i)02dof100'
files = [filestring % {'i':i} for i in range(1,21)]

# Connect to the IPython cluster
c = Client()
c[:].run('stdpidigits.py')

# the number of engines
n = len(c)
id0 = c.ids[0]
v = c[:]
v.block=True
# fetch the pi-files
print("downloading %i files of pi"%n)
v.map(fetch_pi_file, files[:n])
print("done")


LL = np.linspace(0, 99, num = 100)
# Run 10m digits on 1 engine
t1 = clock()
freqs10m = c[id0].apply_sync(compute_two_digit_freqs, files[0])

Sum = freqs10m*LL
avg10m = Sum.sum()/freqs10m.sum()

stdL = (LL - avg10m) ** 2
Stdsum = freqs10m*stdL
std10m = math.sqrt(Stdsum.sum()/freqs10m.sum())

t2 = clock()

digits_per_second1 = 10.0e6/(t2-t1)
print("Digits per second (1 core, 10m digits):   ", digits_per_second1)
print("average of 10m digits of pi = ", avg10m)
print("Std of 10m digits of pi = ", std10m)


# Run n*10m digits on all engines
t1 = clock()
freqs_all = v.map(compute_two_digit_freqs, files[:n])
freqs150m = reduce_freqs(freqs_all)

Sum = freqs150m*np.linspace(0, 99, num = 100)
avg150m = Sum.sum()/freqs150m.sum()

stdL = (LL - avg150m) ** 2
Stdsum = freqs150m*stdL
std150m = math.sqrt(Stdsum.sum()/freqs150m.sum())

t2 = clock()
digits_per_second8 = n*10.0e6/(t2-t1)
print("Digits per second (%i engines, %i0m digits): "%(n,n), digits_per_second8)
print("average of %i0m digits of pi = "%n, avg150m)
print("Std of %i0m digits of pi = "%n, std150m)


print("Speedup: ", digits_per_second8/digits_per_second1)

plot_two_digit_freqs(freqs150m)
plt.title("2 digit sequences in %i0m digits of pi"%n)
plt.show()

