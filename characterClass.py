#|%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% TOP OF FILE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%|
#|                                                                             |
#|      FILE NAME:      characterClass.py                   [Python 3 module]  |
#|                                                                             |
#|      PROGRAM NAME:   BARC Element Classifier (barc)                         |
#|      MODULE NAME:    characterClass                                         |
#|                                                                             |
#|      AUTHOR:         Michael P. Frank <mpfrank@sandia.gov>                  |
#|                                                                             |
#|      PROJECT:        LPS/ACS/ACI Project #41, Asynchronous Ballistic        |
#|                      Reversible Computing using Superconducting             |
#|                      Elements (ABRC/SE)                                     |
#|                                                                             |
#|      IMPORTED BY:    (3) deviceType.                                        |
#|      CODE LAYER:     Layer #0 (no imports from custom modules).             |
#|      IMPORTS:        (none)                                                 |
#|                                                                             |
#|-----------------------------------------------------------------------------|
#|                                                                             |
#|      DESCRIPTION:                                                           |
#|      ============                                                           |
#|                                                                             |
#|          A character class defines a set of signal characters.  In          |
#|          the general case, its properties include the port multipli-        |
#|          city and a pulse type alphabet for each port.  An important        |
#|          subclass is the UniformCharacterClass in which all ports           |
#|          have the same pulse type alphabet.                                 |
#|                                                                             |
#|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv|
"""characterClass - This module defines the CharacterClass class, 
    instances of which define a type of I/O signal character, and
    the UniformCharacterClass subclass, which is a subclass for the
    special case in which all ports have the same pulse-type alphabet."""

__all__ = [
    # Classes:
        'CharacterClass',           # Class of signal characters.
        'UniformCharacterClass'     
            # A character class wherein all ports have the same pulse-type
            # alphabet.
    ]

class CharacterClass:
    """A general class for classes of I/O signal characters."""

    #/--------------------------------------------------------------------------
    #|  Public class properties:
    #|  ========================
    #|
    #|      .isUniform [bool]   - True if all ports' pulse-type
    #|                               alphabets are the same.
    #|
    #\--------------------------------------------------------------------------

    # Private class variable.
    _isUniform = None       # Don't assume uniform by default.

    def __init__(newCharacterClass, nPorts, pulseAlphabets):
    
        ncc = newCharacterClass
    
        ncc.nPorts = nPorts
        ncc.pulseAlphabets = pulseAlphabets

        if ncc._isUniform is None:      # Uniformity not yet determined. 
            ncc._isUniform = True       # Assume it's uniform till we find otherwise.
            if nPorts > 1:
                firstAlphabet = pulseAlphabets[0]
                for alphabet in pulseAlphabets[1:]:
                    if alphabet != firstAlphabet:
                        ncc._isUniform = False

    @property    
    def isUniform(thisCharClass):
        """Boolean; True iff all ports' pulse alphabets are the same."""
        return thisCharClass._isUniform

class UniformCharacterClass(CharacterClass):
    """A class for classes of signal characters in which the pulse 
        type alphabet does not vary by port (i.e., it is the same 
        for all ports)."""

    #/--------------------------------------------------------------------------
    #|  Public class properties:
    #|  ========================
    #|
    #|      .isUnary [bool]   - True the signal character's pulse-type 
    #|                              alphabet is unary (single-valued).
    #|
    #\--------------------------------------------------------------------------

    _isUniform = True        # These character classes are all uniform.

    def __init__(newSymmCharClass, nPorts, pulseAlphabet):
        
        nscc = newSymmCharClass

        nscc.pulseAlphabet = pulseAlphabet
        pulseAlphabets = (pulseAlphabet,) * nPorts

            # Dispatch rest of initialization to our parent class.
        super().__init__(nPorts, pulseAlphabets)
    
    @property
    def isUnary(thisCharClass):
        """Boolean; True iff the pulse-type alphabet is single-valued."""
        return thisCharClass.pulseAlphabet.isUnary


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% BOTTOM OF FILE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%