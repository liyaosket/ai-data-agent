from app.multi_query_retriever import MultiQueryRetriever



def main():


    retriever = MultiQueryRetriever()


    query = "Kafka 为什么会重复消费？"


    results = retriever.search(
        query,
        top_k=10
    )


    print("=" * 70)

    print(
        "Query:",
        query
    )


    print("=" * 70)



    for rank, item in enumerate(
        results[:10],
        start=1
    ):

        print()

        print(
            "Rank:",
            rank
        )

        print(
            "Document:",
            item["document_id"]
        )

        print(
            "Content:"
        )

        print(
            item["content"]
        )


if __name__ == "__main__":
    main()
