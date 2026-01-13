# Governance Substrate for Autonomous Systems (GSAS)

## One-sentence value proposition

GSAS provides a deterministic, composable governance substrate that enforces institutional constraints on autonomous systems without duplicating or overriding existing governance logic.

## Overview

The Governance Substrate for Autonomous Systems (GSAS) is an infrastructure layer that binds autonomous systems to institutional reality by enforcing governance invariants. It does not execute, interpret, or orchestrate — it composes and enforces existing governance primitives.

GSAS operates below applications and agents but above infrastructure, ensuring all execution adheres to institutional constraints without being intrusive.

## Architecture diagram

<pre>
┌─────────────────────────────────────┐
│        Autonomous System            │
└──────────┬──────────────────────────┘
           │
┌──────────▼──────────────────────────┐
│         GSAS Governance Substrate   │
│                                     │
│  ┌─────────────┐  ┌─────────────┐   │
│  │ Determinist │  │ Authority   │   │
│  │ Execution   │  │ Realization │   │
│  └─────────────┘  └─────────────┘   │
│                                     │
│  ┌─────────────┐  ┌─────────────┐   │
│  │ Jurisdiction│  │ Capital     │   │
│  │ Enforcement │  │ Accounting  │   │
│  └─────────────┘  └─────────────┘   │
│                                     │
│  ┌─────────────┐  ┌─────────────┐   │
│  │ Containment │  │ Evaluation  │   │
│  │ & Safety    │  │ Engine      │   │
│  └─────────────┘  └─────────────┘   │
└──────────┬──────────────────────────┘
           │
┌──────────▼──────────────────────────┐
│     Governance Primitives Layer     │
│                                     │
│  ┌─────────────┐  ┌─────────────┐   │
│  │ Execution   │  │ Authority   │   │
│  │ Engine      │  │ System      │   │
│  └─────────────┘  └─────────────┘   │
│                                     │
│  ┌─────────────┐  ┌─────────────┐   │
│  │ Jurisdiction│  │ Capital     │   │
│  │ System      │  │ Accounting  │   │
│  └─────────────┘  └─────────────┘   │
└─────────────────────────────────────┘
</pre>

## Core Components

1. **Governance Evaluation Engine**: Evaluates all governance primitives in sequence.
2. **Composite Proof Generator**: Produces structured proofs for auditability.
3. **Failure Handler**: Enforces fail-closed behavior and emits structured failures.
4. **Integration Layer**: Interfaces with governance primitives via stable contracts.
5. **Proof Theory Module**: Provides cryptographic verification of governance decisions.
6. **Deterministic Context**: Immutable, deterministic execution context.
7. **Primitive Contracts**: Type-safe interfaces for governance primitives.
8. **Composition Operators**: Tools to compose multiple primitives with explicit semantics.
9. **Compliance Checker**: Validates that primitives and deployments satisfy contracts.
10. **Determinism Enforcer**: Ensures primitives are deterministic.

## Usage

GSAS is integrated into autonomous systems as a mandatory pre-execution gate. Before any action, the system calls GSAS to evaluate all governance constraints. If all pass, execution proceeds; otherwise, it fails closed with a structured proof.

## Design Principles

- **Compositional**: Integrates existing primitives without weakening semantics.
- **Deterministic**: All evaluations are deterministic and explainable.
- **Fail-Closed**: No partial compliance; all governance signals must be satisfied.
- **Auditability**: Proofs are reconstructable without runtime access.
- **Non-Interference**: Does not mutate or assume ownership of underlying systems.
- **Type-Safe**: Strong typing ensures contract compliance.
- **Deterministic Enforcement**: Primitives must be deterministic to ensure reproducibility.

## Requirements

1. Must enforce all governance primitives in strict sequence.
2. Must fail closed on any missing or violated signal.
3. Must emit structured proofs for every evaluation.
4. Must not reinterpret or override primitive semantics.
5. Must provide deterministic, explainable evaluation.
6. Must support versioned contracts for long-term compatibility.
7. Must provide cryptographic verification of governance decisions.
8. Must ensure all contexts are immutable and deterministic.
9. Must validate primitive contracts at registration time.
10. Must support composition of primitives with explicit semantics.
11. Must enforce determinism in all primitives.

## Determinism Requirements

**REQUIREMENTS FOR DETERMINISM:**
- Must not read system time (time.time, datetime.now)
- Must not access filesystem or network
- Must not use random numbers without seeded PRNG
- Must not maintain mutable state across calls
- Must not import banned modules like time, os, sys, etc.
- Must not call banned functions like time.time(), print(), open(), etc.
- Must not use __import__ directly (use import statements instead)

## Formal Semantics

GSAS includes formal mathematical specifications of:
- DeterministicContext immutability and behavior
- GovernanceSignal structure and semantics  
- CompositeGovernanceDecision properties
- Composition operator invariants
- Security properties and integrity preservation
- SHA256 commitment cryptographic properties

These formal specifications provide the foundation for proving correctness and reasoning about system security.

## Testing

All code is tested with unit tests covering:
- Governance evaluation engine
- Proof theory and verification
- Deterministic context handling
- Composition operators
- Determinism enforcement
- Compliance checking
- Formal semantics

## Type Checking

Type checking is enforced via mypy. Run:
```bash
mypy gsas/ --strict
```

The repository includes:
- `.github/workflows/typecheck.yml` CI workflow
- `mypy.ini` configuration file
- Comprehensive type annotations throughout the codebase

## Roadmap

### Immediate Fixes
1. Proof Verification: Currently raises NotImplementedError as per requirements.
2. Static Typing: Enforced via mypy with strict settings and CI workflow.
3. Determinism Requirements: Clearly documented in code comments and enforced by static analysis.
4. Composition Proof Chains: Proper versioning for composed primitives.

### Medium-term (Research Quality)
1. Proof Model: Implementation of one of three options (store context, proof-carrying code, trusted replay).
2. Determinism Enforcement: Static checker and sandboxed execution environment.
3. Formal Semantics: Mathematical specification of governance invariants.

## Security Properties

GSAS guarantees:

- Non-Interference: GSAS does not modify or assume ownership of underlying systems
- Fail-Closed: Execution fails if any constraint is violated
- Auditability: All decisions are provable and reconstructible
- Determinism: All evaluations are deterministic and reproducible
- Integrity: Governance invariants are preserved across all operations

## Performance Considerations

For large contexts (e.g., 10MB model parameters), the current implementation uses recursive deep copy which can be expensive. Future improvements may include:
- Copy-on-write using persistent data structures (e.g., pyrsistent)
- Lazy evaluation patterns
- Memory-efficient context handling

## Limitations
1. Proof Verification: Full verification requires stored execution context and is not yet implemented.
2. Determinism Enforcement: Static analysis can be bypassed by sophisticated attackers; sandboxing required for production use.
3. Performance: Deep copying of large contexts may impact performance in high-throughput scenarios.

These limitations are documented and tracked for future improvements.