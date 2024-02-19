class Waveform:
    def __init__( self ):
        """
        The waveform in Pulse
        """
        self._I = None
        self._Q = None
        self._single = None

    @property
    def I( self )->str:
        return self._I
    @property
    def Q( self )->str:
        return self._Q
    @property
    def single( self )->str:
        return self._single

myclass = Waveform()
myclass.I = "A"


print(myclass.I)
print(myclass._I)

myclass.A = 10
print(myclass.A)