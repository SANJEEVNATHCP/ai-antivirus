from typing import List, Dict, Any
from ..detectors.base import BaseDetector
from ..detectors.injection import InjectionDetector
from ..detectors.jailbreak import JailbreakDetector
from ..detectors.leakage import LeakageDetector
from ..core.config import settings

class ScannerService:
    def __init__(self):
        self.detectors: List[BaseDetector] = [
            InjectionDetector(),
            JailbreakDetector(),
            LeakageDetector()
        ]

    def scan_text(self, text: str) -> Dict[str, Any]:
        all_threats = []
        max_score = 0.0
        detailed_results = {}

        for detector in self.detectors:
            result = detector.scan(text)
            detailed_results[detector.name()] = result
            all_threats.extend(result["threats"])
            max_score = max(max_score, result["score"])

        risk_level = self._get_risk_level(max_score)
        action = self._decide_action(max_score)

        return {
            "risk_score": max_score,
            "risk_level": risk_level,
            "threats": all_threats,
            "action": action,
            "details": detailed_results
        }

    def _get_risk_level(self, score: float) -> str:
        if score <= 20:
            return "LOW"
        elif score <= 50:
            return "MEDIUM"
        elif score <= 80:
            return "HIGH"
        else:
            return "CRITICAL"

    def _decide_action(self, score: float) -> str:
        if score >= 80:
            return "BLOCK"  # CRITICAL
        elif score >= settings.RISK_THRESHOLD:
            return "BLOCK"  # HIGH or above threshold
        elif score > 20:
            return "ALLOW" # MEDIUM (Log only)
        else:
            return "ALLOW" # LOW

scanner_service = ScannerService()
