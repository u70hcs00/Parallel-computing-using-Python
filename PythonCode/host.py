import socket
import os

pid  = os.getpid()
host = socket.gethostname()

def hostname():
    return host

def mypid():
    return pid

