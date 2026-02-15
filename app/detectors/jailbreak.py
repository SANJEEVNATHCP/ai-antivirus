import json
import os
from typing import Dict, Any, List
from .base import BaseDetector

class JailbreakDetector(BaseDetector):
    def __init__(self, signatures_path: str = "rules/signatures.json"):
        self.signatures = []
        if os.path.exists(signatures_path):
            with open(signatures_path, "r") as f:
                data = json.load(f)
                self.signatures = data.get("jailbreak", [])

    def name(self) -> str:
        return "Jailbreak Detector"

    def scan(self, text: str) -> Dict[str, Any]:
        found_threats = []
        score = 0.0

        for sig in self.signatures:
            if sig.lower() in text.lower():
                found_threats.append(f"Matched jailbreak signature: {sig}")
                score += 40.0  # Jailbreaks are high risk

        # Cap score at 100
        score = min(score, 100.0)

        return {
            "score": score,
            "threats": found_threats,
            "metadata": {"match_count": len(found_threats)}
        }
