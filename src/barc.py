#/%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% TOP OF FILE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%|
#|                                                                             |
#|      FILE NAME:      barc.py                            [Python 3 program]  |
#|                                                                             |
#|      PROGRAM NAME:   BARC Element Classifier (barc)                         |
#|                                                                             |
#|      VERSION:        v1.0 (first public release)                            |
#|                                                                             |
#|      AUTHOR:         Michael P. Frank <mpfrank@sandia.gov>                  |
#|                                                                             |
#|      PROJECT:        LPS/ACS/ACI Project #41, Asynchronous Ballistic        |
#|                      Reversible Computing using Superconducting             |
#|                      Elements (ABRC/SE)                                     |
#|                                                                             |
#|      CODE LAYER:     Layer #4 (Topmost layer of program.)                   |
#|      IMPORTS:        (3) deviceType;                                        |
#|                      (2) stateSet;                                          |
#|                      (1) symmetryGroup;                                     |
#|                      (0) utilities.                                         |
#|                                                                             |
#|                                                                             |
#|      FILE HISTORY:                                                          |
#|      =============                                                          |
#|                                                                             |
#|          2018 Oct. 16th  - Initial version, used to count 1- and 2-port     |
#|                              functions.                                     |
#|                                                                             |
#|          2022 Jan. 4th   - Starting code review/cleanup to prep. for        |
#|                              extension for element classification task.     |
#|                                                                             |
#|          2022 Jan. 20th  - Successfully completed classification of the     |
#|                              720 three-port, two-state neutral devices      |
#|                              (assuming flux conservation & symmetry).       |
#|                                                                             |
#|          2022 Jan. 22nd  - Doing code cleanup to prep. for other cases.     |
#|                                                                             |
#|          2022 Oct. 16th  - Modifications to handle flux-polarized case.     |
#|                                                                             |
#|          2022 Nov. 6th   - Modifications to do both flux-polarized and      |
#|                              flux-neutral case. Significant cleanup.        |
#|                                                                             |
#|          2023 Feb. 23rd  - Preparing for open-source release; v1.0.         |
#|                                                                             |
#|-----------------------------------------------------------------------------|
#|                                                                             |
#|      DESCRIPTION:                                                           |
#|      ============                                                           |
#|                                                                             |
#|          This program enumerates, interrelates, and classifies all          |
#|          possible ABRC/BARC functional elements of specified dimensions     |
#|          (i.e., numbers of ports, states, and pulse-type arities)           |
#|          respecting specified conservation rules and symmetry con-          |
#|          straints.                                                          |
#|                                                                             |
#|          Our first motivating application for this program is to help       |
#|          us characterize all possible 2-port and 3-port devices for a       |
#|          class of flux quanta-based implementations of BARC where all       |
#|          ports have arity (pulse type variety) 2, corresponding to mo-      |
#|          ving fluxons with polarities (-1, +1), and there can be two        |
#|          internal states, either flux-charged (-1, +1), or possibly         |
#|          flux-neutral (for example: +/-, -/+), or 3 internal states         |
#|          (-1, 0, +1), all corresponding to presence/arrangements of a       |
#|          stationary SFQ of either polarity, and where the following         |
#|          constraints are also (optionally) respected:                       |
#|                                                                             |
#|              (1) REVERSIBILITY: In the context of BARC, our focus is        |
#|                      on reversible (bijective) transition functions.        |
#|                      (Fully, not just conditionally reversible.)            |
#|                      All other functions are ignored at present.            |
#|                                                                             |
#|              (2) FLUX CONSERVATION: This constraint is relevant for         |
#|                      planar circuits with closed superconducting            |
#|                      boundaries. The total (signed) flux charge of          |
#|                      the internal state and the incident pulse is the       |
#|                      same before and after each possible transition.        |
#|                                                                             |
#|              (3) FLUX POLARITY NEGATION (F) SYMMETRY:  This constraint      |
#|                      is relevant for circuits without any DC bias cur-      |
#|                      rents or permanently trapped fluxes. This symmetry     |
#|                      states that the device behavior is identical when      |
#|                      the polarities of all (incoming, outgoing, and in-     |
#|                      ternal) flux charges are negated. We assume that       |
#|                      this inverts even flux-neutral internal states         |
#|                      (which can make sense if they're balanced pairs of     |
#|                      +,- flux).  Thus, a F (flux polarity negation)         |
#|                      transformation automatically includes an S (inter-     |
#|                      nal state exchange) transformation as well.            |
#|                                                                             |
#|          See the file ARCHITECTURE.txt for notes on the program's           |
#|          high-level organization.                                           |
#|                                                                             |
#|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv|
"""barc - Element classifier for the Ballistic Asynchronous Reversible
    Computing (BARC) paradigm. This is a command-line application.
    See barc.py source file for additional documentation in comments."""

    #/=====================================================================|
    #|  Program section 1: Imports.                        [code section]  |
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv|

        #/~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
        #| 1.1. Imports of standard Python modules. [code subsection]  |
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv|

from    enum        import  Enum, auto
    # Support for enumeration types.

from    time        import  process_time    as proctime       
    # Returns CPU time consumed so far by the current process, in seconds.
    # (We use this to measure how long certain program steps take.)


        #/~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
        #| 1.2. Imports of custom modules.          [code subsection]  |
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv|

# Imports from code layer #0:

from    utilities   import  (   # Miscellaneous utility functions.
            assignID,   # Assigns a unique ID to a hashable object.
            count       # Counts the items produced by an iterable.
        )


# Imports from code layer #1:

    #---------------------------------------------------------------------------
    #   The symmetryGroup module is important for defining the composite group G
    #   that encompasses all of the device symmetries that we are interested in.  
    #   Please note that for any given device function f, there are two subgroups 
    #   of this overall composite symmetry group G that are important to keep in
    #   mind: 
    #
    #       (1) The self-symmetry subgroup G0(f) of transforms that leave the
    #           device representation *unchanged*.  This is the group we're re-
    #           ferring to when we say that the device "exhibits X (self-) sym-
    #           metry" for some symmetry subgroup X of G0(f).
    #
    #       (2) The equivalence subgroup G'(f) of transformations that trans-
    #           form the device to a representationally distinct, but essential-
    #           ly equivalent representation. We can say "Function f is Y-symme-
    #           tric to function g" under a symmetry subgroup Y of G'(f).
    #
    #   Note that we can write G = G0(f) * G'(f) for any device function f.
    #
    #   Please note that for purposes of counting the number of equivalence 
    #   classes of devices, and determining which devices are in each class, 
    #   it's the latter type of symmetry group G'(f) that's most important, 
    #   since this is the one that lets us detect that two different device re-
    #   presentations are in fact equivalent (in the same symmetry group).

from    symmetryGroup   import  (
            SymmetryGroup,              # Constructs a simple symmetry group.
            CompositeSymmetryGroup      # Forms composite symmetry groups.
        )


# Imports from code layer #2:

    #---------------------------------------------------------------------------
    #   The stateSet module defines specific internal state sets of interest. 
    #   For now, we focus our attention on two symmetric state sets, theSymme-
    #   tricTwoStateSet and theSymmetricThreeStateSet, which represent flux 
    #   charges of {-1, +1} and {-1, 0, +1} respectively. We can also consider
    #   theSymmetricTwoHalfStateSet, in which the two flux charge states corres-
    #   pond to {-1/2, +1/2}.  However, that one is not implemented yet, since
    #   it's impossible for an isolated, fully-reversible, flux-conserving BARC 
    #   device to utilize that state set, because the total change in the stored 
    #   flux must always be a multiple of 2 flux quanta, since the sum of incom-
    #   ing and outgoing fluxons is always even (0 or +/-2). There's also theLR-
    #   StateSet, in which the two states both have zero net flux charge, but 
    #   are intended to "point" to two different ports labeled "L" (left) and 
    #   "R" (right).

from    stateSet       import (

            theSymmetricTwoStateSet,    # {-1, +1}      
                # Used e.g. in RM (Reversible Memory) cell (w/o reset).
                
            #theSymmetricThreeStateSet,  # {-1, 0, +1}
                # Used e.g. in resettable RM cell. (Not yet in scope.)
                
            theLRStateSet               # {'L', 'R'}
                # Used e.g. in Rupert's Polarized Flipping Diode (PFD).
                    
        )


# Imports from code layer #3:

    #---------------------------------------------------------------------------
    #   NOTE: The deviceType module defines various general types of BARC devi-
    #   ces (i.e., functional elements). 
    #       Initially, we were planning to restrict our attention to the Symme-
    #   tricBinaryDeviceType, in which all ports utilize a symmetric (i.e., 
    #   flux-charge-balanced) binary pulse alphabet, in which there are are two 
    #   pulse types, symbolized by -1 and +1.  These integers correspond to the 
    #   pulse's flux charge in a planar interconnect (two parallel conductors), 
    #   in units of the magnetic flux quantum Phi_0.
    #       UPDATE JAN. 2022:  Now focusing instead on a different class of de-
    #   vice types, the PositiveUnaryDeviceType ones, so as to study the posi-
    #   tive-sector behavior of neutral-state (i.e., flux-balanced) elements.

from    deviceType     import   (

            PositiveUnaryDeviceType,   
                #   Device type in which all ports have the pulse alphabet {+1}.
                #   (This is adequate for flux-neutral devices in the context
                #   of a flux-negation symmetry constraint.)

            SymmetricBinaryDeviceType    
                # Device type where all ports have the pulse alphabet {-1, 1}.

            # Later on, we might look at other device categories.
        )


    #|======================================================================
    #|  Program section 2: Class definitions.               [code section]
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        #/~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #|  Category                                        [enumeration class]
        #|
        #|      An object of class category identifies what general kind
        #|      of devices we are studying.  So far the scope of this pro-
        #|      gram includes only the following two categories of devices:
        #|
        #|          POLARIZED_STATE - Devices have two internal states,
        #|              which have opposite (+1,-1) net flux from each other.
        #|
        #|          NEUTRAL_STATE - Devices have two internal states, which 
        #|              are both neutral in terms of their net flux charge, 
        #|              but they are exchanged with each other upon a flux
        #|              negation transform. (E.g., there could be two storage 
        #|              loops with +1,-1 flux charges that can get exchanged
        #|              with each other.)
        #|
        #|      So far, all of these categories also assume that total flux is 
        #|      conserved and devices are flux-negation symmetric.  And, that 
        #|      all devices are total, deterministic and fully logically rever-
        #|      sible.  Later on we may expand the scope of this program to also 
        #|      address additional cases.
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

class Category(Enum):

    POLARIZED_STATE = auto()     
        # In this category, the two internal states have opposite (+1,-1) net flux.

    NEUTRAL_STATE = auto()        
        # Internal states both have neutral net flux, yet are swapped by flux negation.

    # (Note there are certainly many other conceivable possible device categories 
    #   that we could examine, but we haven't defined/studied them yet.

#__/ End class Category.


    #|======================================================================
    #|  Program section 2. Globals.                         [code section]
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        #/~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #|  POLARIZED_STATE, NEUTRAL_STATE                  [global constants]
        #|
        #|      These global constants just provide convenient access to 
        #|      the possible values of the Category enumeration.
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

global POLARIZED_STATE, NEUTRAL_STATE
POLARIZED_STATE = Category.POLARIZED_STATE
NEUTRAL_STATE   = Category.NEUTRAL_STATE


        #/~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #|  whichCategory: Category                         [global variable]
        #|
        #|      The whichCategory global variable identifies which general
        #|      category of devices we are currently studying: The category
        #|      of POLARIZED_STATE devices, or the category of NEUTRAL_STATE
        #|      devices?
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

global whichCategory
whichCategory = None    # Setting this to be undefined initially.
    # NOTE: Possible values include POLARIZED_STATE, NEUTRAL_STATE.


        #/~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #|  stateSet: StateSet                              [global variable]
        #|
        #|      The stateSet global variable holds an object of class State-
        #|      Set which denotes which type of state set we are currently
        #|      considering. For now, we are focusing on theLRStateSet, since
        #|      we want to explore potential variations on the toggle barrier
        #|      wherein there are two terminals L,R besides the control, and 
        #|      no change in total stored flux when the internal state is
        #|      changed.
        #|          UPDATE: Now looking also at theSymmetricTwoStateSet.
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

global stateSet
stateSet = None     # Setting this to be undefined initially.
    # Set this by calling the selectStateSet() function, defined below.


    #|======================================================================
    #|  Program section 3. Functions.                       [code section]
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        #/~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #|  selectStateSet()                                [impure function]
        #|
        #|      The selectStateSet() function sets up the value of the state-
        #|      Set global variable based on the current value of the which-
        #|      Category global variable.
        #|
        #|  Uses globals:   whichCategory
        #|  Sets globals:   stateSet
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

# Call this function after setting whichCategory to set stateSet appropriately.
def selectStateSet():
    """This side-effecting function sets the global stateSet based on
        the current value of the whichCategory global."""

    global whichCategory, stateSet      # We manipulate these globals.

    if whichCategory is POLARIZED_STATE:
        stateSet = theSymmetricTwoStateSet     # {-1, +1} - Like reversible RM cell.
        #stateSet = theSymmetricThreeStateSet   # {-1, 0, +1} - Like resettable RM cell.
            # This state set is not yet used.
    
    elif whichCategory is NEUTRAL_STATE:
        stateSet = theLRStateSet
            # A pair of neutral flux-charge states.
            # (Could correspond to a left-right symmetry).

    # NOTE: No other cases are handled at present.

#__/ End function selectStateSet().


        #/~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #|  enumerateSymmetryGroups() -> Iterable                   [function]
        #|
        #|      The enumerateSymmetryGroups() function returns an iterable
        #|      (specifically, a list) that enumerates the symmetry equiva-
        #|      lence groups classifying the given device functions, accor-
        #|      ding to the given list of relevant symmetry transforms.
        #|
        #|  Required arguments:
        #|  ===================
        #|
        #|      devFuncList                                     [iterable]
        #|
        #|          This should be an iterable of device functions
        #|          that the caller currently wants us to classify.
        #|
        #|      symmetryTransforms                              [iterable]
        #|
        #|          This should be an iterable of primitive (i.e.,
        #|          not composite) symmetry transforms that should
        #|          be utilized to construct the symmetry groups.
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

def enumerateSymmetryGroups(devFuncList, symmetryTransforms):

    """This function divides up the provided list of device functions
        into symmetry groups according to the provided list of symmetry
        transformations. It returns the list of equivalence groups."""
    
    #print("Entering enumerateSymmetryGroups()...")
    #print("I was given this list of device functions:")
    #print('\t', deviceFunctions)
    
    knownSymmetryGroups = []     # No symmetry groups are known initially.
    
    # The index variable i is just used to count the raw device functions studied.
    i = 0

    for deviceFunction in devFuncList:

        i += 1
        
        print(f"\nExamining device function #{i}: {str(deviceFunction)}")

            # First, let's check whether this function's symmetry group
            # has already been found.
    
        alreadyKnown = False
        for knownSymmetryGroup in knownSymmetryGroups:
            if knownSymmetryGroup.contains(deviceFunction):
                # This function's group has already been identified.
                alreadyKnown = True     
                break
        
        if alreadyKnown:
            print("    It's already in a known symmetry group.")
        
        else:   # This device function hasn't been classified yet.

            #|--------------------------------------------------------
            #| If we get here, then the device's symmetry group hasn't
            #| already been identified, so we create it now.
        
            deviceType = deviceFunction.type    # Get the device type.
        
                # If there's only one symmetry transform to consider, then
                # we just create an ordinary (base) symmetry group.

            if len(symmetryTransforms) == 1:    # Only one transform in list.
                symmetryTransform = symmetryTransforms[0]
                newSymmetryGroup = SymmetryGroup(deviceType, symmetryTransform,
                                    deviceFunction)
            
                # Otherwise, we create a composite symmetry group that
                # includes all possible combinations of transforms.

            else: # multiple symmetry transforms to consider.
                newSymmetryGroup = CompositeSymmetryGroup(deviceType,
                                    symmetryTransforms, deviceFunction)
            
            print("    It's in a new symmetry group!")
            
            knownSymmetryGroups += [newSymmetryGroup]

        #__/ End if alreadyKnown... else...

    #__/ End loop over device functions.

    return knownSymmetryGroups

#__/ End function enumerateSymmetryGroups().


        #|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #|  characterizeDeviceFunctions()                           [function]
        #|
        #|      This function takes a number of ports N as input, then does
        #|      the work of characterizing all of the N-port devices of the
        #|      current category.  Before calling, the global variable state-
        #|      Set should be assigned to the set of internal state labels to
        #|      be used. Also whichCategory should be set to the device cate-
        #|      gory.
        #|
        #|  Uses globals:   whichCategory, stateSet
        #|
        #|  Required arguments:
        #|  ===================
        #|
        #|      nTerminals [non-negative integer] -
        #|
        #|          This identifies how many I/O ports the devices
        #|          to be characterized should have.
        #|
        #|  Optional arguments:
        #|  ===================
        #|
        #|      conserveFlux [boolean] -
        #|
        #|          If set to False, device functions that don't
        #|          conserve flux are allowed. (WARNING: This can
        #|          dramatically increase runtime and memory 
        #|          requirements!)  By default, it is True.
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

def characterizeDeviceFunctions(nTerminals, conserveFlux=True):
    # If conserveFlux=True (default), then we'll skip functions 
    # that don't conserve flux between input and output syndromes.

    """Characterizes all of the possible reversible functional element behaviors
        for devices having N=<nTerminals> bidirectional I/O ports and internal
        state set <stateSet> (specified in a module-level global variable). Also
        ensures flux is conserved, unless conserveFlux is set to False."""

    #|--------------------------------------------------------------------------
    #| Construct the N-terminal deviceType to be explored. When the current de-
    #| vice category is polarized-state devices, the deviceType should use the 
    #| symmetric binary alphabet {-1, +1} for its I/O ports, and the currently-
    #| selected state set.  Alternatively, in the case of neutral-state devices,
    #| we use the positive unary alphabet {+1}, because the device behavior on 
    #| negative pulses can be inferred due to F symmetry.

        # If the currently-selected category is POLARIZED_STATE, then
        # we'll select the corresponding symmetric binary device type.

    if whichCategory is POLARIZED_STATE:
        deviceType = SymmetricBinaryDeviceType(nTerminals, stateSet)

        # If the currently-selected category is NEUTRAL_STATE and we're
        # conserving flux, then it suffices to explore just the sector
        # in which all I/O signals are positive, since the device can't
        # change the I/O pulse polarity, and the behavior in the negative-
        # pulse sector follows from the positive-pulse behavior by flux
        # negation symmetry.

    elif whichCategory is NEUTRAL_STATE and conserveFlux is True:
        deviceType = PositiveUnaryDeviceType(nTerminals, stateSet)

    # NOTE: No other cases are handled yet!

        #|----------------------------------------------------------------------
        #| Retrieve the value of the 'dimensions' property for that device type.
        #| This is an object that summarizes the device type's dimensions 
        #| (#states, #ports, port arities).

    deviceDims = deviceType.dimensions

        #|----------------------------------------------------------
        #| This displays a representation of the selected 
        #| dimensions. How to do this is defined by the __str__() 
        #| method of the DeviceDimensions class (defined in 
        #| deviceDimensions.py).

    print('#'*80)
    print(f"Currently studying devices in the {whichCategory.name} category.")
    print("Enumerating devices with dimensions: %s" % deviceDims)

        #|----------------------------------------------------------
        #| Next we actually do the enumeration task, counting how 
        #| many devices there are of the selected type, and we 
        #| also measure how much time this takes.

    start = proctime()     # Note start time of task.

        # The problem here is that .deviceFunctions()
        # returns a generator, which can't be reset.
        # So instead of running it now, we copy it
        # to run later.
    
        # Retrieve a generator for all "interesting" functions of
        # the given device type. (NOTE: The iterator returned by
        # this generator may be very slow to run!)
    deviceFunctions = deviceType.deviceFunctions

        # Convert the generator to a list. (Potentially slow part.)
    devFuncList = list(deviceFunctions(conserveFlux))

    # The following assigns numeric IDs to the device functions found.
    #print("\nThe device functions are:\n")
    i=1
    for devFunc in devFuncList:
        #print(f"Device #{i} is: {str(devFunc)}")
        assignID(devFunc,i)
        i += 1

        # This enumerates all of the possible distinct fully-
        # reversible functional behaviors for devices of the 
        # given device type, and counts how many of them exist.
    nDeviceFunctions = count(devFuncList)
    
    end = proctime()       # Note end time of task.
    
        #|----------------------------------------------------------
        #| Display results.

        # Display the run time for this task.
    print("This took %f seconds." % (end - start))

        # Display how many devices there are of this type.
    print("There are %d nontrivial devices (raw count)." % nDeviceFunctions)

    # Display devices and their symmetry properties.
    print("\nThe device functions are:\n")
    for devFunc in devFuncList:
        id = devFunc.ID()
        print('-'*70)
        print(f"Device #{id} is: {str(devFunc)}")
        devFunc.showSymmetries()

        #|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #| Generate the composite symmetry groups of interest.
        #| These groups are selected to encompass all of the
        #| trival transformations for up to 3-port reversible
        #| functions with 2 flux-neutral internal states.
        #| UPDATE: Now doing it for flux-polarized internal states.
    
    drt = deviceType.directionReversalTransform()
        # Inverting the transition function leaves us in the group.
        # (It's intuitive that if a given function is reversibly
        # implementable, its reverse also should be. Prove this?)
    
    # Define the state-negation transform; however, we won't end up
    # considering them in the case of flux-polarized devices. Because, 
    # if we're conserving flux, and any transition changes the state, 
    # then after negating states, the transition won't conserve flux.
    snt = deviceType.stateNegationTransform()
        # Exchange of state labels leaves us in the group.
        # (Assume that negating flux-neutral states does this).
    
    psts = list(deviceType.portSwapTransforms())
        # It's somewhat redundant to include all of these swaps:
        # Note for 3 ports, there are 8 combinations of swaps, but 
        # only 6 permutations. This shouldn't increase our run time 
        # by very much, though.
    
    #prts = list(deviceType,portRotateTransforms())
        # We don't actually need any of these, because port swaps can 
        # generate them.

    # Here we collect a list of transforms that we consider "interesting"
    # (i.e., relevant to defining our symmetry-equivalence groups).
    # For our present purposes, the potentially interesting transforms are:
    #   * Direction Reversal Transform:     D
    #   * State Negation Transform:         S       <- Only for flux-neutral states.
    #   * Port Exchange Transforms:         E(i,j)
    #   * Port Rotate Transforms:           R(o)
    #       - However, for 3 ports at least, any of the R(o)'s can 
    #           be generated by combining E(i,j)'s, so we skip them.

    # First, we'll consider the direction-reversal transform to always be 
    # among the set of interesting transforms. Note this assumes there isn't 
    # some reason why the forward direction might turn out to be easier or 
    # harder to implement than the reverse direction.
    interestingTransforms = [drt]

    # Next, we'll consider the state-exchange transform to be in scope, but
    # *only* if either we aren't bothering to conserve flux, or we're currently
    # studying neutral-state devices (for which a state exchange won't affect)
    # flux conservation. This is because, in the case of polarized states, it's
    # impossible for both a given function and its state-exchanged dual to both
    # conserve flux, unless the state is never changed (non-primitive device).
    if (not conserveFlux) or (whichCategory is NEUTRAL_STATE):
        interestingTransforms += [snt]

    # Next, we'll consider the port-swap transforms to be in scope. However,
    # we can skip the rotation transformations, because any rotation for 3-port
    # devices can just be generated by a pair of port-swaps.
    interestingTransforms += psts # + prts   <-- Rotations commented out b/c redundant.
    
    # This was the original code for the neutral-state case.
    #interestingTransforms = [drt, snt] + psts # + prts

    print("\nEnumerating symmetry groups under these combined transforms:")
    for transform in interestingTransforms:
        print(f"\t{transform.sym} {transform.desc}")

    # Really we should probably be calling these "equivalence groups," but oh well.
    symmetryGroups = enumerateSymmetryGroups(devFuncList, 
                        interestingTransforms)

        # Describe the results.
    nGroups = len(symmetryGroups)
    print(f"\nI found {nGroups} symmetry groups.")
    print("Their respective sizes are:")
    for i in range(nGroups):
        groupNum = i+1
        group = symmetryGroups[i]
        groupSize = group.cardinality()
        print(f"\tGroup #{groupNum} contains {groupSize} functions.")
    
        # Next show a representative function from each group.
    print()
    print('='*70)
    print("Here's a list of functions & a representative function from each group:\n")
    for i in range(nGroups):
        groupNum = i+1
        group = symmetryGroups[i]
        size = group.cardinality()
        print('-'*50)
        print(f"Symmetry group #{groupNum} has {size} functions:")
        for func in group.uniqueElements():
            print(f"\tFunction #{func.ID()}.")
        for func in group.uniqueElements():
            print(f"\nExample: Function #{func.ID()} = " + str(func))
            func.showSymmetries()
            break   # Stop after first function.


def tryAllSizes():
    """Performs our main classification task for devices
        of all sizes from 1 to 3 ports."""

    # Do our main task for devices with 1, 2, and 3 ports.
    portsList = [1, 2, 3]

    # NOTE: The only case which is really slow so far is for devices
    # with polarized states and 3 ports -- this takes several hours.

    for nPorts in portsList:
        characterizeDeviceFunctions(nPorts, conserveFlux=True)


    #|======================================================================
    #|  Program section 3. Main Program.                    [code section]
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

# First, we'll analyze the case of devices with polarized states.
whichCategory = POLARIZED_STATE
selectStateSet()    # Selects state set based on whichCategory.
tryAllSizes()       # Try all sizes of devices from 1-3 ports.

# Next, we'll analyze the case of devices with neutral states.
whichCategory = NEUTRAL_STATE
selectStateSet()    # Selects state set based on whichCategory.
tryAllSizes()       # Try all sizes of devices from 1-3 ports.


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% BOTTOM OF FILE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%