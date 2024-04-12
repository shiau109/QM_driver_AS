
from abc import ABC, abstractmethod

from qm.qua import *
from qualang_tools.units import unit
u = unit(coerce_to_integer=True)
class Initializer( ABC ):
    @abstractmethod
    def macro( self ):
        pass

class Thermalization( Initializer ):
    def __init__( self ):
        self.thermalization_time = 1
    def macro(self):
        cc_time = (self.thermalization_time/4)*u.MHz
        wait( cc_time )

from exp.RO_macros import multiRO_measurement

class ActiveReset( Initializer ):
    def __init__( self ):

        self.max_tries = 1
        self.resonators = []
        self.xy_controls = []
        self.threshold = []
        self.iqdata_stream = ()

    def macro( self, iqdata_stream ):
        
        Ig = iqdata_stream[0]
        if Ig is None:
            Ig = declare(fixed)
        if ( self.max_tries < 1) or (not float(self.max_tries).is_integer()):
            raise Exception("max_count must be an integer >= 1.")
        # Initialize Ig to be > threshold
        assign(Ig, self.threshold + 2**-28)
        # Number of tries for active reset
        counter = declare(int)
        # Reset the number of tries
        assign(counter, 0)

        # # Perform active feedback
        # align(qubit, resonator)
        # Use a while loop and counter for other protocols and tests
        with while_((Ig > self.threshold) & (counter < self.max_tries)):
            # Measure the resonator
            multiRO_measurement( self.resonators,  )
            # Play a pi pulse to get back to the ground state
            for xy_name, thr, i in zip(self.xy_controls,self.threshold, Ig):
                play("x180", xy_name, condition=(i > thr))
            # Increment the number of tries
            assign(counter, counter + 1)
