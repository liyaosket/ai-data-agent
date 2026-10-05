class ContextCompressor:


    def compress(
        self,
        query,
        documents,
        max_length=300
    ):

        keywords = query.lower().split()


        results = []


        for doc in documents:

            content = doc["content"]


            sentences = content.split("。")


            selected = []


            for sentence in sentences:

                sentence = sentence.strip()


                if not sentence:
                    continue


                score = 0


                for keyword in keywords:

                    if keyword in sentence:
                        score += 1


                if score > 0:

                    selected.append(
                        sentence
                    )


            compressed = "。".join(
                selected
            )


            if compressed:

                new_doc = doc.copy()

                new_doc["content"] = compressed

                results.append(
                    new_doc
                )


        return results
