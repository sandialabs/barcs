#|%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% TOP OF FILE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%|
#|                                                                             |
#|      FILE NAME:      dictPermuter.py                     [Python 3 module]  |
#|                                                                             |
#|      PROGRAM NAME:   BARC Element Classifier (barc.py)                      |
#|      MODULE NAME:    dictPermuter                                           |
#|                                                                             |
#|      AUTHOR:         Michael P. Frank <mpfrank@sandia.gov>                  |
#|                                                                             |
#|      PROJECT:        LPS/ACS/ACI Project #41, Asynchronous Ballistic        |
#|                      Reversible Computing using Superconducting             |
#|                      Elements (ABRC/SE)                                     |
#|                                                                             |
#|      IMPORTED BY:    (3) deviceType.                                        |
#|      CODE LAYER:     Layer #0 (no custom imports).                          |
#|      IMPORTS:        (none)                                                 |
#|
#|                                                                             |
#|      FILE HISTORY:                                                          |
#|      =============                                                          |
#|          2018 Oct. 16th  - Initial version, used to count 1- and 2-port     |
#|                              functions..                                    |
#|          2022 Jan. 5th   - Starting code review/cleanup to prep. for        |
#|                              extension for element classification task.     |
#|          2022 Oct. 16th  - Modifications to handle flux-polarized case.     |
#|                                                                             |
#|-----------------------------------------------------------------------------+
#|                                                                             |
#|      DESCRIPTION:                                                           |
#|      ============                                                           |
#|                                                                             |
#|          This module defines a generator function that enumerates           |
#|          all possible permutations of a given dictionary.                   |
#|                                                                             |
#|                                                                             |
#|      PUBLIC NAMES DEFINED:                                                  |
#|      =====================                                                  |
#|                                                                             |
#|          This module defines the following public names:                    |
#|                                                                             |
#|              * dictPermutations() -> iterator                [function]     |
#|                                                                             |
#|                  Generator function; returns an iterator that enum-         |
#|                  erates all the permutations of the given dictionary.       |
#|                                                                             |
#|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv|

# This file defines a generator function dictPermutations() that takes
# an arbitrary dictionary as input, and generates all possible
# permutations of assignments in that dictionary.

# Exports.
__all__ = ['dictPermutations']

# Globals.
# Module-level global variable used for diagnostic purposes.
count=0

# Functions.

def dictPermutations(dIn, level=0, verbose=False):

    """This generator function returns an iterator object that enumerates
        all possible permutations of the assignments in the given dictionary
        object."""

    global count

    if verbose or level<0:  # Can increase upper bound here to see more of the calls.
        print(level, "    "*level, "dictPermutations() called with dIn = %s" % dictStr(dIn))

        # First, make a shallow copy of the input dictionary we
        # were given, so that we don't have to disturb the input.

    d = dIn.copy()  

        # BASE CASE: If d is empty, then we just return it, and we're done.
        # Note: We also do occasional diagnostics here.

    if len(d) == 0:
        count += 1
        if count % 1000000 == 0:
            print(f"Completed {count/1000000} million steps...")
        if verbose: print("    "*level, "    Returning copy of empty initial dict:  %s" % d)
        yield d
        return

        #/~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #|  Next, we extract an arbitrary key-value pair from the original
        #|  dictionary; we will 'pivot' our permutations 'centered' on this
        #|  item. The following then breaks down naturally into two cases:
        #|
        #|      1. Permutations where the pivot item's value is unchanged.
        #|
        #|      2. Permutations in which the pivot item's value is that which
        #|          was originally assigned to a *different* item's key.
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    pivotKey, pivotVal = d.popitem()     # Pop an arbitrary key-value pair from the dict.
    if verbose: print("    "*level, "    Extracted pivot point:  %s\t--> %s" % (pivotKey, pivotVal))

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 1. First, we recursively iterate through all permutations of the
        #       remaining items in the dictionary.

    for dPerm in dictPermutations(d, level+1):

            # Add the (unmodified) pivot item back into the permuted dictionary.

        dPerm[pivotKey] = pivotVal

            # Yield a copy of the current dPerm to the generator's caller.

        if verbose: print("    "*level, "    Yielding permutation:  %s" % dictStr(dPerm))
        yield dPerm.copy()


        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 2. Next, we will sequentially swap the pivot's value with that of each
        #   *remaining* item in the orig. dictionary.  Then we will recursively
        #   generate all permutations of the other items in the dictionary (post-
        #   swap), and for each, we'll add the (post-swap) pivot item back into
        #   the resulting dictionary, and yield a copy of that as the next result
        #   of the generator.

    for key in d:   # Iterate through the remaining keys in the dictionary.

            # Here's where we actually do the swap of the pivot item's
            # value with that of the selected other dictionary entry.

        oldValue = pivotVal
        pivotVal = d[key]
        d[key] = oldValue

        if verbose: print("    "*level, "    Swapped into pivot:  %s --> %s" % (pivotKey, pivotVal))

            # Now we recursively iterate through all permutations of the
            # remaining items in the dictionary.

        for dPerm in dictPermutations(d, level+1):

                # Add the (modified) pivot item back into the permuted dictionary.

            dPerm[pivotKey] = pivotVal

                # Yield a copy of the current dPerm to the generator caller.

            if verbose: print("    "*level, "    Yielding permutation:  %s" % dictStr(dPerm))
            yield dPerm.copy()

def dictStr(d):
    """Returns a formatted string representation of the given dictionary."""
    s = "{\n"
    for (key, val) in d.items():
        s += f"\t{str(key)} -> {str(val)},\n"
    s += "}"
    return s


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% BOTTOM OF FILE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%