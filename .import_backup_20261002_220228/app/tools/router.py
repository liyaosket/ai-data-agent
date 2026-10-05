from tools.sql_tool import run_sql_tool
from tools.schema_tool import get_schema_tool
from tools.chart_tool import create_line_chart
from tools.profile_tool import profile_result
from tools.anomaly_tool import detect_anomaly

def execute_tool(
    name: str,
    arguments: dict,
) -> dict:

    if name == "run_sql":

        return run_sql_tool(
            arguments["sql"]
        )

    if name == "get_schema":

        return get_schema_tool()

    if name == "create_line_chart":
        return create_line_chart(
            result_id=arguments["result_id"],
            x_column=arguments["x_column"],
            y_columns=arguments["y_columns"],
            title=arguments["title"],
            x_label=arguments["x_label"],
            y_label=arguments["y_label"],
        )

    if name == "profile_result":
        return profile_result(
            result_id=arguments["result_id"]
        )
    if name == "detect_anomaly":
        return detect_anomaly(
            result_id=arguments["result_id"],
            threshold=arguments["threshold"],
        )

    return {
        "success": False,
        "error": f"未知 Tool: {name}",
    }
