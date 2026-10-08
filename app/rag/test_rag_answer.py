from app.rag.rag_answer import RAGAnswerer


def main():
    question = "这个人做过哪些项目？只要说出项目名称"

    rag = RAGAnswerer()

    result = rag.answer(
        question=question,
        top_k=3,
        document_id=1002,
    )

    print()
    print("=" * 80)
    print("QUESTION")
    print(question)

    print()
    print("=" * 80)
    print("ANSWER")
    print(result["answer"])

    print()
    print("=" * 80)
    print("SOURCES")

    for source in result["sources"]:
        print(
            f"""
chunk_id: {source["id"]}
chunk_index: {source["chunk_index"]}
score: {source["score"]:.4f}
"""
        )


if __name__ == "__main__":
    main()
