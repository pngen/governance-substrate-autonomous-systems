"""
Primitive composition operators for GSAS.
"""

from typing import List, Dict, Any
from gsas.core.primitive_contracts import GovernancePrimitive
from gsas.core.deterministic_context import DeterministicContext


class PrimitiveComposer:
    """Composes primitives with explicit semantics."""
    
    def sequential_and(self, primitives: List[GovernancePrimitive]) -> GovernancePrimitive:
        """
        All primitives must pass in order.
        """
        primitives_captured = primitives  # Capture for closure
        
        class SequentialAndPrimitive:
            def version(self) -> str:
                sub_versions = tuple(p.version() for p in primitives_captured)
                return f"sequential-and-{hash(sub_versions) % 1000000}"
                
            def evaluate(self, context: Any) -> Dict[str, Any]:
                for primitive in primitives_captured:
                    result = primitive.evaluate(context)
                    if not result.get("valid", False):
                        return {
                            "valid": False,
                            "metadata": {"reason": f"Primitive {primitive.__class__.__name__} failed"},
                            "evidence": []
                        }
                return {
                    "valid": True,
                    "metadata": {"message": "All primitives passed sequentially"},
                    "evidence": []
                }
                
        return SequentialAndPrimitive()
    
    def parallel_and(self, primitives: List[GovernancePrimitive]) -> GovernancePrimitive:
        """
        All primitives must pass, order independent.
        """
        primitives_captured = primitives
        
        class ParallelAndPrimitive:
            def version(self) -> str:
                sub_versions = tuple(p.version() for p in primitives_captured)
                return f"parallel-and-{hash(sub_versions) % 1000000}"
                
            def evaluate(self, context: Any) -> Dict[str, Any]:
                results = []
                for primitive in primitives_captured:
                    result = primitive.evaluate(context)
                    results.append(result.get("valid", False))
                    
                if all(results):
                    return {
                        "valid": True,
                        "metadata": {"message": "All primitives passed in parallel"},
                        "evidence": []
                    }
                else:
                    failed_primitives = [
                        p.__class__.__name__ for i, p in enumerate(primitives_captured) 
                        if not results[i]
                    ]
                    return {
                        "valid": False,
                        "metadata": {"reason": f"Failed primitives: {failed_primitives}"},
                        "evidence": []
                    }
                
        return ParallelAndPrimitive()
    
    def threshold(self, primitives: List[GovernancePrimitive], k: int) -> GovernancePrimitive:
        """
        At least k primitives must pass.
        """
        primitives_captured = primitives
        k_captured = k
        
        class ThresholdPrimitive:
            def version(self) -> str:
                sub_versions = tuple(p.version() for p in primitives_captured)
                return f"threshold-{k_captured}-{hash(sub_versions) % 1000000}"
                
            def evaluate(self, context: Any) -> Dict[str, Any]:
                results = []
                for primitive in primitives_captured:
                    result = primitive.evaluate(context)
                    results.append(result.get("valid", False))
                    
                passed_count = sum(results)
                if passed_count >= k_captured:
                    return {
                        "valid": True,
                        "metadata": {"message": f"{passed_count} of {len(primitives_captured)} primitives passed"},
                        "evidence": []
                    }
                else:
                    return {
                        "valid": False,
                        "metadata": {
                            "reason": f"Only {passed_count} of {len(primitives_captured)} primitives passed, need at least {k_captured}"
                        },
                        "evidence": []
                    }
                
        return ThresholdPrimitive()