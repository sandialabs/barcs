#|%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% TOP OF FILE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%|
#|                                                                             |
#|      FILE NAME:      deviceType.py                       [Python 3 module]  |
#|                                                                             |
#|      PROGRAM NAME:   BARC Element Classifier (barc.py)                      |
#|      MODULE NAME:    deviceType                                             |
#|                                                                             |
#|      AUTHOR:         Michael P. Frank <mpfrank@sandia.gov>                  |
#|                                                                             |
#|      PROJECT:        LPS/ACS/ACI Project #41, Asynchronous Ballistic        |
#|                      Reversible Computing using Superconducting             |
#|                      Elements (ABRC/SE)                                     |
#|                                                                             |
#|      IMPORTED BY:    (4) barc.                                              |
#|      CODE LAYER:     Layer #3 (no imports from modules above layer #2).     |
#|      IMPORTS:        (2) deviceFunction;                                    |
#|                      (1) pulseAlphabet, pulseType, transitionFunction;      |
#|                      (0) characterClass, deviceDimensions, dictPermuter,    |
#|                          signalCharacter, symmetryTransform, syndrome,      |
#|                          utilities.                                         |
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
#|          This module defines classes for various "device types."  In        |
#|          the context of the BARC Element Classifier program, a device       |
#|          refers to a functional element of a BARCS circuit, and a de-       |
#|          vice type is a broad category of elements sharing specified        |
#|          dimensions.  Here, by a "dimension" we mean a parameter that       |
#|          helps us determine how many possible devices there are in          |
#|          the given category.  The dimensions of BARC devices include        |
#|          the following (and, see the deviceDimensions module for more       |
#|          details):                                                          |
#|                                                                             |
#|              * The number of distinct internal states the device has.       |
#|                                                                             |
#|              * The number of distinct I/O ports (sometimes informally       |
#|                  called "terminals") the device has.                        |
#|                                                                             |
#|              * For each I/O port, the number of distinct pulse types        |
#|                  that are supported by that port. (In general, we           |
#|                  assume that ports in general are bidirectional, so         |
#|                  that each pulse type may pass in either direction          |
#|                  through the port, in or out.)                              |
#|                                                                             |
#|          In addition to having specified dimensions, a device type          |
#|          is also associated with a specific set of labels for its           |
#|          internal states, and, for each of its terminals, a specific        |
#|          symbolic alphabet for labeling the pulse types supported on        |
#|          that terminal.                                                     |
#|                                                                             |
#|                                                                             |
#|      PUBLIC NAMES DEFINED:                                                  |
#|      =====================                                                  |
#|                                                                             |
#|          This module defines the following public names:                    |
#|                                                                             |
#|              DeviceType [class] - This is the top-level superclass          |
#|                  of the DeviceType class hierarchy. An object of            |
#|                  class DeviceType knows its dimensions, its state           |
#|                  set, and the alphabet of each of its I/O ports.            |
#|                                                                             |
#|              UniformArityDeviceType [class] - A subclass of class           |
#|                  DeviceType in which all I/O ports share the same           |
#|                  arity and also the same pulse-type alphabet.               |
#|                                                                             |
#|              PositiveUnaryDeviceType [class] - A subclass of the            |
#|                  UniformArityDeviceType class in which the pulse-           |
#|                  type alphabet is the positive unary alphabet {+1}          |
#|                  (appropriate for encoding the positive-flux sector         |
#|                  of flux-conserving, flux-neutral devices operating         |
#|                  on polarized fluxons).                                     |
#|                                                                             |
#|              SymmetricBinaryDeviceType [class] - A subclass of              |
#|                  UniformArityDeviceType in which the pulse type             |
#|                  alphabet is the symmetric binary alphabet {-1, +1}         |
#|                  (appropriate for encoding via polarized fluxons).          |
#|                                                                             |
#|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv|

    #|======================================================================
    #| Module section 0. Exports.                           [code section]
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    
    # This special module attribute gives the list of names that are 'exported'
    # from this module, i.e., that will be imported into an importing module 
    # when that module does 'from <thisModule> import *'.
__all__ = [
        #'DeviceType',                  # Not currently used by other modules.
        #'UniformArityDeviceType',      # Not currently used by other modules.
        'PositiveUnaryDeviceType',      # Used by barc module (main program).
        'SymmetricBinaryDeviceType'     # Used by barc module (main program).
    ]

    #|======================================================================
    #|  Module section 1. Imports.                          [code section]
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        #/~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #| Imports from code layer #0.

from characterClass     import  CharacterClass, UniformCharacterClass
    # An object of type UnformCharacterClass describes the specifications
    # for signal characters suitable for uniform-arity device types (those
    # in which all ports have the same degree of pulse-type multiplicity).
    # This is the only case supported at present.
    #   [USED IN: UniformArityDeviceType initializer.]

from deviceDimensions   import  DeviceDimensions     # [Class]
    # An object of class DeviceDimensions specifies the dimensions of
    # a device, that is, its number of internal states, number of ports,
    # and the arities of its ports.
    #   [USED IN: DeviceType initializer.]

from dictPermuter       import  dictPermutations     # [Function]
    # The dictPermutations() function returns a generator for all 
    # possible permutations of a given dictionary.
    #   [USED IN: DeviceType.deviceFunctions() method.]

from signalCharacter    import  SignalCharacter
    # An object of class signalCharacter characterizes an I/O signal pulse
    # incident to a device of given dimensions; this information includes
    # both the index of the port on which the given is incident, as well
    # as the type of pulse. The signal character does not itself specify
    # whether this is an input or an output pulse; that is assumed to be
    # clear from the context.
    #   [USED IN: DeviceType.syndromes() method.]

from    symmetryTransform   import (
            DirectionReversalTransform,     # D swaps inputs with outputs.
            FluxNegationTransform,          # F negates all fluxes (I/O & state).
            StateNegationTransform,         # S negates/swaps just the states.
            PortExchangeTransform,          # E(p1,p2) exchanges two ports.
            PortRotationTransform           # R(o) rotates the ports.
    ) # We need these constructors to create the transforms for this device.

from syndrome           import  Syndrome             # [Class]
    # An object of class Syndrome (for a device of given dimensions) 
    # specifies an I/O syndrome. The consists of an I/O signal character 
    # together with a device state. Whether this is an input or output
    # syndrome is not specified (it's assumed to be clear in context).
    #   [USED IN: DeviceType.syndromes() method.]

from utilities          import  isOdd   
    # Returns True if its argument is an odd number


        #/~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #| Imports from code layer #1.

from pulseAlphabet      import (

        thePositiveUnaryPulseAlphabet,      # {+1}
            # This is a restricted pulse-type alphabet which is appropriate
            # for characterizing functionalities in which all I/O utilizes
            # positive-polarity fluxons only. This is appropriate for
            # characterizing the positive-polarity sector of functionality
            # for flux-conserving elements in which internal flux states
            # are neutral, since such elements cannot change the polarity
            # of any interacting fluxons.

        theSymmetricBinaryPulseAlphabet,    # {-1, +1}
            # This is the standard symbol alphabet we'll generally use to 
            # denote the pulse type for pulses consisting of LJJ fluxons.
            # The possible symbols are -1, +1, where each symbol is a 
            # signed integer counting the number of magnetic flux quanta 
            # contained in this pulse, where the sign indicates field 
            # direction or polarity. For now, we assume all fluxons 
            # contain exactly 1 magnetic flux quantum, of either 
            # polarity.

    ) # These are used in defining our PositiveUnaryDeviceType
      # and SymmetricBinaryDeviceType classes.

from pulseType          import PulseType
    # An object of class PulseType represents a specific type of pulses 
    # (which,in our context, means a specific fluxon polarity. We'll need 
    # to construct PulseType objects when generating I/O syndromes.
    #   [USED IN: DeviceType.syndromes() method.]

from transitionFunction import TransitionFunction   # [Class]
    # An object of class TransitionFunction specifies an I/O relation
    # (map from input syndromes to output syndromes) for a given device
    # type.
    #   [USED IN: DeviceType.deviceFunctions() method.]


        #/~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #| Imports from code layer #2.

from deviceFunction     import DeviceFunction       # [Class]
    # An object of class DeviceFunction specifies both the device type
    # and exact transition function for a particular functional element
    # behavior.
    #   [USED IN: DeviceType.deviceFunctions() method.]


    #/======================================================================
    #|  Module section 3: Class definitions.                [code section]
    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        #/~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #|  DeviceType                                  [module public class]
        #|
        #|      An instance of class DeviceType defines a specific device
        #|      "type."  A device type is characterized by its dimensions
        #|      (see the deviceDimensions module), a pulse alphabet for
        #|      each port (see the pulseAlphabet module), and an internal
        #|      state set (see the stateSet module).
        #|
        #|      Note that a deviceType object by itself does *not* identify
        #|      any specific functional behavior for the device. For that,
        #|      see the deviceFunction module.
        #|
        #|  Additional documentation:
        #|      
        #|      See inside the class definition for comments documenting
        #|      the DeviceType class's:
        #|
        #|          * Private data members.
        #|          * Instance public properties.
        #|          * Instance public methods.
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

class DeviceType:
    """An instance of class DeviceType defines a specific device type.
        A device type has dimensions, a pulse alphabet for each port,
        and an internal state set."""

    isUnary = False     # Are all I/O ports' pulse types unary? No by default.

    #/~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #|  Private data members of objects of class DeviceType:
    #|
    #|      ._dimensions [DeviceDimensions] -
    #|
    #|              Specifies the dimensions (# of ports and states) of 
    #|              this particular deviceType.
    #|
    #|      ._characterClass [CharacterClass] -
    #|
    #|              A characterClass object specifies the set of signal 
    #|              characters for this device type.  Each signal character
    #|              specifies a possible I/O event (combination of a port 
    #|              ID and an allowed pulse type for that port).
    #|
    #|      ._pulseAlphabets [tuple] -
    #|
    #|              A tuple specifying the pulse alphabet objects assigned
    #|              to each of the device's ports.
    #|
    #|      ._stateSet [StateSet] -
    #|
    #|              The stateSet object representing the set of internal 
    #|              states supported by this particular deviceType.
    #|
    #\~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(deviceType, pulseAlphabets, stateSet):

        """Initializer for new instances of class DeviceType. Takes
            an iterable of pulse alphabets, and the internal state set
            as arguments."""

        #print(f"Creating DeviceType(pulseAlphabets={pulseAlphabets}, "
        #    f"stateSet={stateSet})...")

            # Count the number of "terminals" (ports) - This is given by
            # the length of the pulseAlphabets iterable.
        nTerminals = len(pulseAlphabets)

            # Construct a tuple of port arities - these are given by the
            # .arity properties of the ports' respective pulseAlphabets.
        arities = tuple(map(lambda ab: ab.arity, pulseAlphabets))

            # Construct the deviceDimensions object for this device type.
            # This specifies the number of terminals (ports), a tuple of port
            # arities, and the size of the state set.
        devDims = DeviceDimensions(nTerminals, arities, stateSet.cardinality)
        
            # Initialize this new instance's private data members appropriately.
        deviceType._dimensions     = devDims
        deviceType._stateSet       = stateSet
        deviceType._pulseAlphabets = tuple(pulseAlphabets)
        
            # If this device type does not already have a character class
            # assigned, then generate one that's appropriate for the number
            # of terminals and the list of pulse alphabets for this device.
        if not hasattr(deviceType, '_charClass'):
            charClass = CharacterClass(nTerminals, pulseAlphabets)
            deviceType._charClass       = charClass

    # Equivalence operator for device types. We declare two device types to be
    # equivalent iff both their state sets and pulse alphabets are equivalent.

    def __eq__(thisDeviceType, otherDeviceType):
        
        dt1 = thisDeviceType
        dt2 = otherDeviceType
        
        return ((dt1.stateSet == dt2.stateSet) and
                (dt1.pulseAlphabets == dt2.pulseAlphabets))
    
    # Hash function for device types. This is obtained by hashing the tuple
    # of the device type's state set followed by its pulse alphabet.

    def __hash__(thisDeviceType):
        dt = thisDeviceType
        return hash((dt.stateSet, dt.pulseAlphabets))

        #/======================================================================
        #|  Instance public properties for class DeviceType:
        #|
        #|      .characterClass [CharacterClass] -
        #|
        #|          The characterClass object that specifies the type
        #|          of I/O signal characters that describe the possible
        #|          input and output signals for this device.
        #|
        #|      .dimensions [DeviceDimensions] -
        #|
        #|          The deviceDimensions object that specifies the
        #|          dimensions (complexity specifications) for devices
        #|          of this type.
        #|
        #|      .fluxNeutral [bool] -
        #|
        #|          True iff all of the internal states of devices of this 
        #|          type contain zero net flux.
        #|
        #|      .nPorts [int] -
        #|
        #|          The number of ports that devices of this type have.
        #|
        #|      .pulseAlphabets [iterable] -
        #|
        #|          An iterable of the pulse alphabets for the device's
        #|          ports (in canonical order).
        #|
        #|      .stateSet [StateSet] -
        #|
        #|          The stateSet object specifying the set of internal
        #|          states that devices of this type may be in.
        #|
        #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    @property
    def characterClass(deviceType) -> CharacterClass:
        """This property gives the device's characterClass object."""
        return deviceType._charClass

    @property
    def dimensions(deviceType) -> DeviceDimensions:
        """This property gives the device's deviceDimensions object."""
        return deviceType._dimensions

    @property
    def fluxNeutral(deviceType) -> bool:
        """Boolean property; True iff all internal states of the device
            contain 0 net flux."""
        return deviceType.stateSet.fluxNeutral

    @property
    def nPorts(deviceType) -> int:
        """This property gives the device's number of ports."""
        return deviceType.dimensions.nPorts

    @property
    def pulseAlphabets(deviceType):
        """This property gives an iterable of the pulse alphabets
            for the device's ports (in order)."""
        return deviceType._pulseAlphabets

    @property
    def stateSet(deviceType):
        """This property gives the device's stateSet object."""
        return deviceType._stateSet


        #/======================================================================
        #|  Instance public methods for class DeviceType:
        #|
        #|      .deviceFunctions() [iterator] -
        #|
        #|          This generator method returns an iterator which
        #|          enumerates all possible (reversible) device functions
        #|          of this type. (However, we will skip functions that
        #|          are trivial or non-primitive in various respects.)
        #|
        #|      .directionReversalTransform() [DirectionReversalTransform] -
        #|
        #|          Returns the DirectionReversalTransform object (which
        #|          is conceptually an operator) for devices of this type.
        #|
        #|      .reportableTransforms() [iterator] -
        #|
        #|          This generator method returns an iterator that
        #|          enumerates all of the symmetry transformations that
        #|          are "worth reporting about" for this device type.
        #|
        #|      .stateNegationTransform() [StateNegationTransform] -
        #|
        #|          Returns the StateNegationTransform object (which is
        #|          conceptually an operator) for devices of this type.
        #|
        #|      .syndromes() [iterator] -
        #|
        #|          This generator method returns an iterator which
        #|          enumerates all possible I/O syndromes (here, not 
        #|          distinguishing between input and output syndromes)
        #|          for this particular device type.
        #|
        #\vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    # Generates all device functions of this type.

    def deviceFunctions(deviceType, conserveFlux=True):
        # NOTE: If conserveFlux is True, then transition functions
        # that don't conserve flux will be automatically skipped.

        """This generator method returns an iterator which enumerates
            all possible (reversible) device functions of this given
            device type."""

        # NOTE: Eventually we'll want to expand the scope of this study to
        # also include all conditionally reversible functions, and these
        # are not all going to be permutations like we assume below; but 
        # that is out of scope for us at the moment.

        # We start with a device function that's just the identity 
        # function (a function that leaves all I/O syndromes unchanged).

        identityDeviceFunction = DeviceFunction(deviceType)
            # NOTE: This function never changes the pulse polarity or internal
            # state, and all ports just reflect.

        print(f"Starting with identity function: {str(identityDeviceFunction)}")

        nPerms = nFCons = nFSymm = nNonTriv = nDynState = nAtomic = 0

        # Now, we'll try all permutations of that function's IO map.
        for ioMap in dictPermutations(identityDeviceFunction.transitionFunction.ioMap):   
                # Note: Could add verbose=True to arg list to see more diagnostics.

            nPerms += 1

            # Convert the raw IO map (dictionary) to a transition-function object.
            transitionFunction = TransitionFunction(deviceType, ioMap)

            # Okay, now first, if we're supposed to be conserving flux, and the 
            # given transition function does not conserve flux, then it isn't a 
            # valid device function, and we skip it.
            if conserveFlux:
                if not transitionFunction.conservesFlux():
                    continue
                nFCons += 1

            # Alright, now let's create a proper device-function object out of 
            # that transition function.
            df = DeviceFunction(deviceType, transitionFunction)

            # (NOTE: The following is really only relevant if both states and I/O 
            # pulses are polarized.)
            # Skip functions that aren't flux-negation-symmetric -- because we
            # believe that all implementable functions (without external bias
            # or extra trapped fluxes) must be flux-negation-symmetric.
            if not deviceType.isUnary:
                if not df.symmetricUnder(FluxNegationTransform(deviceType)):
                    continue
                nFSymm += 1

            # ...and we skip devices that have a port that's "inactive" (always 
            # reflects and never changes the state), because those devices are 
            # equivalent to a device with one fewer port, plus a separate 
            # reflector -- i.e. they aren't primitive devices.
            if df.hasInactivePort():
                continue

            nAtomic += 1

            # Here, we also skip devices that don't ever change their internal 
            # state (because they aren't primitive devices, since they're 
            # equivalent to a pair of stateless devices).
            if not df.changesState():
                continue

            nDynState += 1

            # Skip the state-reversal-symmetric functions -- these are considered 
            # 'trivial' because the internal state doesn't matter at all and can
            # be omitted (i.e. this device is equivalent to a stateless one).
            # (The device doesn't ever use the state, and can, at most, toggle the
            # state, but with no effect on subsequent behavior.)
            if df.symmetricUnder(StateNegationTransform(deviceType)):
                continue

            nNonTriv += 1

            # NOTE: THE FOLLOWING TEST ISN'T NEEDED, AND IT ELIMINATES TOO MUCH:
            # ...and we skip devices that don't ever change the I/O port of the 
            # pulse (the N-port RM cells are the only nontrivial, primitive devices
            # that don't, but we already know how to make those).
            #if not df.changesPort():
            #    continue

            # If we made it through the above gauntlet of tests, then this is a
            # "good" (i.e. worth studying) transition function, so now yield it.
            yield df
        
        print(f"There were {nPerms} permutations (raw transition functions).")
        n = nPerms

        if conserveFlux:
            print(f"\t(If we filter out {n - nFCons} non-flux-conserving ones, we have...)")
            print(f"{nFCons} of them are flux-conserving device functions.")
            n = nFCons

        if not deviceType.isUnary:
            print(f"\t(If we filter out {n - nFSymm} non-flux-negation-symmetric ones, then...)")
            print(f"{nFSymm} of those device functions are flux-negation symmetric.")
            n = nFSymm

        print(f"\t(If we filter out {n - nAtomic} non-atomic functions, we have...)")
        print(f"{nAtomic} of those device functions are atomic functional primitives.")
        n = nAtomic

        print(f"\t(If we filter out {n - nDynState} that don't change the state, then...)")
        print(f"{nDynState} of those device functions change the state dynamically.")
        n = nDynState

        print(f"\t(If we filter out {n - nNonTriv} of those that don't use the state, then...)")
        print(f"{nNonTriv} of those device functions use the state non-trivially.")
        n = nNonTriv
    
    #__/ End method deviceType.deviceFunctions().

    # Generator for I/O syndromes for this device type.

    def syndromes(deviceType):

        """This generator method returns an iterator which enumerates all 
            possible I/O syndromes (not distinguishing between input and
            output syndromes) for this particular device type."""

        charClass = deviceType.characterClass
        for portIndex in range(deviceType.dimensions.nPorts):
            pulseAlphabet = deviceType.pulseAlphabets[portIndex]
            for symbol in pulseAlphabet.symbols:
                pulseType = PulseType(pulseAlphabet, symbol)
                for state in deviceType.stateSet:
                    yield Syndrome(SignalCharacter(portIndex, pulseType,
                                                    charClass), 
                                    state)

    # The methods below construct and return transforms that are defined
    # for all device types. (We could have made these properties instead
    # of functions, but we didn't bother.)

    def directionReversalTransform(deviceType):

        """Returns the direction-reversal (D) transform for this device type,
            which just inverts the transition function, i.e., exchanges the 
            roles of the input and output syndromes."""

        return DirectionReversalTransform(deviceType)

    def stateNegationTransform(deviceType):

        """Returns the state-negation (S) transform for this device type.
            This exchanges the roles of the two states with each other."""

        # NOTE: In the present context of flux-conserving devices,
        # this one really only makes sense for flux-neutral state sets.
        # That is, if the transition function modifies the state at all,
        # and the state set isn't flux-neutral, then state negation will
        # cause the resulting device to violate flux conservation.

        return StateNegationTransform(deviceType)

    def reportableTransforms(thisDeviceType):

        """This method returns an iterable of symmetry transforms 
            that are relevant for this particular device type."""

        # This base implementation of the reportableTransforms() method returns
        # the D (direction reversal) transform, since it applies to all device
        # types, and the S (state negation) transforms in the case of device
        # types with a flux-neutral state set (for which the state labels don't
        # matter). Subclasses should add additional transforms to this list as 
        # appropriate.

        dt = thisDeviceType

        # Initialize the reportable transforms list with just the D transform.
        rts = [dt.directionReversalTransform()]

        # Note that we skip the state-negation transform in the case of 
        # non-flux-neutral state alphabets. (See the note in the method
        # definition of .stateNegationTransform() above to see why.)
        if dt.fluxNeutral:
            # Add the S (state negation) transform to the list.
            rts += [dt.stateNegationTransform()]

        # NOTE: Subclasses should add more items to this list.
        return rts



# The following subclass of DeviceType specializes it for the case where all
# I/O ports have the same arity (and, we assume, the same pulse alphabet).
# This will always be the case for now -- for example, either all ports only
# support +1 pulses (see the PositiveUnaryDeviceType subclass, below), or all 
# ports support both +1,-1 pulses (see the SymmetricBinaryDeviceType subclass).

class UniformArityDeviceType(DeviceType):

    """Subclass of DeviceType in which all of the device's ports have the same 
        arity and the same pulse alphabet as each other."""

    #/~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #|  Note: This subclass utilizes one new private instance attribute:
    #|
    #|      ._pulseAlphabet [PulseAlphabet] -
    #|
    #|          The pulseAlphabet object describing the pulse-type alphabet 
    #|          utilized by all of this device's ports.
    #|
    #|  which may be referenced, where appropriate, in place of 
    #|  ._pulseAlphabets. (However, we do still initialize the
    #|  ._pulseAlphabets data member as well.)
    #\~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    # The default pulse-type alphabet to be used for all new device types of 
    # a given subclass, if not specified in the constructor call.
    defaultPulseAlphabet = None
        # Note: Subclasses may override this class-level variable.

    # The default instance initializer for the UniformArityDeviceType
    # delegates most of its actual work to the superclass initializer.
    def __init__(deviceType, nPorts, stateSet, pulseAlphabet=None):
        # NOTE: The pulseAlphabet argument here is optional because
        # subclasses may specify particular default pulse alphabets
        # by overriding the defaultPulseAlphabet class variable (above).
        
        # Use the default pulse-type alphabet, if not otherwise specified 
        # in the constructor call.
        if pulseAlphabet is None:
            pulseAlphabet = deviceType.defaultPulseAlphabet
        
        #print(f"Creating UniformArityDeviceType(nPorts={nPorts},"
        #    f"stateSet={stateSet}, pulseAlphabet={pulseAlphabet})")
        
        # Stash the pulse alphabet in an instance data member.
        deviceType._pulseAlphabet = pulseAlphabet

        # All uniform-arity device types use a uniform signal character class.    
        deviceType._charClass = UniformCharacterClass(nPorts, pulseAlphabet)
            # Go ahead and set the character class to a UniformCharacterClass.
        
        # Delegate the rest of the constructor work to our parent class.
        super().__init__((pulseAlphabet,)*nPorts, stateSet)
            # Note above we replicate the same pulse alphabet on each port.

    # Displays a concise representation of uniform-arity device types:
    #   <alphabet>*<nPorts>(<stateSet>)
    def __str__(uadt):
        """String-conversion operator for uniform-arity device types."""
        return f"{str(uadt.pulseAlphabet)}*{uadt.nPorts}({str(uadt.stateSet)})"

    @property
    def pulseAlphabet(deviceType):
        """This property is the device type's (uniform) pulse alphabet."""
        return deviceType._pulseAlphabet

    # For uniform-arity device types, the applicable symmetry transforms include
    # all of the possible port-swap and (in the case of 3-port devices) port-
    # rotation transforms. (Other allowable port permutations can be obtained 
    # from these by composition.)

    def reportableTransforms(deviceType):
        dt = deviceType

        # Start with the generic list of transforms that are relevant even
        # for nonuniform-arity device types.
        rts = super().reportableTransforms()
        
        # Add to this our list of port-swap transforms (if there are any).
        psts = dt.portSwapTransforms()
        if psts is not None:
            rts += list(psts)
        
        # Add to this our list of port-rotation transforms (if there are any).
        prts = dt.portRotateTransforms()
        if prts is not None:
            rts += list(prts)
            
        return rts

    #|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #| The below methods generate symmetry transforms for this device type.

    # This method generates the port-swap transforms. Of course, 1-port devices
    # don't have any. Two-port devices have only a single port-swap transform.
    # For N-port devices (for N>2), we enumerate the port-swap transforms with
    # an appropriate nested FOR loop.

    def portSwapTransforms(deviceType):
        dt = deviceType
        nPorts = dt.nPorts
        if nPorts == 1:
            return
        elif nPorts == 2:
            yield PortExchangeTransform(dt, 0, 1)
        else:
            for firstPort in range(nPorts-1):
                if firstPort == nPorts-2:
                    yield PortExchangeTransform(dt, firstPort, firstPort+1)
                else:
                    for secondPort in range(firstPort + 1, nPorts):
                        yield PortExchangeTransform(dt, firstPort, secondPort)

    # This method generates the port-rotation transforms. This is only relevant
    # for devices with 3 or more ports. Rotation amounts may be either positive
    # or negative (we prefer small-magnitude negative numbers to large-magnitude
    # positive ones). Odd numbers of ports (such as 3) are handled slightly
    # differently from even numbers of ports (such as 4). (But the present 
    # version of the program doesn't study cases with more than 3 ports anyway.)

    def portRotateTransforms(deviceType):
        dt = deviceType
        nPorts = dt.nPorts

        # If there's only 1 or 2 ports, then there aren't any rotations.
        # (Port swap already handles the case of a port exchange.)
        if nPorts <= 2:
            return

        else:   # Case where we have 3 (or more) ports:

            # Note in the below code, we skip the case of rotation 
            # by 0, since it's just the identity transformation.

            if isOdd(nPorts):

                # Rotation amounts for odd numbers of ports go from
                # [-floor(N/2), floor(N/2)], so [-1,+1] for N=3.
                for rotAmt in range(-int(nPorts/2), int(nPorts/2)+1):
                    if rotAmt == 0:     # Rotate by 0 is just the identity.
                        continue        # Skip that one.
                    yield PortRotationTransform(dt, rotAmt)

            else:   # Even number of ports. (Only relevant for 4 or more ports.)

                # Rotation amounts for even numbers of ports go from
                # [-floor(N/2)+1, floor(N/2)-1], so (-2,1,+1) for N=4.
                for rotAmt in range(-int(nPorts/2)+1, int(nPorts/2)):
                    if rotAmt == 0:     # Rotate by 0 is just the identity.
                        continue        # Skip that one.
                    yield PortRotationTransform(dt, rotAmt)

# The following classes define uniform-arity device types
# using specific pulse alphabets that we care about.

class PositiveUnaryDeviceType(UniformArityDeviceType):
    isUnary = True
    defaultPulseAlphabet = thePositiveUnaryPulseAlphabet

class SymmetricBinaryDeviceType(UniformArityDeviceType):
    defaultPulseAlphabet = theSymmetricBinaryPulseAlphabet


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% BOTTOM OF FILE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%