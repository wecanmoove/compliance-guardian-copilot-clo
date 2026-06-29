"""Copilot service — powers the chat assistant with Anthropic's Claude.

The assistant is grounded in the tenant's own compliance data: it receives a
summary of uploaded contracts and their risk findings as context, so answers
are about the user's actual documents rather than generic advice.
"""
from typing import List, Dict

from sqlalchemy.orm import Session

from ..config import settings
from ..models.contracts import ContractEntity
from ..models.findings import RiskFindingEntity

MODEL = "claude-haiku-4-5-20251001"
MAX_TOKENS = 1024

SYSTEM_PROMPT = """You are Compliance Guardian Copilot, an expert assistant for \
governance, risk management, and compliance (GRC). You help legal, procurement, \
and security teams understand contractual risk, policy gaps, and remediation steps.

Be concise, practical, and specific. When the user's documents are provided as \
context, ground your answers in them and reference documents by name. If asked \
about something outside the provided data, say so and give general best-practice \
guidance. Never invent clauses or findings that are not in the context."""


def _is_configured() -> bool:
    """True only when a plausibly-real API key is present (not a placeholder)."""
    key = settings.anthropic_api_key or ""
    return key.startswith("sk-ant-") and len(key) > 40


def _build_context(db: Session) -> str:
    """Summarize the tenant's contracts and findings for the system prompt."""
    contracts = (
        db.query(ContractEntity)
        .order_by(ContractEntity.created_at.desc())
        .limit(20)
        .all()
    )
    if not contracts:
        return "No documents have been uploaded yet."

    lines: List[str] = [f"The user has {len(contracts)} document(s) on file:"]
    for c in contracts:
        findings = (
            db.query(RiskFindingEntity)
            .filter(RiskFindingEntity.contract_id == c.contract_id)
            .all()
        )
        lines.append(
            f"\n- {c.file_name} (owner: {c.business_owner}, dept: {c.department}, "
            f"overall risk: {c.highest_risk_level or 'low'})"
        )
        if c.summary:
            lines.append(f"  Summary: {c.summary}")
        for f in findings[:8]:
            lines.append(
                f"  • [{(f.level or 'low').upper()}] {f.clause_reference}: "
                f"{f.description} → {f.recommendation}"
            )
    return "\n".join(lines)


def generate_reply(db: Session, history: List[Dict[str, str]], user_message: str) -> str:
    """Return the assistant's reply for the given message and prior history.

    `history` is a list of {"role": "user"|"assistant", "content": str} dicts in
    chronological order, excluding the new user_message.
    """
    if not _is_configured():
        return (
            "⚠️ Claude is not connected yet. Add a valid ANTHROPIC_API_KEY to the "
            ".env file (get one at console.anthropic.com), then restart the server. "
            "Once connected, I can answer questions about your uploaded contracts, "
            "risks, and compliance gaps."
        )

    # Imported lazily so the app still boots if the SDK isn't installed.
    import anthropic

    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    context = _build_context(db)

    messages = [{"role": m["role"], "content": m["content"]} for m in history]
    messages.append({"role": "user", "content": user_message})

    try:
        resp = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=f"{SYSTEM_PROMPT}\n\n## User's compliance data\n{context}",
            messages=messages,
        )
        return "".join(block.text for block in resp.content if block.type == "text")
    except anthropic.AuthenticationError:
        return "⚠️ The ANTHROPIC_API_KEY was rejected. Check that the key is valid."
    except Exception as e:  # pragma: no cover - surface any API/network error
        return f"⚠️ Copilot error: {type(e).__name__}: {e}"
