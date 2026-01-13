"""
Unit tests for formal semantics.
"""

import unittest
from gsas.core.formal_semantics import (
    DeterministicContextSpec,
    GovernanceSignalSpec,
    CompositeGovernanceDecisionSpec
)

class TestFormalSemantics(unittest.TestCase):
    
    def test_deterministic_context(self) -> None:
        """Test deterministic context specification."""
        ctx = DeterministicContextSpec(time=123, data={"key": "value"})
        
        self.assertEqual(ctx.time, 123)
        self.assertEqual(ctx.get("key"), "value")
        self.assertEqual(ctx["key"], "value")
        
    def test_governance_signal(self) -> None:
        """Test governance signal specification."""
        signal = GovernanceSignalSpec(
            name="test_primitive",
            is_valid=True,
            metadata={"reason": "test"}
        )
        
        self.assertEqual(signal.name, "test_primitive")
        self.assertTrue(signal.is_valid)
        self.assertEqual(signal.metadata["reason"], "test")
    
    def test_composite_governance_decision(self) -> None:
        """Test composite governance decision specification."""
        signal = GovernanceSignalSpec(
            name="test_primitive",
            is_valid=True,
            metadata={}
        )
        
        decision = CompositeGovernanceDecisionSpec(
            is_permitted=True,
            signals=[signal],
            failure_reasons=[],
            proof={}
        )
        
        self.assertTrue(decision.is_permitted)
        self.assertEqual(len(decision.signals), 1)
        self.assertEqual(len(decision.failure_reasons), 0)

if __name__ == '__main__':
    unittest.main()