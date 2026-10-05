from response_serializer import serialize_response


class FakeItem:

    def model_dump(self):
        return {
            "type": "message",
            "role": "assistant",
        }


class FakeUsage:

    def model_dump(self):
        return {
            "input_tokens": 100,
            "output_tokens": 50,
            "total_tokens": 150,
        }


class FakeResponse:

    output = [FakeItem()]
    output_text = "hello"

    usage = FakeUsage()


response = FakeResponse()

result = serialize_response(response)

print(result)
