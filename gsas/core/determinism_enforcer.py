"""
Determinism enforcement for GSAS primitives.
"""

import ast
import inspect
from typing import Set, Any


class NonDeterministicPrimitiveError(Exception):
    """Raised when a primitive is detected as non-deterministic."""
    pass


class DeterminismEnforcer:
    """Enforces determinism in governance primitives."""
    
    BANNED_IMPORTS: Set[str] = {
        'time', 'datetime', 'random', 'os', 'sys', 'socket',
        'urllib', 'requests', 'subprocess', 'threading'
    }
    
    BANNED_FUNCTIONS: Set[str] = {
        'time.time', 'time.sleep', 'datetime.datetime.now',
        'random.random', 'random.randint', 'os.getenv',
        'input', 'print', 'open', 'eval', 'exec'
    }
    
    @classmethod
    def validate_deterministic(cls, source_code: str) -> None:
        """
        Validate that source code is deterministic.
        
        Args:
            source_code: Source code to validate
            
        Raises:
            NonDeterministicPrimitiveError: If code is not deterministic
        """
        try:
            tree = ast.parse(source_code)
            cls._check_ast(tree)
        except NonDeterministicPrimitiveError:
            raise
        except Exception as e:
            raise NonDeterministicPrimitiveError(f"AST parsing failed: {str(e)}")
    
    @classmethod
    def _check_ast(cls, node: ast.AST) -> None:
        """Recursively check AST for non-deterministic patterns."""
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name in cls.BANNED_IMPORTS:
                    raise NonDeterministicPrimitiveError(
                        f"Banned import '{alias.name}' found"
                    )
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module in cls.BANNED_IMPORTS:
                raise NonDeterministicPrimitiveError(
                    f"Banned import from '{node.module}' found"
                )
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                func_name = node.func.id
                if func_name in cls.BANNED_FUNCTIONS:
                    raise NonDeterministicPrimitiveError(
                        f"Banned function '{func_name}' found"
                    )
                elif func_name == '__import__':
                    raise NonDeterministicPrimitiveError(
                        "Direct __import__ call detected - use import statements instead"
                    )
            elif isinstance(node.func, ast.Attribute):
                if isinstance(node.func.value, ast.Name):
                    full_func_name = f"{node.func.value.id}.{node.func.attr}"
                    if full_func_name in cls.BANNED_FUNCTIONS:
                        raise NonDeterministicPrimitiveError(
                            f"Banned function '{full_func_name}' found"
                        )
        
        for child_node in ast.iter_child_nodes(node):
            cls._check_ast(child_node)
    
    @classmethod
    def validate_primitive_source(cls, primitive_class: Any) -> None:
        """
        Validate that a primitive class source is deterministic.
        
        Args:
            primitive_class: Class to validate
            
        Raises:
            NonDeterministicPrimitiveError: If class source is not deterministic
        """
        try:
            source = inspect.getsource(primitive_class)
            cls.validate_deterministic(source)
        except NonDeterministicPrimitiveError:
            raise
        except Exception as e:
            raise NonDeterministicPrimitiveError(
                f"Could not get source for {primitive_class.__name__}: {str(e)}"
            )