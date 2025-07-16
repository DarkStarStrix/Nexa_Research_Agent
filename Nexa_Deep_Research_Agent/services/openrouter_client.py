import os
import httpx

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = os.getenv(
    "OPENROUTER_URL",
    "https://openrouter.ai/api/v1/chat/completions"
)

class OpenRouterClient:
    def __init__(self):
        self.client = httpx.AsyncClient()
        self.api_key = OPENROUTER_API_KEY
        self.url = OPENROUTER_URL

    async def chat(self, model: str, messages: list, temperature: float = 0.7, max_tokens: int = 1000) -> str:
        """
        Send a chat-style request (list of messages) to OpenRouter.
        """
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        resp = await self.client.post(self.url, json=payload, headers=headers)
        resp.raise_for_status()
        # Return the assistant’s reply text
        return resp.json()["choices"][0]["message"]["content"]

    async def complete(self, model: str, prompt: str, temperature=0.7, max_tokens=1000) -> str:
        """
        Convenience wrapper for single-prompt usage.
        """
        return await self.chat(
            model,
            [{"role": "user", "content": prompt}],
            temperature,
            max_tokens
        )

