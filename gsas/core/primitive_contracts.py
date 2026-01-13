"""
Type-safe contracts for GSAS governance primitives.
"""

from typing import Protocol, Dict, Any, List, runtime_checkable


# Use regular dict instead of TypedDict to support .get() properly
class EvaluationResult(Dict[str, Any]):
    """
    Result returned by governance primitive evaluation.
    
    Expected keys:
    - valid: bool - whether the primitive permits execution
    - metadata: Dict[str, Any] - structured diagnostic information  
    - evidence: List[Any] - optional list of audit artifacts
    """
    pass


@runtime_checkable
class GovernancePrimitive(Protocol):
    """
    Structural contract for all governance primitives.
    """

    def version(self) -> str:
        """Return a stable version identifier for this primitive."""
        ...

    def evaluate(self, context: Any) -> Dict[str, Any]:
        """
        Evaluate the primitive against a deterministic context.

        Args:
            context: DeterministicContext or compatible object

        Returns:
            Dict containing at minimum:
            - 'valid': bool
            - 'metadata': Dict[str, Any]
            - 'evidence': List[Any] (optional)
        """
        ...