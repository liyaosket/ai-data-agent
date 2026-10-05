from app.query_rewriter import QueryRewriter


def main():

    rewriter = QueryRewriter()


    query = "Kafka 为什么会重复消费？"


    queries = rewriter.rewrite(
        query
    )


    print(
        "Original:"
    )

    print(query)


    print()

    print(
        "Rewrite:"
    )

    for q in queries:
        print(
            "-",
            q
        )


if __name__ == "__main__":
    main()
