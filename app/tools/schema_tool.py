from app.schema import DATABASE_SCHEMA


def get_schema_tool() -> dict:
    return {
        "success": True,
        "schema": DATABASE_SCHEMA,
    }
