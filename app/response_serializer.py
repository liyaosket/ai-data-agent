import json

class CachedObject:

    def __init__(self, data):
        for k, v in data.items():
            setattr(
                self,
                k,
                v,
            )


class CachedResponse:

    def __init__(self, data):

        self.output = [
            CachedObject(item)
            for item in data["output"]
        ]

        self.output_text = data.get(
            "output_text"
        )

        self.usage = data.get(
            "usage"
        )


def serialize_response(response):

    return {
        "output": [
            item.model_dump()
            if hasattr(item, "model_dump")
            else item
            for item in response.output
        ],
        "output_text": response.output_text,
        "usage": (
            response.usage.model_dump()
            if response.usage
            and hasattr(response.usage, "model_dump")
            else None
        ),
    }


def deserialize_response(data):

    return CachedResponse(data)
