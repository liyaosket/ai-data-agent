class RetryPolicy:

    def __init__(
        self,
        max_retries: int = 2,
    ):
        self.max_retries = max_retries

    def should_retry(
        self,
        attempt: int,
        error: Exception,
    ) -> bool:

        return attempt <= self.max_retries
