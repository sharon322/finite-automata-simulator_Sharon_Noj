app
from flask import Flask, request, jsonify
from automaton import Automaton
from exception import ValidationError
from renderer import generate_diagram

app = Flask(__name__)

@app.route('/process-automata', methods=['POST'])
def process_automata():
    data = request.get_json()

    if not data or not isinstance(data, list):
        return jsonify({"error": "Invalid JSON format, expected a list of automata"}), 400

    results = []

    for automaton_dict in data:
        automaton_id = automaton_dict.get("id", "unknown")

        try:
            automaton = Automaton(automaton_dict)
            automaton.validate()
            diagram_path = generate_diagram(automaton)

            inputs_results = []
            for input_str in automaton.test_strings:
                res = automaton.process_string(input_str)
                inputs_results.append({"input": input_str, "result": res})

            results.append({
                "id": automaton_id,
                "success": True,
                "inputs_validation": inputs_results,
                "diagram": diagram_path
            })

        except ValidationError as ve:
            results.append({
                "id": automaton_id,
                "success": False,
                "error_description": str(ve)
            })
        except Exception as e:
            results.append({
                "id": automaton_id,
                "success": False,
                "error_description": f"Unexpected error: {str(e)}"
            })

    return jsonify(results), 200

if __name__ == '__main__':
    app.run(debug=True)
