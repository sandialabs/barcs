#|%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% TOP OF FILE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%|
#|                                                                             |
#|      FILE NAME:      symmetryTransform.py           		[Python 3 module]  |
#|                                                                             |
#|      PROGRAM NAME:   BARC Element Classifier (barc)                         |
#|      MODULE NAME:    symmetryTransform                                      |
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
#|-----------------------------------------------------------------------------+
#|                                                                             |
#|      DESCRIPTION:                                                           |
#|      ============                                                           |
#|                                                                             |
#|          This module defines classes for the various types of               |
#|          symmetry transformations that we support.  See the module          |
#|          docstring below for additional details.                            |
#|                                                                             |
#|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv|
"""

    Classes in this module carry out symmetry transforms on device functions' 
    transition functions. 
    
    A symmetry transform is a bijective map (permutation) on the space of 
    transition functions for a given device type, one that reflects a funda-
    mental equivalence between transition functions.
    
    Much of the purpose of the BARC software is to group the transition func-
    tions into equivalence classes under various symmetry transforms, as a 
    way of simplifying our understanding of the set of possible transition
    functions for a given device type.
    
    Some important terminology:

    If a given transition function f is equal to itself under a symmetry 
    transform X, then we say f "possesses X (self-)symmetry."
    
    If the symmetry transform X is its own inverse, i.e. if X*X = I,
    then we call it self-inverse, or an involution.
    
    If, for transition functions f,g, and a self-inverse symmetry transform 
    X, it is the case that f(X)=g, then also f(g)=X, and we say that f,g are 
    "duals under X", or "are X-symmetric (or X-dual) to each other."
    
    If X is not self-inverse, then for some n>2, we still have that X^n = I: 
    Repeating a fixed permutation on any finite set will eventually return us 
    to the initial ordering.  The "order" of a symmetry transformation X is 
    the smallest n such that X^n = I.  Thus, self-inverse transformations have 
    order 2.  (And we'll consider other transformations with order 3; specifi-
    cally rotation transformations on 3-port devices.)
    
    Thus, if f(X)=g, but X is not self-inverse, we can still say that "f and g 
    are in the same symmetry (equivalence) group under X."
    
    The important symmetry transforms that we will define in this module 
    include the following:
    
        * Direction-reversal transformation (D). (Self-inverse.)
        
            In a D transformation, the direction of motion
            of fluxons (incoming vs. outgoing) is reversed, 
            and initial vs. final states are also exchanged,
            so that input syndromes transform into output
            syndromes, and vice-versa. In other words, for
            signal characters c1,c2 and states s1,s2, if 
            the transition
            
                            c1(s1) --> (s2)c2

            was present in the initial transition function f,
            then the new transition function D(f) will include
            the transition
            
                            c2(s2) --> (s1)c1.

        * Flux-negation transformation (F). (Self-inverse.)
        
            If a flux-negation transformation, the signs of all
            flux charges (i.e., of all currents) in the circuit
            are negated.  This negates the value (+1 vs. -1) of
            all I/O symbols, and (for our purposes) also flips
            the internal state in 2-state devices.  Thus, if
            the transition 

                            c1(s1) --> (s2)c2

            is present in f, then the transition
            
                            -c1(-s1) --> (-s2)-c2

            will be present in g=F(f).
                    
        * State-negation transformation (S). (Self-inverse.)
        
            For device types in which internal states can be
            meaningfully negated (that is, for some state s, 
            there is a different state t such that s = -t and 
            t = -s; and also, for every state s, either s = -s 
            or there is another state t such that s = -t and 
            t = -s), the state-negation symmetry transformation 
            performs the state negation.
            
            Thus, the transition
            
                            c1(s1) --> (s2)c2

            becomes
            
                            c1(-s1) --> (-s2)c2.
                            
            Note we define state negation even for flux-neutral 
            binary states; it carries out a state exchange. Also,
            in devices using the symmetric three-state set {-1,
            0, 1}, we can do state-negation, but note -0 = 0.
            
        * Port-exchange transformation E(i,j). (Self-inverse.)
        
            For device types with two or more ports, and port
            labels i,j, i=/=j, this refers to a transformation
            in which port labels i and j are exchanged.
        
        * Port-rotation transformation R(+/-). (Self-inverse.)
        
            Defined for three-port device types, there are two
            of these transformations.  In R(+), port labels
            (1,2,3) map to port labels (2,3,1).  In R(-), port
            labels (1,2,3) map to port labels (3,1,2). Note that
            R(+)*R(+) = R(-) and R(-)*R(-) = R(+).
        
    Note that we also support arbitrary "composite" transforms, which are 
    products of the above.
    
    Some additional transformations which we may implement later are:
    
        * Input-negation symmetry I. (Self-inverse.)
        
            This negates incoming pulse-type symbols, but not outgoing ones.
            
        * Output-negation symmetry O. (Self-inverse.)
        
            This negates outgoing pulse-type symbols, but not incoming ones.
            
    There are additional, composite transformations which may be defined
    as compositions of the aforementioned ones:
    
        * Moving-fluxon negation symmetry: M = I*O.
        
        * Also note that, the way we defined F, it's equal to M*S.
        
"""

# Exported names.
__all__ = [
        # Public classes for various primitive transforms:
            'DirectionReversalTransform',   # Class of direction-reversal transforms (D).
            'FluxNegationTransform',        # Class of flux-negation transforms (F).
            'StateNegationTransform',       # Class of state-negation transforms (S).
            'PortExchangeTransform',        # Class of port-exchange transforms (E(i,j)).
            'PortRotationTransform',        # Class of port-rotation transforms (R(+/-)).

        # Public class of arbitrary composite transforms:
        'CompositeTransform',
    ]


class SymmetryTransform_:

    """A symmetry transform or transformation is a bijective,
        non-identity operation on transition functions for a given 
        device type. The SymmetryTransform_ class is an abstract 
        base class (which is what the final '_' is denoting). All 
        symmetry transforms <st> of concrete derived classes should 
        support all of the following methods/properties (however,
        note that most of these are not yet used in this program):

            st.deviceType - This instance-level property gives the 
                device type that this specific symmetry transform
                instance is designed for.

            st.transform() - Returns the transition function that
                the given transition function <f> maps to under the
                given transformation <st>.  Concise alternate
                syntax: st(<f>). (Virtual function; not defined for
                base class.)
                
            st.inverse() - Returns another symmetry transformation
                <st_inv> that is the inverse transformation to <st>.
                Concise alternate syntax: -st.

            st.isSelfInverse - This class-level property is True 
                if and only if all transformations of this class 
                are their own inverse. It is False if and only if
                all transformations of this class are not their
                own inverse. It is None if the class is so general 
                that it includes both self-inverse transformations
                and non-self-inverse transformations.

            st.maps() - Given two transition functions <f>,<g>,
                this returns True if and only if st(<f>) = <g>.

            st.areDuals() - Applicable for self-inverse transforms.
                Given two transition functions, this method returns 
                True if and only if the two functions are duals to 
                each other under the self-inverse symmetry 
                transformation <st>. (Note that the order of the 
                arguments does not matter.)
                
            st.isSelfDual() - Given a transition function, this method
                returns True if and only if that function maps to 
                (a function equivalent to) itself under the self-inverse
                symmetry transform <st>.
            
            st.symmetricUnder() - Given a transition function, this
                method returns True if and only if that function 
                transforms to itself under <st>. Note this is more
                general than .isSelfDual() since it applies even for
                non-self-inverse symmetry transformations.
            
            st1.compose(st2) - Given another symmetry transform <st2>
                for the same device type, returns a symmetry transform 
                that is the composition of <st1> followed by <st2>.
                Concise alternate syntax: <st2>*<st1>.
            
            st.toPower() - Given an integer <n>, this returns the nth
                power of <st>, that is, <st>*<st>*...*<st> (n times)
                if n is positive, and the same for ~<st> if 
            
            st.sameGroup() - Given two transition functions <f>,<g>, 
                this method returns True iff <f> and <g> are "in the
                same symmetry group under <st>", meaning, there is
                some <n> such that st.toPower(n)(<f>) = <g>.
                
            st1.commutesWith(st2) - Given two symmetry transforms
                <st1> and <st2>, this returns True if and only if
                they commute with each other, or in other words, if
                <st1>*<st2> == <st2>*<st1>. (Not yet implemented,
                because we haven't yet implemented equivalence
                checking between composite transformations.)
        
        """
    
    def __init__(newSymmetryTransform, deviceType):
        st = newSymmetryTransform
        st._deviceType = deviceType

    @property
    def deviceType(st):
        return st._deviceType
    
    # .transform() is not defined here and should be implemented by 
    # all concrete subclasses.
    
    def inverse(st):
        """Return the inverse transform to this one."""
        if st.isSelfInverse:
            return st
        # Note this method returns None for non-self-inverse
        # transformations. In this case, the subclass should 
        # override this method.
    
    @property
    def isSelfInverse(st):
        return None     # Class is too abstract to tell.

    def maps(st, df1, df2):
        """Returns True iff <df1> transform to <df2> under <st>."""
        return st(df1) == df2
    
    def areDuals(st, df1, df2):
        """Returns True iff <df1> and <df2> are duals under the
            self-inverse transformation <st>. Returns None if <st>
            isn't self-inverse."""
        if st is None:
            return None
        return st.maps(df1,df2)
    
    def isSelfDual(st, df):
        """Returns True iff <df> is dual to itself (i.e., unchanged)
            under the self-inverse transformation <st>. Returns None 
            if <st> isn't self-inverse."""
        return st.areDuals(df,df)
    
    def isSymmetric(st, df):
        """Returns True iff <df> transforms to itself (i.e., is unchanged)
            under the symmetry transformation <st>."""
        return st.maps(df,df)
    
    def compose(thisSymmetryTransform, thatSymmetryTransform):
        """Returns a new, composite symmetry transformation that
            consists of applying first <thisSymmetryTransform>,
            followed by <thatSymmetryTransform>. (Note that this
            is a "left-compose" operation.)"""
        st1 = thisSymmetryTransform
        st2 = thatSymmetryTransform
        return CompositeTransform(st2, st1)
    
    def commutesWith(thisSymmetryTransform, thatSymmetryTransform):
        pass    # Not yet implemented.
    
    def __neg__(st):
        return st.inverse()
        
    def __call__(st,func):
        return st.transform(func)


# Note: We could make the following class more powerful by keeping
# track of a list of constituent transforms, and flattening the list
# when combining; this would automatically apply the associative
# property, to make it easier to detect equivalence between composite
# transforms constructed in different ways. However, this wouldn't by
# itself capture all cases of equivalence, so I'm not sure it's 
# worthwhile. (Note a more general way to detect equivalence between
# transforms is just by looking at how they transform all possible
# transition functions, though this is time-consuming to do for 
# complex device types.)

class CompositeTransform(SymmetryTransform_):
    """A symmetry transformation that is the composite of two or more
        constituent transformations."""
    def __init__(newCompositeTransform, st1, st2):
        """Creates a new composite symmetry transformation that
            consists of applying first the transform st2, and
            then applying the transform st1 to the result of that."""
        nct = newCompositeTransform
        nct._symTrans1 = st1
        nct._symTrans2 = st2
        
    def transform(thisCompositeTransform, func):
        """Transforms the given function by applying first st2
            and then st1."""
        tct = thisCompositeTransform
        st1 = tct._symTrans1
        st2 = tct._symTrans2
        return st1(st2(func))   # Applies st1*st2.


class SelfInverseTransform_(SymmetryTransform_):
    @property
    def isSelfInverse(st):
        return True


class NonSelfInverseTransform_(SymmetryTransform_):
    @property
    def isSelfInverse(st):
        return False


class DirectionReversalTransform(SelfInverseTransform_):
    
    """Maps the transition function to its inverse."""

    def transform(drt, func):
        return func.reverse()

    @property
    def desc(drt):
        return "(Direction Reversal)"
    
    @property
    def sym(drt):
        return 'D'


class FluxNegationTransform(SelfInverseTransform_):
    
    """Negates all polarized I/O fluxes, and also 
        negates the internal state, if it is negatable."""

    def transform(fnt, func):
        return func.negFlux()

    @property
    def desc(fnt):
        return "(Flux Negation)"
    
    @property
    def sym(fnt):
        return 'F'


class StateNegationTransform(SelfInverseTransform_):
    
    """Only usable for device types with a negatable
        state set.  Negates only the internal state."""

    def transform(fnt, func):
        return func.negStates()

    @property
    def desc(snt):
        return "(State Swap)"
    
    @property
    def sym(snt):
        return 'S'


class PortExchangeTransform(SelfInverseTransform_):
    
    """Only usable for device types with at least 2 ports.
        Exchanges a specified pair of the ports."""

    def __init__(newPortSwapTrans, devType, port1, port2):
    
        npst = newPortSwapTrans

            # Canonicalize port order.
        if port1 > port2:
            tmp = port1
            port1 = port2
            port2 = tmp

        npst.port1 = port1
        npst.port2 = port2
        
        super().__init__(devType)

    def transform(pst, func):
        return func.portSwap(pst.port1, pst.port2)

    @property
    def desc(pet):
        return f"(Swap ports {pet.port1+1} <-> {pet.port2+1})"
    
    @property
    def sym(pet):
        return f'E({pet.port1+1},{pet.port2+1})'
        
    
class PortRotationTransform(NonSelfInverseTransform_):

    """Only usable for device types with at least 3 ports.
        This transformation simply rotates each port index
        to the next, in circular fashion."""
        
    def __init__(newPortRotTrans, devType, offset):
        nprt = newPortRotTrans
        nprt.offset = offset
        super().__init__(devType)
        
    def transform(prt, func):
        return func.portRotate(prt.offset)

    def inverse(prt):
        """To invert a port-rotation transformation, 
            we simply negate its offset."""
        return PortRotationTransform(-prt.offset)

    @property
    def desc(prt):
        return f"(Rotate ports {prt.offset})"
    
    @property
    def sym(prt):
        return f'R({prt.offset})'


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% BOTTOM OF FILE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%