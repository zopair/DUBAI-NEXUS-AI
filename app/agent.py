"""Small, inspectable agent core; model providers can be added behind this interface."""
from dataclasses import asdict, dataclass
from uuid import uuid4

from .policy import evaluate_action


@dataclass(frozen=True)
class PlanStep:
    id: str
    action: str
    title: str
    status: str
    requires_approval: bool
    rationale: str


@dataclass(frozen=True)
class AgentPlan:
    plan_id: str
    language: str
    intent: str
    summary: str
    steps: list[PlanStep]


INTENTS = {
    "report": ("report", "تقرير", "ملخص", "لخص", "summarize"),
    "analysis": ("analyze", "حلل", "تحليل", "راجع", "review"),
    "communication": ("email", "بريد", "رسالة", "أرسل", "ارسل", "send"),
    "workflow": ("task", "مهمة", "مهام", "متابعة", "workflow", "process"),
}


def detect_language(message: str) -> str:
    """Detect Arabic when at least one Arabic-script character is present."""
    return "ar" if any("\u0600" <= ch <= "\u06ff" for ch in message) else "en"


def resolve_intent(message: str) -> str:
    text = message.casefold()
    for intent, terms in INTENTS.items():
        if any(term.casefold() in text for term in terms):
            return intent
    return "general"


def build_plan(message: str) -> AgentPlan:
    if not isinstance(message, str) or not message.strip():
        raise ValueError("Message must not be empty.")
    language = detect_language(message)
    intent = resolve_intent(message)
    if intent == "communication":
        actions = [
            ("draft", "Prepare a communication draft", "Draft only; nothing is sent."),
            ("send", "Send after explicit approval", "External communication is sensitive."),
        ]
    elif intent == "report":
        actions = [
            ("analyze", "Inspect the supplied information", "Analysis is read-only."),
            ("draft", "Prepare a structured report", "A human reviews the result."),
        ]
    elif intent == "analysis":
        actions = [
            ("analyze", "Analyze the requested subject", "Analysis is read-only."),
            ("draft", "Prepare findings and recommendations", "Recommendations remain reviewable."),
        ]
    else:
        actions = [
            ("analyze", "Clarify and analyze the request", "No external side effect is permitted.")
        ]

    steps = []
    for action, title, rationale in actions:
        decision = evaluate_action(action)
        status = "awaiting_approval" if decision.requires_approval else "planned"
        steps.append(
            PlanStep(
                str(uuid4()), action, title, status, decision.requires_approval, rationale
            )
        )

    summary = (
        "تم تحويل طلبك إلى خطة قابلة للمراجعة."
        if language == "ar"
        else "Your request has been converted into a reviewable plan."
    )
    return AgentPlan(str(uuid4()), language, intent, summary, steps)


def plan_to_dict(plan: AgentPlan) -> dict:
    return asdict(plan)
