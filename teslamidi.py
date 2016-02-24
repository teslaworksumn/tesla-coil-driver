import mido

class TeslaCoilMidi:
    def __init__(self,inport_name,outport_name):
        self.inport = mido.open_input(inport_name)
        self.outport = mido.open_output(outport_name)
        self.outport.reset()
    def passthrough(self):
        while True:
            m = self.inport.receive()
            self.outport.send(m)
    def stop(self):
        self.inport.close()
        self.outport.reset()
        self.outport.close()
