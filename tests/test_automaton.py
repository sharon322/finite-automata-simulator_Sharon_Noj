import unittest
from automaton import Automaton
from exception import ValidationError

class TestAutomaton(unittest.TestCase):
    def setUp(self):
        self.valid_automaton_data = {
            "id": "automata_1",
            "name": "Even number recognizer",
            "initial_state": "q0",
            "acceptance_states": ["q0"],
            "alphabet": ["0", "1"],
            "states": ["q0", "q1"],
            "transitions": [
                {"from_state": "q0", "symbol": "0", "to_state": "q0"},
                {"from_state": "q0", "symbol": "1", "to_state": "q1"},
                {"from_state": "q1", "symbol": "0", "to_state": "q0"},
                {"from_state": "q1", "symbol": "1", "to_state": "q1"}
            ],
            "test_strings": ["0", "10", "101", "1010", ""]
        }

    def test_validation_automaton(self):
        automaton = Automaton(self.valid_automaton_data)
        automaton.validate()
        self.assertTrue(True)

    def test_invalid_initial_state(self):
        data = self.valid_automaton_data.copy()
        data["initial_state"] = "q9"
        automaton = Automaton(data)
        with self.assertRaises(ValidationError):
            automaton.validate()
        

if __name__ == '__main__':
    unittest.main()