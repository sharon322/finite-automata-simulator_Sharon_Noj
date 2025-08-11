test_automaton
import unittest
from automaton import Automaton
from exception import ValidationError

class TestAutomaton(unittest.TestCase):
    def setUp(self):
        self.valid_automaton_dict = {
            "id": "test_1",
            "name": "Test Automaton",
            "initial_state": "q0",
            "acceptance_states": ["q1"],
            "alphabet": ["a", "b"],
            "states": ["q0", "q1"],
            "transitions": [
                {"from_state": "q0", "symbol": "a", "to_state": "q1"},
                {"from_state": "q0", "symbol": "b", "to_state": "q0"},
                {"from_state": "q1", "symbol": "a", "to_state": "q1"},
                {"from_state": "q1", "symbol": "b", "to_state": "q0"}
            ],
            "test_strings": ["a", "b", "ab"]
        }

    def test_validation_success(self):
        automaton = Automaton(self.valid_automaton_dict)
        try:
            automaton.validate()
        except ValidationError:
            self.fail("validate() raised ValidationError unexpectedly!")

    def test_process_string_acceptance(self):
        automaton = Automaton(self.valid_automaton_dict)
        automaton.validate()
        self.assertTrue(automaton.process_string("a"))
        self.assertFalse(automaton.process_string("b"))

    def test_missing_state_in_transitions(self):
        invalid_dict = dict(self.valid_automaton_dict)
        invalid_dict["transitions"][0]["to_state"] = "q2" 
        automaton = Automaton(invalid_dict)
        with self.assertRaises(ValidationError):
            automaton.validate()

if __name__ == '__main__':
    unittest.main()
