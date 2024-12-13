from model.llm.LLModel import LLModel


class GeminiModel():
    def __init__(self, temperature: float = 0.7, max_tokens: int = 512):
        """
        Initialize the GeminiModel by inheriting from LLModel.

        Args:
            temperature (float): Sampling temperature.
            max_tokens (int): Maximum number of tokens in the output.
        """
        self.model_name = 'gemini-1.5-pro'
        self.temperature = temperature
        self.max_tokens = max_tokens

        super().__init__(
            model_name=self.model_name,
            temperature=temperature,
            max_tokens=max_tokens
        )
