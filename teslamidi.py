import mido

class TeslaCoilMidi:
    def __init__(self):
        self.inport = None
        self.outport = None
    def __init__(self,inport_name,outport_name):
        self.inport = mido.open_input(inport_name)
        self.outport = mido.open_output(outport_name)
        self.outport.reset()
    def set_input(self, port_name):
        self.inport = mido.open_input(port_name)
    def set_output(self, port_name):
        self.outport = mido.open_output(port_name)
    def passthrough(self):
        if self.inport is not None and self.outport is not None:
            while True:
                m = self.inport.receive()
                self.outport.send(m)
        else:
            raise TeslaCoilMidiException("An input port is required to use passthrough mode")
    def stop(self):
        self.inport.close()
        self.outport.reset()
        self.outport.close()

class TeslaCoilMidiException(Exception):
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        super(ValidationError, self).__init__(message)