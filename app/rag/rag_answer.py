from openai import OpenAI

from app.rag.vector_retriever import VectorRetriever
import os

from dotenv import load_dotenv

load_dotenv()


MODEL = "deepseek-flash"


class RAGAnswerer:

    def __init__(self):
        self.retriever = VectorRetriever()

        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com",
        )

    def answer(
        self,
        question,
        top_k=5,
        document_id=None,
    ):
        # 1. Retrieve
        results = self.retriever.search(
            query=question,
            top_k=top_k,
            document_id=document_id,
        )

        if not results:
            return {
                "answer": "没有检索到相关内容。",
                "sources": [],
            }

        # 2. Build context
        context_parts = []

        for i, result in enumerate(results, start=1):
            context_parts.append(
                f"""
[Source {i}]
Chunk ID: {result["id"]}
Score: {result["score"]:.4f}

{result["content"]}
"""
            )

        context = "\n".join(context_parts)

        # 3. Ask LLM
        prompt = f"""
你是一个 RAG 问答助手。

请严格根据下面提供的资料回答问题。

要求：
1. 只能使用资料中的信息。
2. 不要编造资料中没有的信息。
3. 如果资料不足以回答，请明确说“资料不足”。
4. 回答简洁、直接。
5. 可以引用相关 Source 编号。

问题：

{question}

资料：

{context}
"""

        response = self.client.responses.create(
            model=MODEL,
            input=prompt,
        )

        answer = response.output_text

        return {
            "answer": answer,
            "sources": results,
        }
