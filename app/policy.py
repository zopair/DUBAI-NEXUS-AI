"""Deterministic safety policy for agent actions."""
from dataclasses import dataclass

READ_ONLY = {"summarize", "analyze", "draft", "list"}
SENSITIVE = {"send", "delete", "approve", "pay", "publish", "modify"}


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    requires_approval: bool
    reason: str


def evaluate_action(action: str) -> PolicyDecision:
    normalized = action.strip().lower()
    if normalized in READ_ONLY:
        return PolicyDecision(True, False, "Read-only action permitted.")
    if normalized in SENSITIVE:
        return PolicyDecision(False, True, "Human approval required before execution.")
    return PolicyDecision(False, False, "Unknown action denied by default.")
