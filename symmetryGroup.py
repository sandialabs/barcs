#|%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% TOP OF FILE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%|
#|                                                                             |
#|      FILE NAME:      symmetryGroup.py           			[Python 3 module]  |
#|                                                                             |
#|      PROGRAM NAME:   BARC Element Classifier (barc)                         |
#|      MODULE NAME:    symmetryGroup                                          |
#|                                                                             |
#|      AUTHOR:         Michael P. Frank <mpfrank@sandia.gov>                  |
#|                                                                             |
#|      PROJECT:        LPS/ACS/ACI Project #41, Asynchronous Ballistic        |
#|                      Reversible Computing using Superconducting             |
#|                      Elements (ABRC/SE)                                     |
#|                                                                             |
#|      IMPORTED BY:    (4) barc.                                              |
#|      CODE LAYER:     Layer #1 (no imports from above layer #0).       	   |
#|      IMPORTS:        (0) utilities.                                         |
#|                                                                             |
#|-----------------------------------------------------------------------------+
#|                                                                             |
#|      DESCRIPTION:                                                           |
#|      ============                                                           |
#|                                                                             |
#|          This module defines a set of classes for representing and          |
#|          working with what we call "symmetry groups," by which in           |
#|          this context we mean equivalence groups of device func-            |
#|          tions that are symmetric to each other under some combina-         |
#|          tion of symmetry transformations. Each such group is iden-         |
#|          tified by an arbitrarily-selected representative "base"            |
#|          device function for the group, together with the (group-           |
#|          theoretic) group of transformations that transform that            |
#|          device function to its different (yet symmetrically equi-          |
#|          valent) representations. The identity element of the               |
#|          group is the identity transformation on device functions,          |
#|          and the (binary) group operation is the composition opera-         |
#|          tion on device transformations.                                    |
#|                                                                             |
#|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv|
"""Classes for representing simple and composite symmetry groups."""

# Exported symbols.
__all__ = [
        # Public classes:
            'SymmetryGroup',     # Base class of symmetry equivalence groups.
            'CompositeSymmetryGroup'    
                # Subclass for symmetry groups that are group products.
    ]

# Imports.
from    utilities   import count    # Counts the elements of an iterable.

# Classes:

class SymmetryGroup:    # Class of symmetry equivalence groups.

    """A "symmetry group," in our terminology, denotes a set of device
        functions (of a given device type) that are all equivalent under 
        a given symmetry transformation, or a combination of symmetry 
        transformations."""
        
    def __init__(newSymmetryGroup, deviceType, symmetryTransform,
                    baseDevice):
    
        nsg = newSymmetryGroup
        
        nsg.deviceType = deviceType
        nsg.symmetryTransform = symmetryTransform
        
        nsg.baseDevice = baseDevice
       
    
    def elements(thisSymmetryGroup):
        """Generates the elements of this group."""

        sg = thisSymmetryGroup
        st = sg.symmetryTransform

        #print(f"\tEnumerating the elements of symmetry group: {str(sg)}")

        device = sg.baseDevice
    
        yield device    # Always yield the base device, at least.
    
        while True:
        
            device = st(device)     # Transform to next device in group.
            
            #print(f"\n\nAfter doing a transformation, I got device #{device.ID()}.")
            
            if device == sg.baseDevice:
                break
            else:
                yield device
    

    def uniqueElements(thisSymmetryGroup):
        """Returns an iterable of the unique elements of this group."""
        return thisSymmetryGroup.elements()
    

    def cardinality(thisSymmetryGroup):
        """Returns the number of unique elements in this group."""
        return count(thisSymmetryGroup.uniqueElements())
    

    def contains(thisSymmetryGroup, device) -> bool:
        """Returns True if the given device is in this group."""
        sg = thisSymmetryGroup
        return sg.symmetryTransform.sameGroup(sg.baseDevice, device)


    def __str__(thisSymmetryGroup):
        """Returns a concise string representation of this group."""
        tsg = thisSymmetryGroup
        tr = tsg.symmetryTransform
        bd = tsg.baseDevice
        return f"{tr.sym}[{bd.ID()}]"


class CompositeSymmetryGroup(SymmetryGroup):

    """A "composite symmetry group" is a "product" of several different
        simple symmetry groups defined by different symmetry transformations.  
        It includes all devices that are equivalent under any sequence of
        symmetry transformations in the set."""
    
    def __init__(newCompositeSymmetryGroup, deviceType, transformList,
                    baseDevice):
        
        ncsg = newCompositeSymmetryGroup
        
        ncsg.deviceType = deviceType
        ncsg.transformList = transformList
        ncsg.baseDevice = baseDevice


    def __str__(thisSymmetryGroup):
    
        tsg = thisSymmetryGroup
    
        s = 'C('
        for tr in tsg.transformList:
            s += tr.sym + ','
        s = s[:-1] # trim trailing comma
        s += ')'
        s += f"[{tsg.baseDevice.ID()}]"
        return s


    def elements(thisSymmetryGroup):

        """Enumerating the elements of a composite symmetry group is done
            using a recursive algorithm."""

        tsg = thisSymmetryGroup
    
        #print(f"Enumerating the elements of symmetry group: {str(tsg)}")
        #print(f"Starting enumeration from base device {tsg.baseDevice.ID()}, "
        #      f"which is: {str(tsg.baseDevice)}")

        transformList = tsg.transformList
            # Note this is a list not a set just to make sure order stays consistent
        
        def _elems_recur(base, tlist):
        
            #print(f"Entering recursion from device {base.ID()} with transform list:", end='')
            #s = "["
            #for tr in tlist:
            #    s += tr.sym + ','
            #s = s[:-1]
            #print(s+']')
        
            if tlist == []:     # Should never happen, but just in case
                yield base
      
            st = tlist[0]
            
            rest = tlist[1:]

            tempGroup = SymmetryGroup(tsg.deviceType, st, base)
            
            for elem in tempGroup.elements():
            
                if len(rest) == 0:
                    yield elem
                else:
                    for dev in _elems_recur(elem, rest):
                        yield dev
        
        #print("we got here")
        
        for dev in _elems_recur(tsg.baseDevice, transformList):
            yield dev
        
        #print("we didn't get here")


    def uniqueElements(thisSymmetryGroup):

        """This is needed because generally for products of mutually
            commuting subgroups, there will be more than one way to
            generate any given element."""

        elemSet = set()
        for elem in thisSymmetryGroup.elements():
            elemSet.add(elem)
        return elemSet


    def contains(thisSymmetryGroup, device):
    
        """Returns True if and only if this symmetry group contains
            the given device.  The present implementation is iterative,
            and we could probably do better with some kind of caching
            of the set of unique group elements."""
            
        for elem in thisSymmetryGroup.elements():
            if device == elem:
                return True
                
        return False


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% BOTTOM OF FILE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%