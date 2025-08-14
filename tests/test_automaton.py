import unittest
from automaton import Automaton
from exception import AutomatonValidationError

class TestAutomaton(unittest.TestCase):

    def setUp(self):
        self.valid = {
            "id": "a1",
            "name": "Even ones",
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
            "test_strings": ["", "0", "1", "10", "101"]
        }

    def test_validate_success(self):
        a = Automaton(**self.valid)
        a.validate() 

    def test_recursive_accept(self):
        a = Automaton(**self.valid)
        a.validate()
        self.assertTrue(a.process_string_recursive(""))
        self.assertTrue(a.process_string_recursive("0"))
        self.assertFalse(a.process_string_recursive("1"))
        self.assertFalse(a.process_string_recursive("101"))

    def test_invalid_initial_state(self):
        bad = dict(self.valid)
        bad["initial_state"] = "q9"
        a = Automaton(**bad)
        with self.assertRaises(AutomatonValidationError):
            a.validate()

    def test_symbol_not_in_alphabet(self):
        bad = dict(self.valid)
        bad["transitions"] = bad["transitions"] + [{"from_state": "q0", "symbol": "2", "to_state": "q0"}]
        a = Automaton(**bad)
        with self.assertRaises(AutomatonValidationError):
            a.validate()

    def test_missing_transition(self):
        bad = dict(self.valid)
        bad["transitions"] = [
            {"from_state": "q0", "symbol": "0", "to_state": "q0"},
            {"from_state": "q0", "symbol": "1", "to_state": "q1"},
            {"from_state": "q1", "symbol": "1", "to_state": "q0"}
        ]
        a = Automaton(**bad)
        with self.assertRaises(AutomatonValidationError):
            a.validate()

if __name__ == "__main__":
    unittest.main()
