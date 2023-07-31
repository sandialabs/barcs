#|%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% TOP OF FILE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#|                                                                             |
#|      FILE NAME:      stateSet.py                         [Python 3 module]  |
#|                                                                             |
#|      PROGRAM NAME:   BARC Element Classifier (barc)                         |
#|      MODULE NAME:    stateSet                                               |
#|                                                                             |
#|      AUTHOR:         Michael P. Frank <mpfrank@sandia.gov>                  |
#|                                                                             |
#|      PROJECT:        LPS/ACS/ACI Project #41, Asynchronous Ballistic        |
#|                      Reversible Computing using Superconducting             |
#|                      Elements (ABRC/SE)                                     |
#|                                                                             |
#|      IMPORTED BY:    (4) barc.                                              |
#|      CODE LAYER:     Layer #2 (no imports from above layer #1).       	   |
#|      IMPORTS:        (1) state.                                             |
#|                                                                             |
#|-----------------------------------------------------------------------------+
#|                                                                             |
#|      DESCRIPTION:                                                           |
#|      ============                                                           |
#|                                                                             |
#|          This Python 3 source file defines a module that includes           |
#|          various classes and objects for defining particular sets           |
#|          of FSM (finate state machine) states with associated symbolic      |
#|          representations.                                                   |
#|                                                                             |
#|          In particular, in the context of the BARCS effort, we define       |
#|          state sets for device states associated with flux configura-       |
#|          tions which can be abstractly transformed into distinct states     |
#|          via flux negation (F) transformations.  This is important for      |
#|          characterizing the symmetry groups that BARCS devices live in.     |
#|                                                                             |
#|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv|


# Exports:
__all__ = [
        # Classes:
            #'StateSet',                # Not currently used outside this module.
            #'TwoStateSet',             # Not currently used outside this module.
            #'SymmetricTwoStateSet',    # Not currently used outside this module.
            #'LRStateSet',              # Not currently used outside this module.
            #'ThreeStateSet',           # Not currently used outside this module.
            #'SymmetricThreeStateSet',  # Not currently used outside this module.

        # Module-global objects:

            'theSymmetricTwoStateSet',
                # State set {-1,+1}; used in main program (barc).

            'theLRStateSet',
                # State set {'L','R'}; used in main program (barc).

            #'theSymmetricThreeStateSet'    # Not currently used outside this module.
    ]

# Imports:
from    state   import  State
    # We need to reference this class constructor when enumerating
    # our possible states.

#-------------------------------------------------------------------------------

# Defines sets of states.
class StateSet:

    """An object that is an instance of class StateSet defines a 
        particular set of internal device states."""

    #|      .negatable:bool - True if all states in the given state set
    #|          are negatable, meaning, they support the .negate()
    #|          (unary '-') operation.
    #|
    #|      .cardinality:int - The number K of distinct states in this
    #|          set of states.
    #|
    #|      .symbols:iterable - Gives the symbols for the K states, in
    #|          their canonical order {s_1, ..., s_K}.
    #|
    #|      .fluxNeutral:bool - True if and only if all possible internal
    #|          states in the state set are flux-neutral, that is, they
    #|          contribute nothing to the total flux charge of any I/O
    #|          syndrome (in the context of a flux-conservation constraint).

    def __init__(stateSet, symbols):
        stateSet._cardinality = len(symbols)
        stateSet._symbols = symbols

    @property
    def negatable(stateSet):
        return None

    @property
    def cardinality(stateSet):
        return stateSet._cardinality

    @property
    def symbols(stateSet):
        return stateSet._symbols

    def state(thisStateSet, symbol):
        return State(thisStateSet, symbol)

    def states(thisStateSet):
        tss = thisStateSet
        return map(lambda sym: tss.state(sym), tss.symbols)

    def __str__(stateSet):
    
        """A concise string representation of this state set."""
        
        s = ""
        for state in stateSet:
            s += str(state)
            s += ','
        s = s[:-1]      # Trim last comma
    
        return s

    def __iter__(stateSet):
        return stateSet.states()
        
    def __eq__(thisStateSet, otherStateSet):
        ss1 = thisStateSet
        ss2 = otherStateSet
        return set(ss1.symbols) == set(ss2.symbols)

    def __hash__(thisStateSet):
        return hash(tuple(thisStateSet.symbols))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # To support state negation, for state sets that support it.
    # Negatable derived classes should implement .negateSymbol().
    
    def negateState(stateSet, state):
        return state.negate()

    def negate(stateSet, stateOrSymbol):
        if isinstance(stateOrSymbol, State):
            return stateSet.negateState(stateOrSymbol)
        else:
            return stateSet.negateSymbol(stateOrSymbol)

#-------------------------------------------------------------------------------

class TwoStateSet(StateSet):

    @property
    def negatable(stateSet):
        return True

    def __init__(twoStateSet, firstSymbol, secondSymbol):
        twoStateSet.firstSymbol = firstSymbol
        twoStateSet.secondSymbol = secondSymbol
        super().__init__((firstSymbol, secondSymbol))
    
    # We'll declare state negation to be a well-defined operator
    # for all two-state sets.
    
    def negateSymbol(twoStateSet, symbol):
    
        firstSymbol = twoStateSet.firstSymbol
        secondSymbol = twoStateSet.secondSymbol
    
        if symbol == firstSymbol:
            return secondSymbol
        else:
            return firstSymbol

#-------------------------------------------------------------------------------

# Should this be a @singleton class?
class SymmetricTwoStateSet(TwoStateSet):

    # Class constant: No, this state set isn't flux-neutral.
    fluxNeutral = False
    
    def __init__(symmetricTwoStateSet):
        super().__init__(-1, +1)

# Should this be a @singleton class?
class LRStateSet(TwoStateSet):

    """This is a state set in which there are two states named L and R
        (possibly implying some association between the states and ports 
        of the same name, or a direction of rotary action). For this
        particular state set, we assume a state encoding that is net 
        flux-neutral (for example, L might be encoded by +1,-1 flux in a
        pair of loops, and R might be encoded by a -1,+1 arrangement.)."""

    # Class constant: Yes, this state set is flux-neutral.
    fluxNeutral = True

    def __init__(symmetricTwoStateSet):
        super().__init__('L', 'R')

#-------------------------------------------------------------------------------

class ThreeStateSet(StateSet):

    def __init__(threeStateSet, firstSymbol, secondSymbol, thirdSymbol):
        super().__init__((firstSymbol, secondSymbol, thirdSymbol))

#-------------------------------------------------------------------------------

# Should this be a @singleton class?
class SymmetricThreeStateSet(ThreeStateSet):
    
    def __init__(symmetricThreeStateSet):
        super().__init__(-1, 0, +1)

    # State negation is a well-defined operator for this state set.
    def negate(this, symbol):
        return -symbol

#-------------------------------------------------------------------------------

theSymmetricTwoStateSet = SymmetricTwoStateSet()
theLRStateSet = LRStateSet()

    # A global singleton object representing the three-state set {-1, 0, +1}.

theSymmetricThreeStateSet = SymmetricThreeStateSet()


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% BOTTOM OF FILE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%