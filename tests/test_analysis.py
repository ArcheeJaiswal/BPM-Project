"""
========================================================================================
Test Suite: Regression, Soundness & Compliance Verification Tests
Referenced in IEEE paper (Section VI.D, Table I).
Run via: python -m unittest discover -s tests -v
========================================================================================
"""

import unittest
from analysis_engine import analyze_model


class TestBPMNComplianceAnalysis(unittest.TestCase):
    """17 Unit and Regression Tests covering all 6 models, bypasses, and soundness criteria."""

    # 1-6: Soundness of all 6 catalog models
    def test_level1_compliant_soundness(self):
        res = analyze_model("level1", "compliant")
        self.assertTrue(res["workflow_net_sound"])
        self.assertTrue(res["is_compliant"])

    def test_level1_violating_soundness(self):
        res = analyze_model("level1", "violating")
        self.assertTrue(res["workflow_net_sound"])

    def test_level2_compliant_soundness(self):
        res = analyze_model("level2", "compliant")
        self.assertTrue(res["workflow_net_sound"])
        self.assertTrue(res["is_compliant"])

    def test_level2_violating_soundness(self):
        res = analyze_model("level2", "violating")
        self.assertTrue(res["workflow_net_sound"])

    def test_level3_compliant_soundness(self):
        res = analyze_model("level3", "compliant")
        self.assertTrue(res["workflow_net_sound"])
        self.assertTrue(res["is_compliant"])

    def test_level3_violating_soundness(self):
        res = analyze_model("level3", "violating")
        self.assertTrue(res["workflow_net_sound"])

    # 7-9: Planted bypass detection
    def test_level1_credit_bypass_detected(self):
        res = analyze_model("level1", "violating")
        self.assertFalse(res["is_compliant"])
        self.assertGreater(res["violating_traces"], 0)

    def test_level2_premature_approval_detected(self):
        res = analyze_model("level2", "violating")
        self.assertFalse(res["is_compliant"])
        self.assertGreater(res["violating_traces"], 0)

    def test_level3_committee_bypass_detected(self):
        res = analyze_model("level3", "violating")
        self.assertFalse(res["is_compliant"])
        self.assertGreater(res["violating_traces"], 0)

    # 10-12: Trace counts and reachability properties
    def test_level1_trace_exploration(self):
        res = analyze_model("level1", "compliant")
        self.assertEqual(res["total_traces_explored"], 2)

    def test_level2_concurrent_traces(self):
        res = analyze_model("level2", "compliant")
        self.assertEqual(res["total_traces_explored"], 4)

    def test_level3_advanced_concurrency_traces(self):
        res = analyze_model("level3", "compliant")
        self.assertEqual(res["total_traces_explored"], 144)

    # 13-17: Counterexample and rule witness validation
    def test_level1_counterexample_witness(self):
        res = analyze_model("level1", "violating")
        ce = res["shortest_counterexample"]
        self.assertIsNotNone(ce)
        self.assertIn("t_bypass", ce["trace_ids"])

    def test_level2_counterexample_witness(self):
        res = analyze_model("level2", "violating")
        ce = res["shortest_counterexample"]
        self.assertIsNotNone(ce)
        self.assertIn("t_skip_cred", ce["trace_ids"])

    def test_level3_counterexample_witness(self):
        res = analyze_model("level3", "violating")
        ce = res["shortest_counterexample"]
        self.assertIsNotNone(ce)
        self.assertIn("t_comm_bypass", ce["trace_ids"])

    def test_level3_compliant_zero_violations(self):
        res = analyze_model("level3", "compliant")
        self.assertEqual(res["violating_traces"], 0)

    def test_level2_compliant_zero_violations(self):
        res = analyze_model("level2", "compliant")
        self.assertEqual(res["violating_traces"], 0)


if __name__ == "__main__":
    unittest.main()

