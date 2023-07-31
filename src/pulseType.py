#|%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% TOP OF FILE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%|
#|                                                                             |
#|      FILE NAME:      pulseType.py                        [Python 3 module]  |
#|                                                                             |
#|      PROGRAM NAME:   BARC Element Classifier (barc)                         |
#|      MODULE NAME:    pulseType                                              |
#|                                                                             |
#|      AUTHOR:         Michael P. Frank <mpfrank@sandia.gov>                  |
#|                                                                             |
#|      PROJECT:        LPS/ACS/ACI Project #41, Asynchronous Ballistic        |
#|                      Reversible Computing using Superconducting             |
#|                      Elements (ABRC/SE)                                     |
#|                                                                             |
#|      IMPORTED BY:    (3) deviceType.                                        |
#|      CODE LAYER:     Layer #0 (no custom imports).                          |
#|      IMPORTS:        (0) utilities.                                         |
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
#|          This module defines a class PulseType. An object of class          |
#|          PulseType denotes a specific pulse type within a given             |
#|          pulse-type alphabet.                                               |
#|                                                                             |
#|                                                                             |
#|      PUBLIC NAMES DEFINED:                                                  |
#|      =====================                                                  |
#|                                                                             |
#|          This module defines the following public names:                    |
#|                                                                             |
#|              * PulseType                                         [class]    |
#|                                                                             |
#|                  Class of pulse types.                                      |
#|                                                                             |
#|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv|

    #|======================================================================
    #| Module section 0. Exports.                           [code section]
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    
# This special module attribute gives the list of names that are 'exported'
# from this module, i.e., that will be imported into an importing module 
# when that module does 'from <thisModule> import *'.
__all__ = [
        'PulseType'     # Used by deviceType module.
    ]

    #|======================================================================
    #| Module section 1. Imports.                           [code section]
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    
from utilities import flux      
    # This is a simple helper function to convert symbols to flux values.

    #|======================================================================
    #| Module section 2. Class definitions.                 [code section]
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        #|--------------------------------------------------------------
        #|  PulseType                                          [class]
        #|
        #|      An object of class PulseType represents a specific
        #|      type of pulse. In the context of BARCS, this is
        #|      a fluxon polarity (-1 or +1).
        #|
        #|
        #|  Public properties:
        #|  ------------------
        #|
        #|      PulseType objects have the following properties:
        #|
        #|          .alphabet [PulseAlphaBet] - The underlying
        #|              pulse type symbol alphabet from which
        #|              this specific pulse type was selected.
        #|
        #|          .symbol [object] - The symbol representing
        #|              this specific pulse type. This is used as 
        #|              the printable representation of the pulse 
        #|              type.
        #|
        #|          .index [non-negative integer] - The index of
        #|              this specific pulse type's symbol within 
        #|              its pulse alphabet.
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

class PulseType:

    def __init__(pulseType, pulseAlphabet, symbol):
        pulseType._alphabet = pulseAlphabet
        pulseType._symbol = symbol

            # Identify this pulseType's index.
        
        for index in range(pulseAlphabet.arity):
            if pulseAlphabet.symbols[index] == symbol:
                pulseType._index = index
        if not hasattr(pulseType, '_index'):
            # should report error here
            pass

    @property
    def flux(thisPulseType):
        return flux(thisPulseType.symbol)

    @property
    def negate(thisPulseType):
        pt = thisPulseType
        pa = pt.alphabet
        return PulseType(pa, pa.negate(pt.symbol))

    @property
    def alphabet(pulseType):
        return pulseType._alphabet

    @property
    def symbol(pulseType):
        return pulseType._symbol

    # Not currently used.
    @property
    def index(pulseType):
        return pulseType._index

    def __str__(pulseType):
        return str(pulseType._symbol)

    def __eq__(thisPulseType, thatPulseType):
        pt1 = thisPulseType
        pt2 = thatPulseType
        return pt1.symbol == pt2.symbol
    
    def __lt__(thisPulseType, thatPulseType):
        pt1 = thisPulseType
        pt2 = thatPulseType
        return pt1.symbol < pt2.symbol
    
    def __hash__(pulseType):
        return hash(pulseType.symbol)


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% BOTTOM OF FILE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%