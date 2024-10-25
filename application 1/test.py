import unittest
from flask import json
from rlg import app  # Assuming rlg.py contains your Flask app

class RuleEngineAPITestCase(unittest.TestCase):
    def setUp(self):
        # Set up the Flask application for testing
        self.app = app.test_client()
        self.app.testing = True

    def test_create_rule(self):
        # Test creating a rule
        response = self.app.post('/create_rule', json={'rule_string': 'Sample Rule'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('rule_id', response.get_json())

    def test_combine_rules(self):
        # Test combining rules
        response = self.app.post('/combine_rules', json={'rule_ids': [1, 2]})
        self.assertEqual(response.status_code, 200)
        self.assertIn('combined_rule_id', response.get_json())

    def test_evaluate_rule(self):
        # Test evaluating a rule
        rule_id = 1  # Make sure this rule ID exists in your test database
        data = {"key": "value"}  # Adjust as needed based on your rules
        response = self.app.post('/evaluate_rule', json={'rule_id': rule_id, 'data': data})
        self.assertEqual(response.status_code, 200)
        self.assertIn('evaluation_result', response.get_json())

    def test_modify_rule(self):
        # Test modifying a rule
        rule_id = 1  # Make sure this rule ID exists in your test database
        new_rule_string = 'Modified Rule'
        response = self.app.post('/modify_rule', json={'rule_id': rule_id, 'new_rule_string': new_rule_string})
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.get_json())

    def tearDown(self):
        # Clean up any necessary state (if needed)
        pass

if __name__ == '__main__':
    unittest.main()
