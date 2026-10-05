class TextChunker:

    def __init__(
        self,
        chunk_size=100,
        overlap=20,
    ):
        if overlap >= chunk_size:
            raise ValueError(
                "overlap must be smaller than chunk_size"
            )

        self.chunk_size = chunk_size
        self.overlap = overlap

    def split(self, text):

        chunks = []

        start = 0

        while start < len(text):

            end = start + self.chunk_size

            chunk = text[start:end]

            chunks.append(chunk)

            start = end - self.overlap

        return chunks
