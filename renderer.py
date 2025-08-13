from graphviz import Digraph
import os
import time

def generate_diagram(automaton, output_path="generated_diagrams"):
    os.makedirs(output_path, exist_ok=True)

    dot = Digraph(name=automaton.name, format='png')
    dot.attr(rankdir='LR')
    
    dot.node("", shape="none")
    dot.edge("", automaton.initial_state)

    for state in automaton.states:
        shape = "doublecircle" if state in automaton.acceptance_states else "circle"
        dot.node(state, shape=shape)

    for t in automaton.transitions:
        dot.edge(t['from_state'], t['to_state'], label=t['symbol'])

    filename = f"automata_{automaton.id}_{int(time.time())}"
    filepath = os.path.join(output_path, filename)
    dot.render(filepath, cleanup=True)
    return f"{filepath}.png"