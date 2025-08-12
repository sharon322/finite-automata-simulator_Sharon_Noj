from exception import ValidationError

class Automaton:
    def __init__(self, automaton_dict):
        self.id = automaton_dict.get("id")
        self.name = automaton_dict.get("name")
        self.initial_state = automaton_dict.get("initial_state")
        self.acceptance_states = automaton_dict.get("acceptance_states", [])
        self.alphabet = automaton_dict.get("alphabet", [])
        self.states = automaton_dict.get("states", [])
        self.transitions = automaton_dict.get("transitions", [])
        self.test_strings = automaton_dict.get("test_strings", [])

    def validate(self):
        if not self.id or not isinstance(self.id, str):
            raise ValidationError("Invalid or missing automaton id.")

        if not self.name or not isinstance(self.name, str):
            raise ValidationError("Invalid or missing automaton name.")

        if not self.states or not isinstance(self.states, list):
            raise ValidationError("States must be a non-empty list.")

        if self.initial_state not in self.states:
            raise ValidationError(f"Initial state '{self.initial_state}' is not in states.")

        if not self.acceptance_states:
            raise ValidationError("No acceptance states defined.")

        for state in self.acceptance_states:
            if state not in self.states:
                raise ValidationError(f"Acceptance state '{state}' is not in states.")

        if not self.alphabet or not isinstance(self.alphabet, list):
            raise ValidationError("Alphabet must be a non-empty list.")

        for t in self.transitions:
            if t.get("from_state") not in self.states:
                raise ValidationError(f"Transition from_state '{t.get('from_state')}' invalid.")
            if t.get("to_state") not in self.states:
                raise ValidationError(f"Transition to_state '{t.get('to_state')}' invalid.")
            if t.get("symbol") not in self.alphabet:
                raise ValidationError(f"Symbol '{t.get('symbol')}' not in alphabet.")

        for state in self.states:
            for symbol in self.alphabet:
                if not any(t for t in self.transitions if t["from_state"] == state and t["symbol"] == symbol):
                    raise ValidationError(f"Missing transition from state '{state}' with symbol '{symbol}'.")

    def process_string(self, input_str, current_state=None, position=0):
        if current_state is None:
            current_state = self.initial_state

        if position == len(input_str):
            return current_state in self.acceptance_states

        symbol = input_str[position]

        for t in self.transitions:
            if t["from_state"] == current_state and t["symbol"] == symbol:
                return self.process_string(input_str, t["to_state"], position + 1)

        return False