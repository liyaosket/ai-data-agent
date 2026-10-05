import os

from openai import OpenAI

from app.embedding_model import EmbeddingModel
from dotenv import load_dotenv

load_dotenv()

class QwenEmbeddingModel(EmbeddingModel):

    def __init__(
        self,
        api_key=None,
        base_url=None,
        model=None,
        dimensions=1024,
    ):
        self.api_key = (
            api_key
            or os.getenv("DASHSCOPE_API_KEY")
        )

        self.base_url = (
            base_url
            or os.getenv("DASHSCOPE_BASE_URL")
        )

        self.model = (
            model
            or os.getenv(
                "QWEN_EMBEDDING_MODEL",
                "qwen3.7-text-embedding",
            )
        )

        self.dimensions = int(
            os.getenv(
                "QWEN_EMBEDDING_DIMENSIONS",
                str(dimensions),
            )
        )

        if not self.api_key:
            raise ValueError(
                "DASHSCOPE_API_KEY is not configured"
            )

        if not self.base_url:
            raise ValueError(
                "DASHSCOPE_BASE_URL is not configured"
            )

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )

    def embed(self, text):
        response = self.client.embeddings.create(
            model=self.model,
            input=text,
            dimensions=self.dimensions,
        )

        return response.data[0].embedding

    def embed_batch(self, texts):
        response = self.client.embeddings.create(
            model=self.model,
            input=texts,
            dimensions=self.dimensions,
        )

        return [
            item.embedding
            for item in response.data
        ]
