from tornado import websocket, web, ioloop
import thread
import json
import signal
import sys
import numpy
import time
import sys, traceback, os
from bitalino import *
from os.path import expanduser
import threading

cl = []
tflag = True

def tostring(data):
    """
    :param data: object to be converted into a JSON-compatible `str`
    :type data: any
    :return: JSON-compatible `str` version of `data`
    
    Converts `data` from its native data type to a JSON-compatible `str`.
    """
    dtype=type(data).__name__
    if dtype=='ndarray':
        if numpy.shape(data)!=(): data=data.tolist() # data=list(data)
        else: data='"'+data.tostring()+'"'
    elif dtype=='dict' or dtype=='tuple':
        try: data=json.dumps(data)
        except: pass
    elif dtype=='NoneType':
        data=''
    elif dtype=='str' or dtype=='unicode':
        data=json.dumps(data)
    
    return str(data)


class SocketHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        global tflag
        if self not in cl:
            cl.append(self)
        print("CONNECTED")
        tflag = True

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        if self in cl:
            cl.remove(self)
        print("DISCONNECTED")

def signal_handler(signal, frame):
    print('TERMINATED')
    sys.exit(0)

def BITalino_handler(mac_addr, ch_mask, srate, labels):
    #labels = ["'nSeq'", "'I1'", "'I2'", "'O1'", "'O2'", "'A1'", "'A2'", "'A3'", "'A4'", "'A5'", "'A6'"]
    ch_mask = numpy.array(ch_mask)-1
    try:
        print(mac_addr)
        device=BITalino(mac_addr)
        print(ch_mask)
        print(srate)
        device.start(srate, ch_mask)
        cols = numpy.arange(len(ch_mask)+5)
        while (1):
            data=device.read(250)
            res = "{"
            for i in cols:
                idx = i
                if (i>4): idx=ch_mask[i-5]+5
                res += '"'+labels[idx]+'":'+tostring(data[:,i])+','
            res = res[:-1]+"}"
            if len(cl)>0: cl[-1].write_message(res)
    except:
        traceback.print_exc()
        os._exit(0)


def printHi():
    global tflag
    tflag = True

def BITalino_simulate(mac_addr, ch_mask, srate, labels):
    #labels = ["'nSeq'", "'I1'", "'I2'", "'O1'", "'O2'", "'A1'", "'A2'", "'A3'", "'A4'", "'A5'", "'A6'"]
    global tflag
    ch_mask = numpy.array(ch_mask)-1
    DATA = numpy.loadtxt('D:/github/wring/PZT_3_2.txt')
    dsrate = 1000
    buffer_size = 250
    xi = 0
    xf = buffer_size
    data = DATA[xi:xf,:]
    xi = xf
    maxdata = 361000
    firstcall = True
    update_rate = 1.0*buffer_size/srate
#    update_rate = 0.250
#    update_rate = 2

    print(update_rate)
    try:
        print("ch_mask: ", ch_mask)
        print("srate: ", srate)
        print("labels:", labels)
        cols = numpy.arange(len(ch_mask)+5)
        print("cols:", cols)
        while (1):
            # Create timer
            if firstcall or tflag:
                threading.Timer(update_rate, printHi).start()

                tflag = False
                firstcall = False

                data = numpy.roll(data, -buffer_size, axis = 0)
                xf = (xf % maxdata) + buffer_size
                data_buffer = DATA[xi:xf,:]
            
                xi = xf % maxdata
                data[-buffer_size:,:] = data_buffer



                res = "{"
                for i in cols:
                    idx = i
                    if (i>4): idx=ch_mask[i-5]+1
                    res += '"'+labels[idx]+'":'+tostring(data[:,i])+','
                res = res[:-1]+"}"
                if len(cl)>0: cl[-1].write_message(res)
    except:
        traceback.print_exc()
        os._exit(0)            


app = web.Application([(r'/', SocketHandler)])

if __name__ == '__main__':
    home = expanduser("~") + '/ServerBIT'
    print(home)
    try:
        with open(home+'/config.json') as data_file:
            config = json.load(data_file)
            print(config)
    except:
        with open('config.json') as data_file:
            config = json.load(data_file)
        os.mkdir(home)
        with open(home+'/config.json', 'w') as outfile:
            json.dump(config, outfile)
    signal.signal(signal.SIGINT, signal_handler)
    app.listen(config['port'])
    print('LISTENING')
#    thread.start_new_thread(BITalino_handler, (config['device'],config['channels'],config['sampling_rate'], config['labels']))
    thread.start_new_thread(BITalino_simulate, (config['device'],config['channels'],config['sampling_rate'], config['labels']))
    ioloop.IOLoop.instance().start()
    
