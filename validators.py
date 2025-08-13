from exceptions import AutomatonValidationError

def validate_automaton(automaton):
    if not automaton.initial_state:
        raise AutomatonValidationError("Initial state is not defined.") 

    if automaton.initial_state not in automaton.states:
        raise AutomatonValidationError("Initial state does not exist in the state list")

    if not automaton.acceptance_states:
        raise AutomatonValidationError("There are no acceptance states in the automaton")

    for state in automaton.acceptance_states:
        if state not in automaton.states
            raise AutomatonValidationError(f"Acceptance state '{state}' does not exist in the state list")
        
    for (from_state, symbol), to_state in automaton.transition_map.items():
        if from_state not in automaton.states or to_state not in automaton.states:
            raise AutomatonValidationError(f"Transition from non-existent state: {from_state} -> {to_state}")
        if symbol not in automaton.alphabet:
            raise AutomatonValidationError(f"Symbol '{symbol}' not in alphabet")

    for state in automaton.states:
        if not any(from_state == state for (from_state, _) in automaton.transition_map):
            raise AutomatonValidationError(f"State '{state}' has no outgoing transitions")