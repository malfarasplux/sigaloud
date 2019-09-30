
##MIDO 
import mido
import copy
    
def stop_mido(port_is_open):
    global mido_port
    global D_note
    if port_is_open:
        for i in range(len(D_note)):
            mido_port.send(mido.Message('note_off', note = D_note[i], velocity = 80, time = 0))
        mido_port.close()

mido_port = mido.open_output('loopMIDI Port 1')

mido_port.panic()
mido_port.reset()