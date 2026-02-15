import re
from typing import Dict, Any, List
from .base import BaseDetector

class LeakageDetector(BaseDetector):
    def name(self) -> str:
        return "Data Leakage Detector"

    def scan(self, text: str) -> Dict[str, Any]:
        found_threats = []
        score = 0.0

        # Simple Regex patterns for PII
        patterns = {
            "Email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
            "Credit Card": r"\b(?:\d[ -]*?){13,16}\b",
            "SSN": r"\b\d{3}-\d{2}-\d{4}\b"
        }

        for label, pattern in patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                found_threats.append(f"Detected {label}: {len(matches)} occurrence(s)")
                score += 50.0

        score = min(score, 100.0)

        return {
            "score": score,
            "threats": found_threats,
            "metadata": {"leaked_types": found_threats}
        }
