#|%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% TOP OF FILE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%|
#|                                                                             |
#|      FILE NAME:      deviceDimensions.py                 [Python 3 module]  |
#|                                                                             |
#|      PROGRAM NAME:   BARC Element Classifier (barc.py)                      |
#|      MODULE NAME:    deviceDimensions                                       |
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
#|          An instance of class DeviceDimensions characterizes the            |
#|          overall complexity parameters associated with a particular         |
#|          type of device. These include the number of ports, pulse-          |
#|          type arities (multiplicities) for the ports, and the               |
#|          device's number of internal states.                                |
#|                                                                             |
#|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv|
"""Defines a class for describing device dimensions (complexity parameters)."""

# Exports:
__all__ = ['DeviceDimensions']

# Classes:

class DeviceDimensions:   # Characterizes the overall complexity parameters of a device.

    """Description of the overall complexity parameters of a device type."""

    #|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv|
    #|                                                                         |
    #|  Instance public properties:             [class documentation section]  |
    #|  ---------------------------                                            |
    #|                                                                         |
    #|      .nPorts:int - An integer n>0 giving the number of distinct         |
    #|          I/O ports (terminals) incident on the device.  Note that       |
    #|          this does not in general imply that all of these terminals     |
    #|          are used in a nontrivial way, or that they interact.           |
    #|                                                                         |
    #|      .portArities:iterable - For each port index i>=0, this gives       |
    #|          the corresponding arity (multiplicity) m_i of that port        |
    #|          (that is, of the wires that may be attached to that port,      |
    #|          and of the signals that may pass along those wires).           |
    #|                                                                         |
    #|      .nStates:int - An integer k>0 giving the number of distinct        |
    #|          internal states of the device.  Note that this does not        |
    #|          in general imply that all of these states are used in a        |
    #|          nontrivial way.                                                |
    #|                                                                         |
    #|^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^|

    def __init__(deviceDimensions, nPorts, portArities, nStates):
        deviceDimensions._nPorts      = nPorts
        deviceDimensions._portArities = portArities
        deviceDimensions._nStates     = nStates

    @property
    def nPorts(deviceDimensions):
        return deviceDimensions._nPorts

    @property
    def portArities(deviceDimensions):
        return deviceDimensions._portArities

    @property
    def nStates(deviceDimensions):
        return deviceDimensions._nStates

    def __str__(deviceDimensions):
        string = "%d[" % deviceDimensions.nPorts
        for portIndex in range(deviceDimensions.nPorts):
            portArity = deviceDimensions.portArities[portIndex]
            string += "%d" % portArity
            if portIndex < deviceDimensions.nPorts - 1:
                string += ","
        string += "](%d)" % deviceDimensions.nStates
        return string


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% BOTTOM OF FILE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%