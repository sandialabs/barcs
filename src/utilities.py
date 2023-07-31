#|%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% TOP OF FILE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%|
#|                                                                             |
#|      FILE NAME:      utilities.py           	            [Python 3 module]  |
#|                                                                             |
#|      PROGRAM NAME:   BARC Element Classifier (barc)                         |
#|      MODULE NAME:    utilities                                              |
#|                                                                             |
#|      AUTHOR:         Michael P. Frank <mpfrank@sandia.gov>                  |
#|                                                                             |
#|      PROJECT:        LPS/ACS/ACI Project #41, Asynchronous Ballistic        |
#|                      Reversible Computing using Superconducting             |
#|                      Elements (ABRC/SE)                                     |
#|                                                                             |
#|      IMPORTED BY:    (3) deviceType;                                        |
#|                      (2) deviceFunction;                                    |
#|                      (1) pulseAlphabet, pulseType, state, symmetryGroup,    |
#|                              transitionFunction.                            |
#|      CODE LAYER:     Layer #0 (no custom imports).                          |
#|                                                                             |
#|                                                                             |
#|      FILE HISTORY:                                                          |
#|      =============                                                          |
#|                                                                             |
#|          2022 Nov. 6th   - Substantial cleanup; getting ready to archive.   |
#|                                                                             |
#|-----------------------------------------------------------------------------+
#|                                                                             |
#|      DESCRIPTION:                                                           |
#|      ============                                                           |
#|                                                                             |
#|          This module defines a grab-bag of simple utility functions         |
#|          that are used by other modules.  These include:                    |
#|                                                                             |
#|                                                                             |
#|      Defines public names:                                                  |
#|      =====================                                                  |
#|                                                                             |
#|      (The following are all functions.)                                     |
#|                                                                             |
#|          assignID()                                          [function]     |
#|                                                                             |
#|              Assigns a given device function a unique numeric ID.           |
#|                                                                             |
#|          lookupID()                                          [function]     |
#|                                                                             |
#|              Looks up the unique numeric ID for the given device            |
#|              function.                                                      |
#|                                                                             |
#|          count()                                             [function]     |
#|                                                                             |
#|              Counts the number of items enumerated by an iterable.          |
#|                                                                             |
#|          hashdict()                                          [function]     |
#|                                                                             |
#|              Returns a hash code for a dictionary (assuming its             |
#|              key-value pairs can be ordered and are hashable).              |
#|                                                                             |
#|          isOdd()                                             [function]     |
#|                                                                             |
#|              Returns True if the given integer is odd.                      |
#|                                                                             |
#|          flux()                                              [function]     |
#|                                                                             |
#|              Returns the integer flux value (in units of the                |
#|              magnetic flux quantum) corresponding to a given                |
#|              pulse-type or internal state symbol.                           |
#|                                                                             |
#|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv|
"""Miscellaneous utility functions."""

# Exported names.
__all__ = [
        # Classes:

            #'_KeyClass',     
                # Simple generic class for sort keys.
                # Not used outside utils module at present.

            #'_Pair',         
                # Sortable ordered-pair type.
                # Not used outside utils module at present.
        
        # Globals:

            #'_deviceIDs',    
                # Maps deviceFunction objects to numeric IDs.
                # Private; not used outside utils module.

        # Functions:

            'assignID',
                # Assigns a device function a unique numeric ID. 
                # Used in the main program (top-level module).

            'lookupID',     
                # Look up the unique numeric ID for the given device. 
                # Used in deviceFunction module.

            'count',        
                # Counts the number of items in an iterable.
                # Used at top-level and in pulseAlphabet & symmetryGroup modules.

            'hashdict',
                # Hashes a dictionary. 
                # Used by the transitionFunction module.

            'isOdd',
                # Returns True on odd numbers.
                # Used by deviceType module.

            'flux',
                # Returns the flux value of a given symbol.
                # Used by pulseType and state modules.
    ]


# Imports.
from collections.abc import Iterable    # Used in type hints.


    #|==========================================================================
    #|  Module section 1:  Classes.                     [module code section]
    #|
    #|      Note that the following two classes are both private (i.e.,
    #|      they are only used internally within this module, and are
    #|      not intended to be exported to other modules.
    #|
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

class _KeyClass:     # Not used outside utils -- could make it private.

    """Given objects of any class that supports __eq__ and __lt__ 
        methods, _KeyClass is a "key function" that can 
        be used e.g. for sorting items of that class."""
    # USAGE: sorted(objList, key=_KeyClass)

    def __init__(self, obj, *args):
        self.obj = obj
    def __lt__(self, other):
        return self.obj < other.obj
    def __gt__(self, other):
        return other.obj < self.obj
    def __eq__(self, other):
        return self.obj == other.obj
    def __le__(self, other):
        return (self < other) or (self == other)
    def __ge__(self, other):
        return (self > other) or (self == other)
    def __ne__(self, other):
        return not (self == other)


class _Pair:     # Not used outside utils -- could make it private.
    """A simple ordered-pair type that supports comparison, hashing, and
        sorting. This is used by the utils.hashdict() function."""
    def __init__(p, a, b):
        p.a = a
        p.b = b
    def __lt__(p, q):
        return (p.a < q.a) or ((p.a == q.a) and (p.b < q.b))
    def __eq__(p, q):
        return p.a == q.a
    def __hash__(p):
        return hash((p.a, p.b))


    #|==========================================================================
    #|  Module section 2:  Globals.                     [module code section]
    #|
    #|      Note that the only global variable defined here (_deviceIDs)
    #|      is private in that it is only used within this module and is
    #|      not intended to be exported to other modules.  It should be
    #|      accessed by other modules only through the public functions
    #|      assignID() and lookupID(), defined below.
    #|
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

global _deviceIDs       # Maps deviceFunction objects to numeric IDs. Private.
_deviceIDs = dict()      
    # This is a map from distinct deviceFunction objects to numeric IDs.
    # Initially it is empty. Use assignID() to populate it.


    #|==========================================================================
    #|  Module section 3: Functions.                    [module code section]
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        #|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #|  assignID(), lookupID()                  [module public functions]
        #|
        #|      These two functions are for working with the global map
        #|      from distinct deviceFunction objects to their corresponding 
        #|      unique numeric IDs.
        #|
        #|      Note that this map has to be managed as a hash table rather
        #|      than as an instance attribute of DeviceFunction, since
        #|      deviceFunction objects may be reconstructed in a variety of 
        #|      ways; the unique IDs allow us to recognize them as long as 
        #|      we have seen them before.
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

def assignID(device,id):
    """Given a deviceFunction object <device>, assigns it the unique
        numeric identifier <id>."""
    _deviceIDs[hash(device)] = id
    
def lookupID(device):
    """Given a deviceFunction object <device>, looks up and returns its
        unique numeric identifier."""
    return _deviceIDs[hash(device)]


        #|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #|  count()                                 [module public function]
        #|
        #|      Given an iterable, this function counts how many items it 
        #|      enumerates. (Why isn't this functionality built into 
        #|      Python? Or is it?)
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

def count(iterable:Iterable) -> int:
    """Counts the number of items in the given iterable."""
    # The below implementation is more verbose, but slightly faster than 
    # just doing sum(1 for f in iterable).
    count = 0
    if iterable is not None:
        for item in iterable:
            count += 1
    return count


        #|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #|  flux()                                  [module public function]
        #|
        #|      Given a symbol for a state or a pulse type, return the
        #|      corresponding net flux present in a device in that state
        #|      or a pulse of that pulse type.
        #|
        #|      This assumes that symbol objects of integer type *are* 
        #|      the flux and that symbol objects of type string have no
        #|      flux.  Other cases are not supported.
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

# Given a state or pulse-type symbol, return the corresponding net flux.
def flux(chrOrInt):
    """Returns the flux value of the given (character or integer) symbol."""

    # Assume named states have zero net internal flux.
    if type(chrOrInt) == str:
        return 0
    
    # Assume states that are integers have that as their net internal flux.
    if type(chrOrInt) == int:
        return chrOrInt

    # Other cases return None (we don't know how to handle them.)


        #|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #|  hashdict()                              [module public function]
        #|
        #|      Given a dictionary of items that can be put into a canon-
        #|      ical order and hashed, returns a hash for the entire dic-
        #|      tionary. The items must support the <, ==, and hash() 
        #|      operations.
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

def hashdict(dict):
    """Hashes a dictionary, so long as both the keys and values
        support < and == comparisons and are hashable."""
    
    # Get an iterable view on the items in the dictionary.
    items = dict.items()
    
    # Define a function-local helper function to generate 
    # the dictionary items in the form of sortable pairs.
    def genItems():
        for (key,val) in items:
            yield _Pair(key,val)
    
    # Get a sortable list of all ordered pairs in the dictionary.
    itemList = list(genItems())

    # Now sort the list, using our helpful generic key class.
    itemList = sorted(itemList, key=_KeyClass)
    itemTup = tuple(itemList)
    return hash(itemTup)


        #|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #|  isOdd()                                 [module public function]
        #|
        #|      Given an integer, returns True iff it is odd.
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

def isOdd(num:int) -> bool:
    """Boolean; returns True iff the number given is odd."""
    return (num % 2) == 1


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% BOTTOM OF FILE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%