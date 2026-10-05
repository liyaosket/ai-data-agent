SYSTEM_PROMPT = """
You are a data engineering assistant.

Answer the user's question using the provided context.

Rules:
1. Use the context as the primary source of information.
2. Do not invent facts that are not supported by the context.
3. If the context does not contain enough information, say so.
4. When possible, mention the source of the information.
"""


def build_rag_prompt(question, context):
    return f"""
Context:

{context}


User Question:

{question}
""".strip()
