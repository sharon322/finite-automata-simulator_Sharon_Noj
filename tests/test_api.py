import json
import unittest
from app import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_process_automata_ok_and_error(self):
        payload = [
            {
                "id": "ok",
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
                "test_strings": ["", "1"]
            },
            {
                "id": "bad_initial",
                "name": "Invalid",
                "initial_state": "q9",
                "acceptance_states": ["q0"],
                "alphabet": ["0", "1"],
                "states": ["q0", "q1"],
                "transitions": [
                    {"from_state": "q0", "symbol": "0", "to_state": "q0"},
                    {"from_state": "q0", "symbol": "1", "to_state": "q1"},
                    {"from_state": "q1", "symbol": "0", "to_state": "q1"},
                    {"from_state": "q1", "symbol": "1", "to_state": "q0"}
                ],
                "test_strings": ["0"]
            }
        ]
        res = self.client.post("/process-automata", data=json.dumps(payload), content_type="application/json")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(len(data), 2)
        ok = next(x for x in data if x["id"] == "ok")
        self.assertTrue(ok["success"])
        bad = next(x for x in data if x["id"] == "bad_initial")
        self.assertFalse(bad["success"])
        self.assertIn("error_description", bad)

    def test_invalid_payload(self):
        res = self.client.post("/process-automata", json={"not": "a list"})
        self.assertEqual(res.status_code, 400)

if __name__ == "__main__":
    unittest.main()
