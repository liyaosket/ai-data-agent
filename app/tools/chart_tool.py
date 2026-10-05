import os

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib import font_manager

FONT_PATH = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"

font_manager.fontManager.addfont(FONT_PATH)
plt.rcParams["font.family"] = "Noto Sans CJK SC"

from app.result_store import result_store


CHART_DIR = "data/charts"

from app.result_store import result_store

def create_line_chart(
    result_id: str,
    x_column: str,
    y_columns: list[str],
    title: str,
    x_label: str,
    y_label: str,
) -> dict:

    result = result_store.get(result_id)

    columns = result["columns"]
    rows = result["rows"]

    if x_column not in columns:
        raise ValueError(
            f"X 轴字段不存在: {x_column}"
        )

    if not y_columns:
        raise ValueError(
            "至少需要一个 Y 轴字段"
        )

    for column in y_columns:
        if column not in columns:
            raise ValueError(
                f"Y 轴字段不存在: {column}"
            )

    x_index = columns.index(x_column)

    y_indices = {
        column: columns.index(column)
        for column in y_columns
    }

    x_values = [
        str(row[x_index])
        for row in rows
    ]

    plt.figure(figsize=(12, 6))

    for column, index in y_indices.items():
        y_values = []

        for row in rows:
            value = row[index]

            if value is None:
                y_values.append(None)
            else:
                y_values.append(float(value))

        plt.plot(
            x_values,
            y_values,
            marker="o",
            label=column,
        )

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()

    os.makedirs(CHART_DIR, exist_ok=True)

    file_path = os.path.join(
        CHART_DIR,
        f"{result_id}.png",
    )

    plt.savefig(file_path)
    plt.close()

    return {
        "success": True,
        "file_path": file_path,
        "result_id": result_id,
        "x_column": x_column,
        "y_columns": y_columns,
    }
