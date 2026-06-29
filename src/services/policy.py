"""Policy comparison and gap detection."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Requirement:
    key: str
    title: str
    description: str
    severity_if_missing: Severity
    guidance: str
    keywords: list


@dataclass
class Gap:
    requirement: Requirement
    present: bool


DEFAULT_POLICY = [
    Requirement(
        key="access_control",
        title="Access Control",
        description="RBAC must be enforced.",
        severity_if_missing=Severity.CRITICAL,
        guidance="Implement RBAC with least-privilege.",
        keywords=["access control", "rbac", "least privilege"],
    ),
    Requirement(
        key="encryption",
        title="Encryption",
        description="Data in transit and at rest must be encrypted.",
        severity_if_missing=Severity.CRITICAL,
        guidance="Use AES-256 for rest, TLS 1.2+ for transit.",
        keywords=["encryption", "aes-256", "tls", "encrypted"],
    ),
    Requirement(
        key="audit_logging",
        title="Audit Logging",
        description="All access must be logged and monitored.",
        severity_if_missing=Severity.HIGH,
        guidance="Implement centralized audit logging.",
        keywords=["audit", "logging", "log", "siem"],
    ),
    Requirement(
        key="backup_recovery",
        title="Backup & Recovery",
        description="Regular backups must be tested.",
        severity_if_missing=Severity.HIGH,
        guidance="Backup daily. Test recovery monthly.",
        keywords=["backup", "recovery", "rto", "rpo"],
    ),
]


def compare_to_policy(text: str, policy: list = None) -> list:
    """Compare document against policy requirements."""
    if policy is None:
        policy = DEFAULT_POLICY

    text_lower = text.lower()
    gaps = []

    for req in policy:
        present = any(keyword.lower() in text_lower for keyword in req.keywords)
        gaps.append(Gap(requirement=req, present=present))

    return gaps


def gap_summary(gaps: list) -> dict:
    """Summarize gap analysis."""
    total = len(gaps)
    met = sum(1 for g in gaps if g.present)
    missing = total - met
    compliance_pct = int((met / total * 100) if total > 0 else 0)

    return {
        "met": met,
        "total": total,
        "missing": missing,
        "compliance_pct": compliance_pct,
    }
