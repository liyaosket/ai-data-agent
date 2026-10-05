from app.query import execute_query
from app.sql_validator import validate_sql

from result_store import result_store


def run_sql_tool(sql: str) -> dict:

    valid, message = validate_sql(sql)

    if not valid:
        return {
            "success": False,
            "error": message,
        }

    try:

        columns, rows = execute_query(sql)

        result_id = result_store.save(
            columns=columns,
            rows=rows,
        )

        return {
            "success": True,
            "result_id": result_id,
            "columns": columns,
            "row_count": len(rows),
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e),
        }
