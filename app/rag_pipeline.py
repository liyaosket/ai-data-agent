from app.retriever import Retriever
from app.context_assembler import ContextAssembler
from app.rag_prompt import SYSTEM_PROMPT, build_rag_prompt


class RAGPipeline:

    def __init__(
        self,
        retriever,
        context_assembler,
        llm,
    ):
        self.retriever = retriever
        self.context_assembler = context_assembler
        self.llm = llm

    def run(
        self,
        question,
        query_vector,
        top_k=3,
        score_threshold=0.0,
    ):
        # 1. Retrieve
        results = self.retriever.retrieve(
            query_vector=query_vector,
            top_k=top_k,
            score_threshold=score_threshold,
        )

        # 2. Assemble context
        context = self.context_assembler.assemble(
            results
        )

        # 3. Build prompt
        user_prompt = build_rag_prompt(
            question=question,
            context=context,
        )

        # 4. Call LLM
        answer = self.llm.generate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )

        return {
            "question": question,
            "retrieved_documents": results,
            "context": context,
            "answer": answer,
        }
