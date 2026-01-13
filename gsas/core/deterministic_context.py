"""
Deterministic execution context for GSAS.
"""

from typing import Dict, Any, Iterator, Tuple
import copy


class DeterministicContext:
    """Immutable, deterministic evaluation context."""
    
    def __init__(self, data: Dict[str, Any], logical_time: int) -> None:
        self._data = self._freeze_dict(data)
        self._time = logical_time
    
    @staticmethod
    def _freeze_dict(d: Dict[str, Any]) -> Dict[str, Any]:
        """Create a deep frozen copy of dictionary."""
        if isinstance(d, dict):
            return {k: DeterministicContext._freeze_dict(v) for k, v in d.items()}
        elif isinstance(d, list):
            return [DeterministicContext._freeze_dict(item) for item in d]
        else:
            return d
    
    def __getitem__(self, key: str) -> Any:
        """Get value from context."""
        return self._data[key]  # Changed from .get() to raise KeyError if missing
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get value with default."""
        return self._data.get(key, default)
    
    def items(self) -> Iterator[Tuple[str, Any]]:  # Fixed return type
        """Iterate over items."""
        return iter(self._data.items())
    
    def keys(self) -> Iterator[str]:  # Added return type
        """Get all keys."""
        return iter(self._data.keys())
    
    def values(self) -> Iterator[Any]:  # Added return type
        """Get all values."""
        return iter(self._data.values())
    
    @property
    def time(self) -> int:
        """Get logical time."""
        return self._time
    
    def __setitem__(self, key: str, value: Any) -> None:
        """Prevent modification."""
        raise TypeError("Context is immutable")
    
    def __delitem__(self, key: str) -> None:
        """Prevent modification."""
        raise TypeError("Context is immutable")
    
    def __contains__(self, key: str) -> bool:
        """Check if key exists."""
        return key in self._data
    
    def copy(self) -> 'DeterministicContext':
        """Create a copy of the context."""
        return DeterministicContext(
            copy.deepcopy(self._data),
            self._time
        )
    
    def __repr__(self) -> str:
        return f"DeterministicContext(time={self._time}, data={self._data})"