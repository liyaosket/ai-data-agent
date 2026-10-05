import time

from task_agent import call_llm, MODEL
from llm_cache import llm_cache

from response_serializer import (
    serialize_response,
    deserialize_response,
)


def cached_call_llm(input_items):

    start = time.perf_counter()


    cached = llm_cache.get(
        input_items,
        MODEL,
    )


    if cached is not None:

        duration = (
            time.perf_counter()
            - start
        )

        return (
            deserialize_response(cached),
            True,
            duration,
        )


    response = call_llm(
        input_items
    )


    serialized = serialize_response(
        response
    )


    llm_cache.set(
        input_items,
        MODEL,
        serialized,
    )


    duration = (
        time.perf_counter()
        - start
    )


    return (
        response,
        False,
        duration,
    )
