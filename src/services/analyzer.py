"""Rule-based compliance risk analysis engine.

Detects risky clauses in contract/policy text.
Inspired by: https://github.com/wecanmoove/compliance-guardian-app
"""
from __future__ import annotations
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Tuple


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


_LEVEL_WEIGHT = {
    RiskLevel.LOW: 1,
    RiskLevel.MEDIUM: 3,
    RiskLevel.HIGH: 6,
    RiskLevel.CRITICAL: 10,
}

_LEVEL_ORDER = {
    RiskLevel.LOW: 0,
    RiskLevel.MEDIUM: 1,
    RiskLevel.HIGH: 2,
    RiskLevel.CRITICAL: 3,
}


@dataclass
class Finding:
    keyword: str
    category: str
    level: RiskLevel
    description: str
    recommendation: str
    snippet: str = ""


@dataclass
class AnalysisResult:
    findings: List[Finding] = field(default_factory=list)
    overall_level: RiskLevel = RiskLevel.LOW
    score: int = 0
    word_count: int = 0

    @property
    def counts(self) -> Dict[str, int]:
        out = {lvl.value: 0 for lvl in RiskLevel}
        for f in self.findings:
            out[f.level.value] += 1
        return out


_RISK_RULES: Dict[str, Tuple[RiskLevel, str, str, str]] = {
    "unlimited liability": (
        RiskLevel.CRITICAL, "Liability",
        "Uncapped financial exposure.",
        "Negotiate liability cap tied to contract value.",
    ),
    "uncapped liability": (
        RiskLevel.CRITICAL, "Liability",
        "No ceiling on damages.",
        "Insist on aggregate liability cap.",
    ),
    "indemnify and hold harmless": (
        RiskLevel.HIGH, "Indemnification",
        "Broad indemnification may expose organization.",
        "Make indemnity mutual and limit to direct losses.",
    ),
    "perpetual license": (
        RiskLevel.HIGH, "IP",
        "Perpetual rights without limits.",
        "Add term limits or revenue-share clause.",
    ),
    "automatic renewal": (
        RiskLevel.MEDIUM, "Contract Term",
        "Auto-renewal may be missed.",
        "Require written opt-in for renewals.",
    ),
    "data protection": (
        RiskLevel.HIGH, "Compliance",
        "Data handling commitments required.",
        "Ensure DPA/processor agreements.",
    ),
    "confidential": (
        RiskLevel.LOW, "Data Protection",
        "Confidentiality obligations apply.",
        "Ensure reasonable definitions.",
    ),
}


def analyze(text: str) -> AnalysisResult:
    """Analyze text for compliance risks."""
    text_lower = text.lower()
    word_count = len(text.split())
    findings = []
    weights_sum = 0

    for keyword, (level, category, description, recommendation) in _RISK_RULES.items():
        matches = list(re.finditer(re.escape(keyword), text_lower, re.IGNORECASE))

        for match in matches:
            start = max(0, match.start() - 50)
            end = min(len(text), match.end() + 50)
            snippet = text[start:end].strip()

            finding = Finding(
                keyword=keyword,
                category=category,
                level=level,
                description=description,
                recommendation=recommendation,
                snippet=snippet,
            )
            findings.append(finding)
            weights_sum += _LEVEL_WEIGHT[level]

    # Remove duplicates
    seen_keywords = set()
    unique_findings = []
    for f in findings:
        if f.keyword not in seen_keywords:
            unique_findings.append(f)
            seen_keywords.add(f.keyword)

    findings = unique_findings
    findings.sort(key=lambda f: _LEVEL_ORDER[f.level], reverse=True)

    if findings:
        overall_level = max(findings, key=lambda f: _LEVEL_ORDER[f.level]).level
    else:
        overall_level = RiskLevel.LOW

    score = min(100, 10 + (weights_sum * 5))

    return AnalysisResult(
        findings=findings,
        overall_level=overall_level,
        score=score,
        word_count=word_count,
    )
