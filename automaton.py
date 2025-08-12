from graphviz import Digraph
import time
from exceptions import AutomatonValidationError
from validators import validate_automaton

class Automaton:
    def __init__(self,id, name, initial_state, acceptance_states, alphabet, states, transitions, test_strings):
        self.id = id
        self.name = name
        self.initial_state = initial_state
        self.acceptance_states = acceptance_states
        self.alphabet = alphabet
        self.states = states
        self.transitions = transitions
        self.test_strings = test_strings
        self.transition_map = self._build_transition_map()

    def _build_transition_map(self):
        mapping = {}
        for t in self.transitions:
            mapping.setdefault(t["from_state"], {})[t["symbol"]] = t["to_state"]
        return mapping

    def validate(self):
        validate_automaton(self)

    def process_string_recursive(self, input_str, current_state=None):
        if current_state is None:
            current_state = self.initial_state
        if not input_str:
            return current_state in self.acceptance_states

        symbol = input_str[0]
        next_state = self.transition_map.get((current_state, symbol))
        if next_state is None:
            return False
        return self.process_string_recursive(input_str[1:], next_state)

    def generate_diagram(self, output_dir='generated_diagrams'):
        dot = Digraph(format='png')
        dot.attr(rankdir='LR')

        dot.node('', shape='none')
        dot.edge('', self.initial_state)

        for state in self.states:
            if state in self.acceptance_states:
                dot.node(state, shape='doublecircle')
            else:
                dot.node(state, shape='circle')

        for t in self.transitions:
            dot.edge(t["from_state"], t["to_state"], label=t["symbol"])

        filename = f"automata_{self.id}_{int(time.time())}"
        filepath = f"{output_dir}/{filename}"
        dot.render(filepath, cleanup=True)
        return f"{filepath}.png"