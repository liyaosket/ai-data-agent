from result_store import result_store


def detect_anomaly(
    result_id: str,
    threshold: float = 2.0,
) -> dict:
    result = result_store.get(result_id)

    columns = result["columns"]
    rows = result["rows"]

    if len(columns) != 2:
        raise ValueError(
            f"异常检测当前要求两列数据，实际得到: {columns}"
        )

    if len(rows) < 3:
        raise ValueError("数据量太少，无法进行异常检测")

    x_values = []
    y_values = []

    for row in rows:
        if row[1] is None:
            continue

        try:
            value = float(row[1])
        except (TypeError, ValueError):
            raise ValueError(
                f"第二列必须是数值类型，得到: {row[1]}"
            )

        x_values.append(str(row[0]))
        y_values.append(value)

    if len(y_values) < 3:
        raise ValueError("有效数值数据太少")

    mean = sum(y_values) / len(y_values)

    variance = sum(
        (value - mean) ** 2
        for value in y_values
    ) / len(y_values)

    std = variance ** 0.5

    if std == 0:
        return {
            "success": True,
            "result_id": result_id,
            "mean": mean,
            "std": 0,
            "anomalies": [],
            "message": "所有数据值相同，没有检测到异常",
        }

    anomalies = []

    for x, value in zip(x_values, y_values):
        z_score = (value - mean) / std

        if abs(z_score) > threshold:
            anomalies.append({
                "x": x,
                "value": value,
                "z_score": round(z_score, 3),
            })

    return {
        "success": True,
        "result_id": result_id,
        "mean": round(mean, 2),
        "std": round(std, 2),
        "threshold": threshold,
        "anomaly_count": len(anomalies),
        "anomalies": anomalies,
    }
