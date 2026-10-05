TOOLS = [
    {
        "type": "function",
        "name": "run_sql",
        "description": (
            "执行安全的 PostgreSQL SELECT 查询。"
            "当用户需要查询、统计、聚合数据库中的实际业务数据时使用。"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "sql": {
                    "type": "string",
                    "description": "需要执行的 PostgreSQL SELECT SQL",
                }
            },
            "required": ["sql"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_schema",
        "description": (
            "获取 ecommerce 数据库的表结构、字段和表关系。"
            "当用户询问数据库结构、表、字段，"
            "或者需要了解数据库中有哪些数据时使用。"
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
        "strict": True,
    },
        {
        "type": "function",
        "name": "create_line_chart",
        "description": (
            "根据 ResultStore 中已经存在的数据生成折线图。"
            "支持一个 X 轴字段和一个或多个 Y 轴字段。"
            "只能使用 result_id 对应 Result 中已经存在的字段。"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "result_id": {
                    "type": "string",
                    "description": "已有数据结果的 result_id",
                },
                "x_column": {
                    "type": "string",
                    "description": "X 轴字段名",
                },
                "y_columns": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "一个或多个 Y 轴字段名",
                },
                "title": {
                    "type": "string",
                    "description": "图表标题",
                },
                "x_label": {
                    "type": "string",
                    "description": "X 轴名称",
                },
                "y_label": {
                    "type": "string",
                    "description": "Y 轴名称",
                },
            },
            "required": [
                "result_id",
                "x_column",
                "y_columns",
                "title",
                "x_label",
                "y_label",
            ],
            "additionalProperties": False,
        },
        "strict": True,
    },
{
    "type": "function",
    "name": "profile_result",
    "description": (
        "分析已经通过 run_sql 获得的查询结果。"
        "必须使用 run_sql 返回的 result_id。"
        "用于检查结果行数、列数、NULL 数量以及基本数据特征。"
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "result_id": {
                "type": "string",
                "description": "run_sql 返回的查询结果 ID",
            }
        },
        "required": [
            "result_id"
        ],
        "additionalProperties": False,
    },
    "strict": True,
},
{
    "type": "function",
    "name": "detect_anomaly",
    "description": (
        "分析已经通过 run_sql 获得的查询结果，"
        "检测第二列数值数据中的统计异常。"
        "必须使用 run_sql 返回的 result_id。"
        "适用于销售额、订单数量等连续数值数据。"
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "result_id": {
                "type": "string",
                "description": "run_sql 返回的查询结果 ID",
            },
            "threshold": {
                "type": "number",
                "description": (
                    "Z-score 异常阈值，默认使用 2.0"
                ),
            },
        },
        "required": [
            "result_id",
            "threshold",
        ],
        "additionalProperties": False,
    },
    "strict": True,
},
]
