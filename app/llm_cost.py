MODEL_PRICING = {
    "deepseek-flash": {
        "input_per_1m": 1.00,
        "output_per_1m": 5.00,
    }
}


def calculate_cost(
    model: str,
    input_tokens: int,
    output_tokens: int,
) -> float:
    pricing = MODEL_PRICING.get(model)

    if pricing is None:
        raise ValueError(f"未配置模型价格: {model}")

    input_cost = (
        input_tokens / 1_000_000
    ) * pricing["input_per_1m"]

    output_cost = (
        output_tokens / 1_000_000
    ) * pricing["output_per_1m"]

    return input_cost + output_cost
