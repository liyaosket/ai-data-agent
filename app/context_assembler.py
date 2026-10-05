class ContextAssembler:

    def __init__(self, max_chars=3000):
        self.max_chars = max_chars

    def assemble(self, results):
        contexts = []
        current_length = 0

        for index, result in enumerate(results, start=1):

            metadata = result.get("metadata", {})

            source = metadata.get(
                "source",
                "unknown",
            )

            context = (
                f"[Document {index}]\n"
                f"Source: {source}\n"
                f"Score: {result['score']:.4f}\n"
                f"Content:\n"
                f"{result['text']}"
            )

            if current_length + len(context) > self.max_chars:
                break

            contexts.append(context)
            current_length += len(context)

        return "\n\n".join(contexts)
