from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseDetector(ABC):
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def scan(self, text: str) -> Dict[str, Any]:
        """
        Returns:
            {
                "score": float (0-100),
                "threats": List[str],
                "metadata": Dict[str, Any]
            }
        """
        pass
