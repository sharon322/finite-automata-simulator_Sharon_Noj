from graphviz import Digraph
import time
import os

def generate_diagram(automaton):
    dot = Digraph(name=automaton.name)
    dot.attr(rankdir='LR') 

    for state in automaton.states:
        if state in automaton.acceptance_states:
            dot.node(state, shape='doublecircle')
        else:
            dot.node(state, shape='circle')

    dot.node('', shape='none')
    dot.edge('', automaton.initial_state)

    for t in automaton.transitions:
        dot.edge(t["from_state"], t["to_state"], label=t["symbol"])

    if not os.path.exists('generated_diagrams'):
        os.makedirs('generated_diagrams')

    timestamp = int(time.time())
    filename = f"generated_diagrams/automata_{automaton.id}_{timestamp}.png"
    dot.render(filename, format='png', cleanup=True)
    return filename
