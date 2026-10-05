from result_store import result_store


def profile_result(result_id: str) -> dict:
    result = result_store.get(result_id)

    columns = result["columns"]
    rows = result["rows"]

    profile = {
        "result_id": result_id,
        "row_count": len(rows),
        "column_count": len(columns),
        "columns": [],
    }

    for index, column in enumerate(columns):
        values = [row[index] for row in rows]

        null_count = sum(
            1 for value in values
            if value is None
        )

        non_null_values = [
            value for value in values
            if value is not None
        ]

        column_info = {
            "name": column,
            "null_count": null_count,
            "non_null_count": len(non_null_values),
        }

        if non_null_values:
            column_info["sample_values"] = [
                str(value)
                for value in non_null_values[:5]
            ]

        profile["columns"].append(column_info)

    return {
        "success": True,
        "profile": profile,
    }
