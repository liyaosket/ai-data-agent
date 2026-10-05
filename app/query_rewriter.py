class QueryRewriter:


    def rewrite(self, query):

        expansions = []


        q = query.lower()


        if "kafka" in q:

            expansions.extend(
                [
                    "Kafka consumer",
                    "Kafka offset commit",
                    "Consumer Group",
                    "duplicate consumption",
                    "exactly once"
                ]
            )


        if "flink" in q:

            expansions.extend(
                [
                    "Flink checkpoint",
                    "state backend",
                    "exactly once"
                ]
            )


        if len(expansions) == 0:

            expansions.append(query)


        return expansions
