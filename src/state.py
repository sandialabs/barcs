#|%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% TOP OF FILE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%|
#|																			   |
#|      FILE NAME:      state.py                   			[Python 3 module]  |
#|																			   |
#|      PROGRAM NAME:   BARC Element Classifier (barc)						   |
#|      MODULE NAME:    state												   |
#|                                                                             |
#|      AUTHOR:         Michael P. Frank <mpfrank@sandia.gov>                  |
#|                                                                             |
#|      PROJECT:        LPS/ACS/ACI Project #41, Asynchronous Ballistic        |
#|                      Reversible Computing using Superconducting             |
#|                      Elements (ABRC/SE)                                     |
#|                                                                             |
#|      IMPORTED BY:    (2) stateSet.                                          |
#|      CODE LAYER:     Layer #1 (no imports from above layer #0).       	   |
#|      IMPORTS:        (0) utilities.                                         |
#|                                                                             |
#|-----------------------------------------------------------------------------+
#|																			   |
#|      DESCRIPTION:														   |
#|      ============														   |
#|																			   |
#|			This module defines the class State. An object that is an in-	   |
#|			stance of class State is used to identify a specific internal 	   |
#|			state of a device. A state object knows what state alphabet it	   |
#|			was drawn from, and may support basic operators such as state	   |
#|			negation/swapping (for two-state alphabets).					   |
#|																			   |
#|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv|

from utilities import flux

class State:

	"""Represents an internal device state, selected from a given state set."""
	
	def __init__(newState, stateSet, symbol):
		newState._stateSet = stateSet
		newState._symbol = symbol
	
	@property
	def flux(thisState):
		return flux(thisState.symbol)

	@property
	def stateSet(thisState):
		return thisState._stateSet
	
	@property
	def symbol(thisState):
		return thisState._symbol

	@property
	def negatable(thisState):
		return thisState.stateSet.negatable
	
	def negate(thisState):
	
		stateSet = thisState.stateSet
		symbol = thisState.symbol
	
		return State(stateSet, stateSet.negate(symbol))

	def __neg__(thisState):
		return thisState.negate()
		
	def swap(thisState):
		return -thisState

	def __str__(thisState):
		sym = thisState.symbol
		if isinstance(sym,str):
			return sym
		else:
			return str(sym)

	def __eq__(thisState, thatState):
		s1 = thisState
		s2 = thatState
		return s1.symbol == s2.symbol
	
	def __lt__(thisState, thatState):
		s1 = thisState
		s2 = thatState
		return s1.symbol < s2.symbol
	
	def __hash__(state):
		return hash(state.symbol)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% BOTTOM OF FILE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%