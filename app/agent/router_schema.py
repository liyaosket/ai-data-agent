ROUTER_TOOLS = [
    "rag_search",
    "run_sql",
    "kafka_status",
    "flink_status",
    "iceberg_metadata",
]


ROUTER_SCHEMA = {
    "type": "object",
    "properties": {
        "route": {
            "type": "string",
            "enum": [
                "knowledge",
                "data_query",
                "analysis",
                "system",
            ],
        },
        "intent": {
            "type": "string",
        },
        "tools": {
            "type": "array",
            "items": {
                "type": "string",
                "enum": ROUTER_TOOLS,
            },
        },
        "reason": {
            "type": "string",
        },
    },
    "required": [
        "route",
        "intent",
        "tools",
        "reason",
    ],
    "additionalProperties": False,
}
