#|%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% TOP OF FILE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%|
#|                                                                             |
#|      FILE NAME:      transitionFunction.py               [Python 3 module]  |
#|                                                                             |
#|      PROGRAM NAME:   BARC Element Classifier (barc)                         |
#|      MODULE NAME:    transitionFunction                                     |
#|                                                                             |
#|      AUTHOR:         Michael P. Frank <mpfrank@sandia.gov>                  |
#|                                                                             |
#|      PROJECT:        LPS/ACS/ACI Project #41, Asynchronous Ballistic        |
#|                      Reversible Computing using Superconducting             |
#|                      Elements (ABRC/SE)                                     |
#|                                                                             |
#|      IMPORTED BY:    (2) deviceFunction                                     |
#|      CODE LAYER:     Layer #1 (no imports from above layer #0).       	   |
#|      IMPORTS:        (0) utilities.                                         |
#|                                                                             |
#|-----------------------------------------------------------------------------+
#|                                                                             |
#|      DESCRIPTION:                                                           |
#|      ============                                                           |
#|                                                                             |
#|          This module defines a class called TransitionFunction.             |
#|          An object that is an instance of class TransitionFunction          |
#|          represents a specific transition function (or mapping              |
#|          from input syndromes to output syndromes) that a device            |
#|          may have.  The distinction between the DeviceFunction and          |
#|          TransitionFunction classes is a little bit subtle, but it          |
#|          is essentially that a DeviceFunction is characterized by           |
#|          having a TransitionFunction that has already been "vetted"         |
#|          in the sense of having been confirmed to represent a non-          |
#|          trivial, atomic behavioral primitive. So a raw transition          |
#|          function is conceptually a slightly lower-level entity.            |
#|                                                                             |
#|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv|
"""Support for raw (low-level) device transition functions."""

# Imports.
from utilities import hashdict      # Returns the hash of a dictionary.

    #/~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #|  TransitionFunction                              [module public class]
    #|
    #|      An object that is an instance of class TransitionFunction is a
    #|      specific map from input syndromes to output syndromes for a 
    #|      particular device type.  For now, all transition functions are 
    #|      assumed to be total injective operations on the set of I/O
    #|      syndromes, thus also bijective (reversible).  In the future, 
    #|      we may further expand upon this concept to encompass condition-
    #|      ally reversible functions, partial functions, stochastic maps, 
    #|      and perhaps even quantum (unitary) transition relations.
    #|
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

class TransitionFunction:
    """For our present purposes, a transition function is a bijection on the 
        set of I/O syndromes for a given device type."""

    # Instance private data members:
    #   ._deviceType - The type of device that this transition function is for.
    #   ._ioMap - The map implemented by this transition function.  Defaults to
    #               an identity map over all I/O syndromes.

    def __init__(transitionFunction, deviceType, ioMap = None):
    
        transitionFunction._deviceType = deviceType

            # If no map from input to output syndromes was provided,
            # then default to the identity map.
        
        if ioMap == None:
            ioMap = dict()
            for syndrome in deviceType.syndromes():
                ioMap[syndrome.asInput()] = syndrome.asOutput()
                
        transitionFunction._ioMap = ioMap

    # Instance public properties:

    @property
    def deviceType(transitionFunction):
        return transitionFunction._deviceType

    @property
    def ioMap(transitionFunction):
        return transitionFunction._ioMap

    # Instance public methods:

    def conservesFlux(thisTransFunc):
        """Boolean; returns True iff this transition function conserves flux."""
        tf = thisTransFunc
        
        ioMap = tf.ioMap
        for (inSyn,outSyn) in ioMap.items():
            inFlux = inSyn.flux
            outFlux = outSyn.flux
            if inFlux != outFlux:
                return False        # Nope; flux isn't conserved.

        # If we get here, then flux is conserved.
        return True

    def changesState(transFunc):
        """Return True iff the transition function changes the state in any case."""
        doesIt = False
        ioMap = transFunc.ioMap
        for (inSyn,outSyn) in ioMap.items():
            if not inSyn.state == outSyn.state:
                doesIt = True
        return doesIt

    def changesPort(transFunc):
        """Return True iff the transition function changes the I/O port in any case.
            (Otherwise, if it's flux-neutral, it's just a set of reflectors with
            no way to do state readout..)"""
        doesIt = False
        ioMap = transFunc.ioMap
        for (inSyn,outSyn) in ioMap.items():
            if not inSyn.port == outSyn.port:
                doesIt = True
        return doesIt
        
    def portIsActive(transFunc, port):
        """Return True if the given port is active, meaning that it either changes
            or causes the state to change. If it does neither, then it's just a 
            simple reflector and is unrelated to the rest of the device."""
        isActive = False
        ioMap = transFunc.ioMap
        for (inSyn,outSyn) in ioMap.items():
            if inSyn.port == port:
                if not (outSyn.port == port):
                    isActive = True
                if not (inSyn.state == outSyn.state):
                    isActive = True
        return isActive
        
    def applyTo(transitionFunction, syndrone):
        """Invoked on a transition function <tf>, with a single argument
            that is an I/O syndrome <s>, interpreted as an input syndrome,
            this returns the result of applying <tf> to <s>; i.e., the 
            corresponding output syndrome.
            
            Concise alternate syntax: <tf>(<s>)."""
        return transitionFunction.ioMap[syndrome.asInput()]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # The below methods are to support symmetry transformations.
    
    def reverse(thisTransitionFunction):
    
        """Returns a transition function that is the reverse of this one;
            that is, its I/O map is the inverse function to our I/O map."""
        
        tf = thisTransitionFunction

        devType = tf.deviceType
        ioMap = tf.ioMap

        oiMap = dict()
        
        for (inputSyndrome, outputSyndrome) in ioMap.items():
        
                # Flip syndrome types.
            outAsIn = outputSyndrome.asInput()
            inAsOut = inputSyndrome.asOutput()
        
            oiMap[outAsIn] = inAsOut
            
        return TransitionFunction(devType, oiMap)
    
    def negStates(thisTransitionFunction):
    
        """Returns a transition function that is the same as this one,
            except that the (assumed negatable) states are changed
            to their negations."""
    
        tf = thisTransitionFunction

        devType = tf.deviceType
        ioMap = tf.ioMap
        
        new_ioMap = dict()
        
        for (inputSyndrome, outputSyndrome) in ioMap.items():
            #print(f"Negating state in {inputSyndrome} -> {outputSyndrome}...")
            new_ioMap[inputSyndrome.negState().asInput()] = outputSyndrome.negState().asOutput()
            
        return TransitionFunction(devType, new_ioMap)
    
    def negFlux(thisTransitionFunction):
    
        """Returns a transition function that is the same as this one,
            except that the (assumed polarized) pulse types are changed
            to their negations; and if the state set is negatable,
            then the states are also changed to their negations."""
    
        tf = thisTransitionFunction

        devType = tf.deviceType
        ioMap = tf.ioMap
        
        new_ioMap = dict()
        
        for (inputSyndrome, outputSyndrome) in ioMap.items():
            new_ioMap[inputSyndrome.negFlux().asInput()] = outputSyndrome.negFlux().asOutput()
            
        return TransitionFunction(devType, new_ioMap)
    
    def portSwap(thisTransitionFunction, port1, port2):
    
        """Returns a transition function that is the same as this one,
            except that the two given port indices are exchanged."""

        tf = thisTransitionFunction

        devType = tf.deviceType
        ioMap = tf.ioMap
        
        new_ioMap = dict()
        
        for (inputSyndrome, outputSyndrome) in ioMap.items():
        
            new_is = inputSyndrome.portSwap(port1, port2).asInput()
            new_os = outputSyndrome.portSwap(port1, port2).asOutput()
        
            new_ioMap[new_is] = new_os
            
        return TransitionFunction(devType, new_ioMap)
    
    def portRotate(thisTransitionFunction, offset):
    
        """Returns a transition function that is the same as this one,
            except that the port indices are rotated by the given
            offset (an integer)."""

        tf = thisTransitionFunction

        devType = tf.deviceType
        ioMap = tf.ioMap
        
        new_ioMap = dict()
        
        for (inputSyndrome, outputSyndrome) in ioMap.items():
        
            new_is = inputSyndrome.portRotate(offset).asInput()
            new_os = outputSyndrome.portRotate(offset).asOutput()
        
            new_ioMap[new_is] = new_os
            
        return TransitionFunction(devType, new_ioMap)

    # Instance special methods:

    def __call__(transitionFunction, syndrone):
        return transitionFunction.applyTo(syndrome)

    def __str__(transitionFunction):
        string = ""
        for inSyn, outSyn in transitionFunction.ioMap.items():
            string += "\t%s -> %s\n" % (inSyn, outSyn)
        return string
    
    def __hash__(transitionFunction):
        return hash((transitionFunction.deviceType,hashdict(transitionFunction.ioMap)))
    
    # Commented this out b/c it's superseded by the later definition anyway
    #def __eq__(thisTransitionFunction, otherTransitionFunction):
    #
    #    """Returns True if the two transition functions are equivalent,
    #        which means, they have the same device type and the same
    #        I/O map."""
    # 
    #    tf1 = thisTransitionFunction
    #    tf2 = otherTransitionFunction
    #    
    #    return ((tf1.deviceType == tf2.deviceType) and
    #            (tf1.ioMap == tf2.ioMap))

    def __eq__(thisTransitionFunction, otherTransitionFunction):
        
        tf1 = thisTransitionFunction
        tf2 = otherTransitionFunction
        
            # Two transition functions compare equal if and only if
            # they map each input syndrome to the same output syndrome.
            # (Note this also implies that the device types match too.)
        for (in_syn, out_syn) in tf1.ioMap.items():
            if not tf2.ioMap[in_syn] == out_syn:
                return False
                
        return True


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% BOTTOM OF FILE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%