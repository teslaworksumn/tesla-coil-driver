import mido

class TeslaCoilMidi:
    def __init__(self):
        self.inport = None
        self.outport = None
    def set_input(self, port_name):
        self.inport = mido.open_input(port_name)
    def set_output(self, port_name):
        self.outport = mido.open_output(port_name)
    def passthrough(self):
        if self.inport is not None and self.outport is not None:
            while True:
                try:
                    m = self.inport.receive()
                    self.outport.send(m)
                except KeyboardException:
                    self.outport.reset()
                    break
        else:
            raise TeslaCoilMidiException("An input port is required to use passthrough mode")
    def stop(self):
        self.inport.close()
        self.outport.reset()
        self.outport.close()

class TeslaCoilMidiException(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)