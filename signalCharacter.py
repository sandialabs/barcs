#|%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% TOP OF FILE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%|
#|                                                                             |
#|      FILE NAME:      signalCharacter.py                  [Python 3 module]  |
#|                                                                             |
#|      PROGRAM NAME:   BARC Element Classifier (barc)                         |
#|      MODULE NAME:    signalCharacter                                        |
#|                                                                             |
#|      AUTHOR:         Michael P. Frank <mpfrank@sandia.gov>                  |
#|                                                                             |
#|      PROJECT:        LPS/ACS/ACI Project #41, Asynchronous Ballistic        |
#|                      Reversible Computing using Superconducting             |
#|                      Elements (ABRC/SE)                                     |
#|                                                                             |
#|      IMPORTED BY:    (3) deviceType.                                        |
#|      CODE LAYER:     Layer #0 (no custom imports).                          |
#|                                                                             |
#|                                                                             |
#|      FILE HISTORY:                                                          |
#|      =============                                                          |
#|          2018 Oct. 16th  - Initial version, used to count 1- and 2-port     |
#|                              functions..                                    |
#|          2022 Jan. 5th   - Starting code review/cleanup to prep. for        |
#|                              extension for element classification task.     |
#|                                                                             |
#|-----------------------------------------------------------------------------+
#|                                                                             |
#|      DESCRIPTION:                                                           |
#|      ============                                                           |
#|                                                                             |
#|          This module defines the class SignalCharacter. An object of        |
#|          class SignalCharacter specifies (for a device type with a          |
#|          specified number N of ports) the information characterizing        |
#|          an I/O event, where this includes the port index in the set        |
#|          [0, ..., N), and also the pulse type.                              |
#|                                                                             |
#|          Currently, the signalCharacter objects themselves do not           |
#|          specifying whether they are representing input events or           |
#|          output events (although it may be clear from context).             |
#|                                                                             |
#|                                                                             |
#|      PUBLIC NAMES DEFINED:                                                  |
#|      =====================                                                  |
#|                                                                             |
#|          This module defines the following public names:                    |
#|                                                                             |
#|              * SignalCharacter                                   [class]    |
#|                                                                             |
#|                  Class of signal characters.                                |
#|                                                                             |
#|                                                                             |
#|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv|

    #|======================================================================
    #| Module section 0. Exports.                           [code section]
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    
    # This special module attribute gives the list of names that are 'exported'
    # from this module, i.e., that will be imported into an importing module 
    # when that module does 'from <thisModule> import *'.
__all__ = [
        'SignalCharacter'     # Used by deviceType module.
    ]


    #|======================================================================
    #| Module section 1.  Class definitions.                [code section]
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        #|--------------------------------------------------------------
        #|  SignalCharacter                                    [class]
        #|
        #|      An object of class SignalCharacter characterizes
        #|      a pulse incident to a device. This may be either
        #|      an input (incoming) pulse, or an output (outgoing)
        #|      pulse. Properties of a signal character include
        #|      its port index and pulse type. Together, these 
        #|      define the signal character (that is, signal 
        #|      characters with the same port index and pulse type
        #|      are considered equal).
        #|
        #|
        #|  Public properties:
        #|  ------------------
        #|
        #|      .portIndex [non-negative integer] - For an N-port
        #|          device, this is the index i, where 0 <= i < N, 
        #|          of the port specified by this signal character.
        #|
        #|      .pulseType [PulseType] - An object specifying the 
        #|          type of pulse that is entering or leaving.
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

class SignalCharacter:

    def __init__(signalCharacter, portIndex, pulseType, characterClass):
    
        signalCharacter._portIndex = portIndex
        signalCharacter._pulseType = pulseType
        
        signalCharacter._characterClass = characterClass

    @property
    def flux(thisSigChar):
        """This property is the flux of the signal character."""
        return thisSigChar.pulseType.flux

    @property
    def isUnary(sigChar):
        return sigChar.characterClass.isUnary

    @property
    def characterClass(sigChar):
        return sigChar._characterClass

    @property
    def portIndex(sigChar):
        return sigChar._portIndex

    @property
    def pulseType(sigChar):
        return sigChar._pulseType

    def negate(thisSigChar):
        sc = thisSigChar
        return SignalCharacter(sc.portIndex, sc.pulseType.negate, sc.characterClass)

    def portSwap(sigChar, port1, port2):
        """NOTE: This only makes sense if the pulse alphabets are the same."""
        charClass = sigChar.characterClass
        assert(charClass.isUniform)
        if sigChar.portIndex == port1:
            return SignalCharacter(port2, sigChar.pulseType, charClass)
        elif sigChar.portIndex == port2:
            return SignalCharacter(port1, sigChar.pulseType, charClass)
        else:
            return sigChar      # No change.
    
    def portRotate(sigChar, offset):
        """NOTE: This only makes sense if the pulse alphabets are the same."""
        charClass = sigChar.characterClass
        assert(charClass.isUniform)
        newPort = (sigChar.portIndex + offset)%charClass.nPorts
        return SignalCharacter(newPort, sigChar.pulseType, charClass)

    def inStr(sigChar):
        if sigChar.isUnary:
                # For unary alphabets, omit the pulse type
            return f"{sigChar.portIndex+1}"
        else:
            return f"{str(sigChar.pulseType)}>{sigChar.portIndex+1}"

    def outStr(sigChar):
        if sigChar.isUnary:
                # For unary alphabets, omit the pulse type
            return f"{sigChar.portIndex+1}"
        else:
            return f"{sigChar.portIndex+1}>{str(sigChar.pulseType)}"

    def __str__(sigChar):
        return f"{str(sigChar.pulseType)}@P{sigChar.portIndex+1}"
        #return "p%s@P%s" % (sigChar.pulseType, sigChar.portIndex)
        
    def __eq__(thisSigChar, thatSigChar):
        sc1 = thisSigChar
        sc2 = thatSigChar
        return ((sc1.portIndex == sc2.portIndex) and
                (sc1.pulseType == sc2.pulseType))

    def __lt__(thisSigChar, thatSigChar):
        sc1 = thisSigChar
        sc2 = thatSigChar
        return ((sc1.portIndex < sc2.portIndex) or
                ((sc1.portIndex == sc2.portIndex) and
                 (sc1.pulseType < sc2.pulseType)))

    def __hash__(sigChar):
        return hash((sigChar.portIndex, sigChar.pulseType))


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% BOTTOM OF FILE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%