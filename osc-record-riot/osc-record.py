#!/usr/bin/env python
# -*- coding: utf-8 -*-

import liblo
import sys
from datetime import datetime as dt
import datetime
import time

num_devices = 10

# config for listening
listeningPort = 8888

# now method
def now():
	return dt.today()

# start time
#print '%s,INFO:osc-record started.\n' % now()

# create server, listening on given port
try:
    server = liblo.Server(listeningPort)
except liblo.ServerError, err:
    print str(err)
    sys.exit()

# callback functions 
def n_callback(path):
    print '%s,%s' % (now(), path)

def f_callback(path, args):
	print '%s,%s %f' % (now(), path, args[0])

def fffff_callback(path, args):
    print '%s,%s %f,%f,%f,%f,%f' % (now(), path, args[0], args[1], args[2], args[3], args[4])

def riot0_callback(path, args):
    print '%s,%s,%s' % (now(), path, ','.join(map(str, args)))

def riot1_callback(path, args):
    print '%s,%s,%s' % (now(), path, ','.join(map(str, args)))

def fallback(path, args, types, src):
    print "got unknown message '%s' from '%s'" % (path, src.get_url())
    for a, t in zip(args, types):
        print "argument of type '%s': %s" % (t, a)

# register method taking an int and a float
server.add_method("/pedal", None, n_callback)
server.add_method("/speed", 'f', f_callback)
server.add_method("/wek/outputs", 'fffff', fffff_callback)

#for i in range(num_devices):
#    addr = '/%i/raw' % i
#    server.add_method(addr, 'ffffffffffffffffffffff', riot_callback)
server.add_method('/0/raw', 'ffffffffffffffffffffff', riot0_callback)
server.add_method('/1/raw', 'ffffffffffffffffffffff', riot1_callback)
#server.add_method("/0/raw", 'ffffffffffffffffffffff', riot_callback)

# register a fallback for unhandled messages
server.add_method(None, None, fallback)

# loop and dispatch messages every 100ms
time.sleep(1)
while True:
    server.recv(5)

