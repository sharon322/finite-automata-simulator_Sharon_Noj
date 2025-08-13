from flask import Flask, request, jsonify
from automaton import Automaton
from exception import AutomatonValidationError
import os

app = Flask(__name__)

OUTPUT_DIR = 'generated_diagrams'
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route('/process-automata', methods=['POST'])
def process_automata():
    try:
        data = request.get_json()
        if not isinstance(data, list):
            return jsonify({"error": "Invalid JSON format, expected a list of automata"}), 400

        results = []
        for automaton_def in data:
            automaton_id = automaton_def.get("id", "unknown")
            try:
                automaton = Automaton(**automaton_def)
                automaton.validate()
                diagram_path = automaton.generate_diagram(output_dir=OUTPUT_DIR)

                inputs_results = [
                    {"input": s, "result": automaton.process_string_recursive(s)}
                    for s in automaton_def.get("test_strings", [])
                ]

                results.append({
                    "id": automaton_id,
                    "success": True,
                    "diagram": diagram_path,
                    "inputs_validation": inputs_results,
                })

            except AutomatonValidationError as e:
                results.append({
                    "id": automaton_id,
                    "success": False,
                    "error_description": str(e)
                })

        return jsonify(results), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)