from abc import ABC, abstractmethod


class BaseModelService(ABC):
    @abstractmethod
    async def generate(
        self,
        prompt: str,
        language: str = "auto",
    ) -> dict:
        """Generate a model output for the given prompt."""
        raise NotImplementedError


