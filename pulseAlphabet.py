#|%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% TOP OF FILE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#|                                                                             |
#|      FILE NAME:      pulseAlphabet.py                    [Python 3 module]  |
#|                                                                             |
#|      PROGRAM NAME:   BARC Element Classifier (barc)                         |
#|      MODULE NAME:    pulseAlphabet                                          |
#|                                                                             |
#|      AUTHOR:         Michael P. Frank <mpfrank@sandia.gov>                  |
#|                                                                             |
#|      PROJECT:        LPS/ACS/ACI Project #41, Asynchronous Ballistic        |
#|                      Reversible Computing using Superconducting             |
#|                      Elements (ABRC/SE)                                     |
#|                                                                             |
#|      IMPORTED BY:    (3) deviceType.                                        |
#|      CODE LAYER:     Layer #1 (no custom imports from above layer #0)       |
#|      IMPORTS:        (0) utilities.                                         |
#|
#|                                                                             |
#|      FILE HISTORY:                                                          |
#|      =============                                                          |
#|          2018 Oct. 16th  - Initial version, used to count 1- and 2-port     |
#|                              functions.                                     |
#|          2022 Jan. 4th   - Starting code review/cleanup to prep. for        |
#|                              extension for element classification task.     |
#|                                                                             |
#|-----------------------------------------------------------------------------|
#|                                                                             |
#|      DESCRIPTION:                                                           |
#|      ============                                                           |
#|                                                                             |
#|          This module defines various classes and objects for defining       |
#|          particular sets of pulse types with associated symbolic            |
#|          representations. We call these sets "alphabets," by analogy        |
#|          with the ordered set of letters of a written language.             |
#|                                                                             |
#|          In the BARC framework, the significance of a pulse alphabet is     |
#|          that a specific I/O port of a specific device type may be          |
#|          declared to use a specific pulse alphabet. This means that the     |
#|          interconnect line connected to that I/O port must not supply       |
#|          pulses of any other types to that I/O port, and must support       |
#|          all of those pulse types, in case they're emitted by the port.     |
#|                                                                             |
#|          The symbolic representations of pulse types can in general be      |
#|          any Python objects, but in particular alphabets, the objects       |
#|          may be meaningful, for example, specifying the flux charge of      |
#|          a pulse.                                                           |
#|                                                                             |
#|                                                                             |
#|      PUBLIC NAMES DEFINED:                                                  |
#|      =====================                                                  |
#|                                                                             |
#|          This module defines & exports the following public names:          |
#|                                                                             |
#|          Module public classes:                                             |
#|          ----------------------                                             |
#|                                                                             |
#|              PulseAlphabet [class] - This is the base class for all         |
#|                  pulse-type alphabets.                                      |
#|                                                                             |
#|              UnaryPulseAlphabet [class] - Class for pulse alphabets         |
#|                  with only a single pulse type.                             |
#|                                                                             |
#|              PositiveUnaryPulseAlphabet [class] - Class for a pulse         |
#|                  alphabet containing only a +1 flux quantum pulse.          |
#|                                                                             |
#|              BinaryPulseAlphabet [class] - Class for pulse alphbets         |
#|                  with exactly two pulse types.                              |
#|                                                                             |
#|              SymmetricBinaryPulseAlphabet [class] - Class for a             |
#|                  pulse alphabet with pulse types -1, +1 (these              |
#|                  could correspond to flux charges, in SFQ units).           |
#|                                                                             |
#|                                                                             |
#|          Module public globals:                                             |
#|          ----------------------                                             |
#|                                                                             |
#|              thePositiveUnaryPulseAlphabet [PositiveUnaryPulseAlphabet]     |
#|                  - An instance of the PositiveUnaryPulseAlphabet.           |
#|                                                                             |
#|              theSymmetricBinaryPulseAlphabet [SymmetricBinaryPulseAlphabet] |
#|                  - An instance of the SymmetricBinaryPulseAlphabet.         |
#|                                                                             |
#|                                                                             |
#|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv|

# Module docstring:
"""The pulseAlphabet module defines the following pulse alphabet classes:
        
        PulseAlphabet                   Base class.
        UnaryPulseAlphabet              Pulse alphabets with 1 element.
        PositiveUnaryPulseAlphabet      A pulse alphabet with 1 element: +1.
        BinaryPulseAlphabet             Pulse alphabets with 2 elements.
        SymmetricBinaryPulseAlphabet    A pulse alphabet with 2 elements: -1, +1."""

    #|=========================================================================|
    #| Module section 0.  Exports.                           [code section]    |
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv|
    
# This special module attribute gives the list of names that are 'exported'
# from this module, i.e., that will be imported into an importing module 
# when that module does 'from <thisModule> import *'.
__all__ = [         # NOTE: I'm not sure we really need to export all these.
        # Classes:
            'PulseAlphabet',
            'UnaryPulseAlphabet',
            'PositiveUnaryPulseAlphabet',
            'BinaryPulseAlphabet',
            'SymmetricBinaryPulseAlphabet',
        # Objects:
            'thePositiveUnaryPulseAlphabet',
            'theSymmetricBinaryPulseAlphabet'
    ]

    #|=========================================================================|
    #| Module section 1.  Imports.                           [code section]    |
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv|
    
from collections.abc import Iterable    # Used in type hints.
from utilities import count             # Counts elements of an Iterable.


    #|=========================================================================|
    #| Module section 2. Class definitions.                  [code section]    |
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv|

        #|---------------------------------------------------------------------|
        #|                                                                     |
        #|  PulseAlphabet                             [module public class]    |
        #|                                                                     |
        #|      This is the base class for all pulse alphabets. A pulse        |
        #|      alphabet specifies the symbols for a set of pulse types.       |
        #|      Two PulseAlphabet objects should be considered equal iff       |
        #|      they specify the same sequence of symbols.                     |
        #|                                                                     |
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv|

class PulseAlphabet:

    """Base class for pulse alphabets <pa>.  A pulse alphabet specifies 
        an ordered sequence of all of the distinct symbols corresponding
        to pulse types in a given set of pulse types, and rules for 
        operating on those pulse type symbols.
        
    
        Public instance properties:
        ---------------------------
        
            pa.arity:int - The cardinality or multiplicity m>0 of the set        |
                of pulse types; i.e., the number of distinct pulse types 
                in this alphabet.
            
            pa.symbols:iterable - Ordered sequence of all symbols in the 
                alphabet. For each pulse type index j>=0, pa.symbols[j]
                should give the corresponding symbol representing that 
                pulse type, which should be an object of class PulseType.
                (See the pulseType module.)
            
            pa.negatable - Return True if this pulse type alphabet supports
                a "negate" operation on pulse types.  A negate operation is
                a unary operation '-' such that, for each pulse type x, 
                either x = -x, or there is a y such that y = -x and x = -y.
            
            pa.opposable - Return True if this pulse type alphabet supports
                an oppository "opposite" operation on pulse types.  An 
                oppository operation is a unary operation '/' such that, for 
                each pulse type x, there is a y such that y = /x and x = /y.
                
            
        Public instance methods:
        ------------------------
        
            pa.negate(pt) - For negatable pulse alphabets, returns the
                negative of pulse type <pt>.  Alternate syntax: -pt.
                
            pa.opposite(pt) - For opposable pulse alphabets, returns the
                opposite of pulse type <pt>.  Alternate syntax: ~pt.
    """


    @property
    def arity(pulseAlphabet):
        """The number of distinct pulse types in this pulse alphabet."""
        return pulseAlphabet._arity

    @property
    def symbols(pulseAlphabet):
        """The sequence of symbols making up this pulse alphabet."""
        return pulseAlphabet._symbols

    def __init__(pulseAlphabet, symbols:Iterable):
        """The instance initializer sets up the alphabet's attributes."""
        pulseAlphabet._arity = count(symbols)
        pulseAlphabet._symbols = tuple(symbols)

    def __str__(pulseAlphabet):
        """Returns a printable representation of the pulse alphabet."""
        return str(list(pulseAlphabet.symbols))

        # Pulse alphabets are equivalent if their symbol lists are the same.

    def __eq__(pulseAlphabet, otherObj):
        return (isinstance(otherObj, PulseAlphabet)
                and pulseAlphabet.symbols == otherObj.symbols)

    def __hash__(pulseAlphabet):
        return hash(pulseAlphabet.symbols)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Compact syntax for .negate() and .opposite() operations.
    
    def __neg__(pulseAlphabet, pulseType):
        return pulseAlphabet.negate(pulseType)
        
    def __inv__(pulseAlphabet, pulseType):
        return pulseAlphabet.opposite(pulseType)

    def __eq__(thisPulseAlphabet, otherPulseAlphabet):
        pa1 = thisPulseAlphabet
        pa2 = otherPulseAlphabet
        return set(pa1.symbols()) == set(pa2.symbols())
            # Note the order of the symbols doesn't matter.
    
    def __hash__(thisPulseAlphabet):
        return hash(tuple(thisPulseAlphabet.symbols))

#__/ End class PulseAlphabet.


        #|---------------------------------------------------------------------|
        #|                                                                     |
        #|  UnaryPulseAlphabet                        [module public class]    |
        #|                                                                     |
        #|      A unary pulse alphabet is one that only contains a single      |
        #|      pulse type.                                                    |
        #|                                                                     |
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv|

class UnaryPulseAlphabet(PulseAlphabet):

    """A subclass of PulseAlphabet that is still somewhat abstract
        (since it does not specify the pulse symbol) but that at least 
        specifies that the .arity property has the value 1."""
    
    isUnary = True
    
    def __init__(self, pulseSymbol):
        super().__init__((pulseSymbol,))
            # Note the comma is necessary to force (pulseSymbol,) to
            # parse as a tuple rather than just a parenthesized 
            # arithmetic expression.


        #|---------------------------------------------------------------------|
        #|                                                                     |
        #|  PositiveUnaryPulseAlphabet                [module public class]    |
        #|                                                                     |
        #|      This is a unary pulse alphabet in which the single pulse       |
        #|      type is symbolized by the number (+) 1.  This is used to       |
        #|      represent the supported pulse types for I/O ports and          |
        #|      interconnects that are specified to only support fluxons       |
        #|      containing a total flux charge of +1 flux quantum.             |
        #|                                                                     |
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv|

# Should this be a @singleton class?
class PositiveUnaryPulseAlphabet(UnaryPulseAlphabet):
    """A subclass of UnaryPulseAlphabet that specifies that the symbol
        for the pulse is +1, corresponding to the flux charge (in
        magnetic flux quanta) of the physical voltage pulse."""
    def __init__(self):
        super().__init__(+1)


        #|---------------------------------------------------------------------|
        #|                                                                     |
        #|  BinaryPulseAlphabet                       [module public class]    |
        #|                                                                     |
        #|      A binary pulse alphabet is one that contains exactly two       |
        #|      types of pulses.                                               |
        #|                                                                     |
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv|

class BinaryPulseAlphabet(PulseAlphabet):

    """A subclass of PulseAlphabet that is still a somewhat abstract class
        (since it does not specify the actual symbol list) but
        that specifies that the .arity attribute has the value 2."""

    isUnary = False

    def __init__(this, firstSymbol, secondSymbol):
        super().__init__((firstSymbol, secondSymbol))

    def opposite(this, symbol):

        """Given a symbol in the alphabet, return its opposite."""
        
        if symbol == this._symbols[0]:
            return this._symbols[1]
        else:
            return this._symbols[0]

        #|---------------------------------------------------------------------|
        #|                                                                     |
        #|  SymmetricBinaryPulseAlphabet              [module public class]    |
        #|                                                                     |
        #|      This is a binary pulse alphabet in which the two types of      |
        #|      pulses are symbolized by the integers -1 and +1 (as opposed    |
        #|      to, say, 0 and 1).  A symmetric binary alphabet is appropri-   |
        #|      ate for representing pulses embodied by fluxons on LJJ         |
        #|      transmission lines, since the -1,+1 symbols can also corre-    |
        #|      spond to the number of flux quanta carried by the given flux   |
        #|      soliton.                                                       |
        #|                                                                     |
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv|

# Should this be a @singleton class?
class SymmetricBinaryPulseAlphabet(BinaryPulseAlphabet):      
    """A subclass of BinaryPulseAlphabet where the symbols are -1,+1."""
    
    def __init__(this):
        super().__init__(-1, +1)

    def negate(this, sym):
        return -sym

#__/ End class SymmetricBinaryPulseAlphabet.


    #|=========================================================================|
    #| Module section 3.  Global object initializations.     [code section]    |
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv|

thePositiveUnaryPulseAlphabet = PositiveUnaryPulseAlphabet()
    # A global singleton object representing the symbol alphbet {+1}.

theSymmetricBinaryPulseAlphabet = SymmetricBinaryPulseAlphabet()
    # A global singleton object representing the symbol alphabet {-1, +1}.


#|^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^|
#|                    BOTTOM OF FILE:  pulseAlphabet.py                        |
#|=============================================================================|