import unittest
from automaton import Automaton
from exception import ValidationError

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
                {"from_state": "q1", "symbol": "0", "to_state": "q1"},
                {"from_state": "q1", "symbol": "1", "to_state": "q0"}
            ],
            "test_strings": ["", "0", "1", "10", "101"]
        }

    def test_validate_success(self):
        a = Automaton(self.valid)
        a.validate()  # no debe lanzar

    def test_recursive_accept(self):
        a = Automaton(self.valid)
        a.validate()
        self.assertTrue(a.process_string(""))
        self.assertTrue(a.process_string("0"))
        self.assertFalse(a.process_string("1"))
        self.assertFalse(a.process_string("101"))

    def test_invalid_initial_state(self):
        bad = dict(self.valid)
        bad["initial_state"] = "q9"
        a = Automaton(bad)
        with self.assertRaises(ValidationError):
            a.validate()

    def test_symbol_not_in_alphabet(self):
        bad = dict(self.valid)
        bad["transitions"] = bad["transitions"] + [{"from_state": "q0", "symbol": "2", "to_state": "q0"}]
        a = Automaton(bad)
        with self.assertRaises(ValidationError):
            a.validate()

    def test_missing_transition(self):
        bad = dict(self.valid)
        # quita transición q1 con '0' para forzar "faltan transiciones completas"
        bad["transitions"] = [
            {"from_state": "q0", "symbol": "0", "to_state": "q0"},
            {"from_state": "q0", "symbol": "1", "to_state": "q1"},
            {"from_state": "q1", "symbol": "1", "to_state": "q0"}
        ]
        a = Automaton(bad)
        with self.assertRaises(ValidationError):
            a.validate()

if __name__ == "__main__":
    unittest.main()
