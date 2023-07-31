#|%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% TOP OF FILE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%|
#|                                                                             |
#|      FILE NAME:      syndrome.py                         [Python 3 module]  |
#|                                                                             |
#|      PROGRAM NAME:   BARC Element Classifier (barc)                         |
#|      MODULE NAME:    syndrome                                               |
#|                                                                             |
#|      AUTHOR:         Michael P. Frank <mpfrank@sandia.gov>                  |
#|                                                                             |
#|      PROJECT:        LPS/ACS/ACI Project #41, Asynchronous Ballistic        |
#|                      Reversible Computing using Superconducting             |
#|                      Elements (ABRC/SE)                                     |
#|                                                                             |
#|      IMPORTED BY:    (3) deviceType                                         |
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
#|          This module defines a class Syndrome. An object of class           |
#|          syndrome identifies an I/O syndrome for a device of given          |
#|          dimensions. The I/O syndrome specifies a signal character          |
#|          as well as an internal state.                                      |
#|                                                                             |
#|          Objects of class Syndrome do not by default identify               |
#|          whether they are input or output syndromes. However,               |
#|          subclasses InputSyndrome and OutputSyndrome are also               |
#|          provided for cases where this is needed.                           |
#|                                                                             |
#|                                                                             |
#|      PUBLIC NAMES DEFINED:                                                  |
#|      =====================                                                  |
#|                                                                             |
#|          This module defines the following public names:                    |
#|                                                                             |
#|              Syndrome [class] - Class for I/O syndromes.                    |
#|                                                                             |
#|              InputSyndrome [class] - Subclass of Syndrome.  An              |
#|                  object of this class denotes an input syndrome.            |
#|                                                                             |
#|              OutputSyndrome [class] - Subclass of Syndrome.  An             |
#|                  object of this class denotes an output syndrome.           |
#|                                                                             |
#|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
"""Classes for working with I/O syndromes."""

    #|======================================================================
    #| Module section 0. Exports.                           [code section]
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    
    # This special module attribute gives the list of names that are 'exported'
    # from this module, i.e., that will be imported into an importing module 
    # when that module does 'from <thisModule> import *'.
__all__ = [
        'Syndrome',         # Used by deviceType module.
        'InputSyndrome',    
        'OutputSyndrome'
    ]


    #|======================================================================
    #| Module section 1. Class definitions.                 [code section]
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        #|--------------------------------------------------------------
        #|  Syndrome                                           [class]
        #|
        #|      An object of class Syndrome (for a device of given 
        #|      dimensions) specifies a signal character and a 
        #|      device state.
        #|
        #|      NOTE: Syndrome objects are hashable so that we can 
        #|      use them as dictionary keys. This means that we 
        #|      define custom hash() and == operators for them, so 
        #|      that they are considered identical as long as they 
        #|      have the same signal character and state.
        #|
        #|
        #|  Public properties:
        #|  ------------------
        #|
        #|      .signalCharacter [SignalCharacter] - The character
        #|          of the (arriving or departing) signal.
        #|
        #|      .state [object] - The label of the (initial or final)
        #|          device state, as appropriate.
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

class Syndrome:

    def __init__(syndrome, signalCharacter, state):
    
        syndrome._signalCharacter = signalCharacter
        syndrome._state           = state

    @property
    def flux(thisSyndrome):
        """This property is the net flux of the syndrome."""
        syn = thisSyndrome
        return syn.signalCharacter.flux + syn.state.flux

    @property
    def port(syndrome):
        return syndrome.signalCharacter.portIndex

    @property
    def signalCharacter(syndrome):
        return syndrome._signalCharacter

    @property
    def state(syndrome):
        return syndrome._state

    def asInput(syndrome):
        """Return this syndrome interpreted as an input syndrome."""
        return InputSyndrome(syndrome.signalCharacter, syndrome.state)

    def asOutput(syndrome):
        """Return this syndrome interpreted as an output syndrome."""
        return OutputSyndrome(syndrome.state, syndrome.signalCharacter)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Methods to support symmetry transformations.
    
    def negFlux(thisSyndrome):
        """Returns an I/O syndrome like this one, but all fluxes
            are negated."""
        ts = thisSyndrome
        return Syndrome(ts.signalCharacter.negate(), ts.state.negate())

    def negState(thisSyndrome):
        """Returns an I/O syndrome like this one, but the internal
            state is negated."""
        ts = thisSyndrome
        return Syndrome(ts.signalCharacter, ts.state.negate())

    def portExchange(thisSyndrome, port1, port2):
        ts = thisSyndrome
        return Syndrome(ts.signalCharacter.portSwap(port1, port2), ts.state)

    def portSwap(thisSyndrome, port1, port2):
        return thisSyndrome.portExchange(port1, port2)

    def portRotate(thisSyndrome, offset):
        ts = thisSyndrome
        return Syndrome(ts.signalCharacter.portRotate(offset), ts.state)
        
    def stateSwap(thisSyndrome):
        ts = thisSyndrome
        return Syndrome(ts.signalCharacter, ts.state.swap())

    def __eq__(thisSyndrome, thatSyndrome):
        ts1 = thisSyndrome
        ts2 = thatSyndrome
        return ((ts1.signalCharacter == ts2.signalCharacter) and
                (ts1.state == ts2.state))
    
    def __lt__(thisSyndrome, thatSyndrome):
        """Used for canonicalizing transition function order; 
            facilitates transition function equality testing."""
        ts1 = thisSyndrome
        ts2 = thatSyndrome
        return ((ts1.signalCharacter < ts2.signalCharacter) or
                ((ts1.signalCharacter == ts2.signalCharacter) and
                 (ts1.state < ts2.state)))

    def __hash__(syndrome):
        return hash((syndrome.signalCharacter, syndrome.state))

class InputSyndrome(Syndrome):

    def __str__(this):
    
        sc = this.signalCharacter
        st = this.state
    
        return f"{sc.inStr()}({str(st)})"
    
        #return "%s>(%s)" % (this.signalCharacter, this.state)

class OutputSyndrome(Syndrome):

        # Reverse argument order in initializer:
        #   OutputSyndrome(state, sigChar)

    def __init__(syndrome, state, signalCharacter):
        super().__init__(signalCharacter, state)

    def __str__(this):
    
        sc = this.signalCharacter
        st = this.state
    
        return f"({str(st)}){sc.outStr()}"
    
        #return "(%s)>%s" % (this.state, this.signalCharacter)

        
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% BOTTOM OF FILE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%