#|%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% TOP OF FILE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%|
#|                                                                             |
#|      FILE NAME:      deviceFunction.py                   [Python 3 module]  |
#|                                                                             |
#|      PROGRAM NAME:   BARC Element Classifier (barc.py)                      |
#|      MODULE NAME:    deviceFunction                                         |
#|                                                                             |
#|      AUTHOR:         Michael P. Frank <mpfrank@sandia.gov>                  |
#|                                                                             |
#|      PROJECT:        LPS/ACS/ACI Project #41, Asynchronous Ballistic        |
#|                      Reversible Computing using Superconducting             |
#|                      Elements (ABRC/SE)                                     |
#|                                                                             |
#|      IMPORTED BY:    (3) deviceType.                                        |
#|      CODE LAYER:     Layer #2 (no cust. imports fr. above layer #1)         |
#|      IMPORTS:        (1) transitionFunction;                                |
#|                      (0) utilities.                                         |
#|                                                                             |
#|-----------------------------------------------------------------------------|
#|                                                                             |
#|      DESCRIPTION:                                                           |
#|      ============                                                           |
#|                                                                             |
#|          An instance of class DeviceFunction defines a device's             |
#|          type (its port alphabets and state set) and also its exact         |
#|          function, defined as a transition function, or map from            |
#|          input syndrome T(S) to output syndrome (S')T'.  Here, T and        |
#|          T' are the incoming and outgoing signal characters, respec-        |
#|          tively, and S and S' are the initial and final states, res-        |
#|          pectively.                                                         |
#|                                                                             |
#|          The main difference between objects of type DeviceFunction         |
#|          and TransitionFunction objects is mainly just that we only         |
#|          keep around and assign IDs to DeviceFunction objects whose         |
#|          transition functions that obey the required conservation           |
#|          and symmetry constraints, and that are non-trivial and             |
#|          atomic.  You can think of transition functions as being            |
#|          lower-level entities.                                              |
#|                                                                             |
#|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv|
"""Defines a class for describing specific device functionalities."""

# Exports:
__all__ = ['DeviceFunction']

# Imports:

    #~~~~~~~~~~~~~~~~~~~~~~~~
    # Imports from layer #0:

from utilities import lookupID
    # Looks up the unique ID# associated with a specifice device function.

    #~~~~~~~~~~~~~~~~~~~~~~~~
    # Imports from layer #1:

from transitionFunction import TransitionFunction

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DeviceFunction:
    """A device function has a device type and a transition function."""
    
        #/~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #|  Instance special methods.
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvv

    def __init__(deviceFunction, deviceType, transitionFunction = None):

        """Initializes the .type and .transitionFunction properties
            of the device function.  If the transition function is
            not specified, it defaults to the identity function."""

        deviceFunction._type         = deviceType

        if transitionFunction is None:
            transitionFunction = TransitionFunction(deviceType)
        
        deviceFunction._transitionFunction = transitionFunction

    def __eq__(thisDeviceFunction, otherDeviceFunction):
    
        """Returns True iff the two device functions are
            equivalent, which means that their device types
            are equivalent and their transition functions
            are equivalent."""
            
        df1 = thisDeviceFunction
        df2 = otherDeviceFunction
        
        return ((df1.type == df2.type) and 
                (df1.transitionFunction == df2.transitionFunction))

    def __hash__(thisDeviceFunction):
        """Returns a consistent hash code for this device function."""
        tdf = thisDeviceFunction
        return hash((tdf.type, tdf.transitionFunction))
    
    def __str__(deviceFunction) -> str:
        """Human-readable string representation of this device function."""
        return (f"{str(deviceFunction.type)}:\n" +
                str(deviceFunction.transitionFunction))

        #/~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #|  Instance public methods:
        #|
        #|      .changesState() [bool] - Returns True if and only if this
        #|          device function changes the device's internal state in
        #|          some input syndrome cases.
        #|
        #|      .changesPort() [bool] - Returns True if and only if this
        #|          device function changes the I/O fluxon's port (between
        #|          input and output) in some input syndrome cases.
        #|
        #|      .hasInactivePort() [bool] - Returns True if and only if
        #|          this device function has at least one port that is
        #|          "inactive," meaning that it always reflects the input
        #|          fluxon and never changes the device's internal state.
        #| 
        #|      .ID() [int] - Returns the unique numeric ID of this device
        #|          function.
        #|
        #|      .showSymmetries() - Displays the symmetry properties of
        #|          this device function in a human-readable way.
        #|
        #|      .symmetricUnder(T) [bool] - Returns True if and only if
        #|          this device function possesses a symmetry to itself
        #|          under the symmetry transformation T.
        #|
        #|      .transformBy(T) [DeviceFunction] - Returns the result of
        #|          applying the symmetry transform T to this device 
        #|          function.
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    def changesState(thisDevFunc) -> bool:
        """Boolean; returns True iff this device function changes the device's
            state in some input cases."""
        return thisDevFunc.transitionFunction.changesState()
        
    def changesPort(thisDevFunc) -> bool:
        """Returns True if this function changes ports in some case."""
        return thisDevFunc.transitionFunction.changesPort()
        
    def hasInactivePort(thisDevFunc):
        """Returns True if the device has an inactive port, that is,
            one that always reflects and doesn't change the state."""
        f = thisDevFunc
        for portIndex in range(f.type.nPorts):
            if not f.transitionFunction.portIsActive(portIndex):
                return True
        return False

    def ID(thisDeviceFunction) -> int:
        """Returns the unique numeric ID of this device function."""
        return lookupID(thisDeviceFunction)

    def showSymmetries(thisDeviceFunction):

        """Displays the symmetry properties of this device function."""

        df = thisDeviceFunction
        print(f"Function #{df.ID()} has the following symmetry properties:")
        rts = df.type.reportableTransforms()
        for rt in rts:
            if df.symmetricUnder(rt):
                if rt.isSelfInverse:
                    print(f"\tIt is self-dual under {rt.sym} {rt.desc}.")
                else:
                    print(f"\tIt is symmetric under {rt.sym} {rt.desc}.")
            else:
                new_df = df.transformBy(rt)
                if rt.isSelfInverse:
                    print(f"\tIt is {rt.sym}-dual to function #{new_df.ID()}")
                else:
                    print(f"\tIt {rt.sym}-transforms to function #{new_df.ID()}")
        print()

    def symmetricUnder(thisDeviceFunction, symmetryTransform) -> bool:
        """Returns True if <thisDeviceFunction> is self-symmetric (i.e.,
            symmetric to itself) under the given <symmetryTransform>."""
        return symmetryTransform.isSymmetric(thisDeviceFunction)
    
    def transformBy(thisDeviceFunction, symmetryTransform):
        """Returns the result of applying the given symmetry transformation
            to this device function."""
        return symmetryTransform(thisDeviceFunction)

        #/~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #|  Instance public properties:
        #|
        #|   .type [DeviceType] - The deviceType for this deviceFunction.
        #|
        #|   .transitionFunction [TransitionFunction] - The device's transition 
        #|      function, or map from inputSyndrome to outputSyndrome for 
        #|      this deviceFunction.
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    @property
    def type(deviceFunction):
        return deviceFunction._type

    @property
    def transitionFunction(deviceFunction):
        return deviceFunction._transitionFunction
    

        #|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #| NOTE: The below methods are to support symmetry transformations.
        #| (But note, the real work is passed through to the transition fn.)
    
    def reverse(deviceFunction):
        """Return the device function that is the direction-reversed 
            version of this device function."""
        df = deviceFunction
        return DeviceFunction(df.type, df.transitionFunction.reverse())

    def negFlux(deviceFunction):
        """Return the device function that is the flux-negated version
            of this device function."""
        df = deviceFunction
        return DeviceFunction(df.type, df.transitionFunction.negFlux())
        
    def negStates(deviceFunction):
        """Return the device function that is the state-exchanged version
            of this device function."""
        df = deviceFunction
        return DeviceFunction(df.type, df.transitionFunction.negStates())
    
    def portExchange(deviceFunction, port1, port2):
        """Return the device function that results from exchanging the
            specified two ports of this device function."""
        df = deviceFunction
        new_tf = df.transitionFunction.portSwap(port1, port2)
        return DeviceFunction(df.type, new_tf)
    
    def portSwap(df, p1, p2):
        """Synonym for the .portExchange() method."""
        return df.portExchange(p1, p2)
    
    def portRotate(deviceFunction, offset):
        """Return the device function that results from rotating this
            device function by the specified numerical offset."""
        df = deviceFunction
        new_tf = df.transitionFunction.portRotate(offset)
        return DeviceFunction(df.type, new_tf)


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% BOTTOM OF FILE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%