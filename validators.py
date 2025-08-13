from exception import AutomatonValidationError

def validate_automaton(a):
    # ID y nombre
    if not isinstance(a.id, str) or not a.id.strip():
        raise AutomatonValidationError("The automaton 'id' is mandatory and must be a string")
    if not isinstance(a.name, str) or not a.name.strip():
        raise AutomatonValidationError("The 'name' of the automaton is mandatory and must be a string")

    # Estados y alfabeto
    if not isinstance(a.states, list) or not a.states:
        raise AutomatonValidationError("The automaton states are not defined (empty or null list)")
    if not isinstance(a.alphabet, list) or not a.alphabet:
        raise AutomatonValidationError("The automaton alphabet is not defined (empty or null list)")

    # Estado inicial
    if a.initial_state is None or not isinstance(a.initial_state, str):
        raise AutomatonValidationError("There is no initial state defined for the automaton")
    if a.initial_state not in a.states:
        raise AutomatonValidationError("The initial state does not exist in the state list")

    # Estados de aceptación
    if not isinstance(a.acceptance_states, list):
        raise AutomatonValidationError("The acceptance states must be a list")
    if not a.acceptance_states:
        raise AutomatonValidationError("There are no acceptance states in the automaton")
    for s in a.acceptance_states:
        if s not in a.states:
            raise AutomatonValidationError(f"The acceptance state '{s}' does not exist in the state list")

    # Transiciones
    if not isinstance(a.transitions, list) or not a.transitions:
        raise AutomatonValidationError("Transitions are not defined (empty or null list)")

    for t in a.transitions:
        if not isinstance(t, dict):
            raise AutomatonValidationError("Each transition must be an object with from_state, symbol, to_state")
        fs = t.get("from_state")
        sym = t.get("symbol")
        ts = t.get("to_state")
        if fs is None or sym is None or ts is None:
            raise AutomatonValidationError("Invalid transition: Required fields (from_state, symbol, to_state) are missing")
        if fs not in a.states:
            raise AutomatonValidationError(f"Invalid transition: source state '{fs}' does not exist")
        if ts not in a.states:
            raise AutomatonValidationError(f"Invalid transition: destination state '{ts}' does not exist")
        if sym not in a.alphabet:
            raise AutomatonValidationError(f"The character '{sym}' is not defined in the automaton alphabet")

    # Validar transiciones completas
    for state in a.states:
        for symbol in a.alphabet:
            if symbol not in a.transition_map.get(state, {}):
                raise AutomatonValidationError(f"Missing transition from '{state}' with symbol '{symbol}'.")
