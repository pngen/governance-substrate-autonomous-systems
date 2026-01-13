"""
Unit tests for determinism enforcer.
"""

import unittest
from gsas.core.determinism_enforcer import DeterminismEnforcer, NonDeterministicPrimitiveError

class TestDeterminismEnforcer(unittest.TestCase):
    
    def test_valid_deterministic_code(self) -> None:
        """Test valid deterministic code."""
        valid_code = """
class ValidPrimitive:
    def evaluate(self, context):
        return {"valid": True, "metadata": {}}
"""
        DeterminismEnforcer.validate_deterministic(valid_code)
        
    def test_banned_import_time(self) -> None:
        """Test banned import time."""
        invalid_code = """
import time

class InvalidPrimitive:
    def evaluate(self, context):
        return {"valid": True, "metadata": {}}
"""
        with self.assertRaises(NonDeterministicPrimitiveError):
            DeterminismEnforcer.validate_deterministic(invalid_code)
    
    def test_banned_function_time(self) -> None:
        """Test banned function time.time()."""
        invalid_code = """
import time

class InvalidPrimitive:
    def evaluate(self, context):
        t = time.time()
        return {"valid": True, "metadata": {}}
"""
        with self.assertRaises(NonDeterministicPrimitiveError):
            DeterminismEnforcer.validate_deterministic(invalid_code)
    
    def test_banned_import_from_time(self) -> None:
        """Test banned import from time."""
        invalid_code = """
from time import time

class InvalidPrimitive:
    def evaluate(self, context):
        t = time()
        return {"valid": True, "metadata": {}}
"""
        with self.assertRaises(NonDeterministicPrimitiveError):
            DeterminismEnforcer.validate_deterministic(invalid_code)
    
    def test_direct_import_call(self) -> None:
        """Test direct __import__ call."""
        invalid_code = """
class InvalidPrimitive:
    def evaluate(self, context):
        t = __import__('time')
        return {"valid": True, "metadata": {}}
"""
        with self.assertRaises(NonDeterministicPrimitiveError):
            DeterminismEnforcer.validate_deterministic(invalid_code)

if __name__ == '__main__':
    unittest.main()