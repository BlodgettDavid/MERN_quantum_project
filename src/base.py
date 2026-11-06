from abc import ABC, abstractmethod

class BaseAlgorithm(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Specific program identifier/slug (e.g., 'grover', 'teleportation', 'qsvm', 'qaoa', 'bb84')."""
        pass

    @property
    @abstractmethod
    def category(self) -> str:
        """Domain category for UI grouping (e.g., 'Algorithms', 'QML', 'Optimization', 'Security')."""
        pass

    @abstractmethod
    def run(self, **kwargs) -> dict:
        """Executes the circuit and returns the standardized UI payload."""
        pass