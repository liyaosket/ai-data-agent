import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from tools.definitions import TOOLS
from tools.router import execute_tool


load_dotenv()

client = OpenAI(
    #api_key=os.getenv('DEEPSEEK_API_KEY'),
    api_key="sk-13111e3767894ddea5c899adbc1be6f1",
    base_url="https://api.deepseek.com")

MODEL = "deepseek-flash"


SYSTEM_PROMPT = """
你是一个 AI 数据分析助手。

你可以使用以下工具：

1. run_sql
   用于查询和分析数据库中的实际业务数据。

2. get_schema
   用于查看数据库的表、字段和关系。

3. create_line_chart
   用于把已经查询得到的两列数据生成折线图。

工作规则：

1. 如果用户的问题需要实际业务数据，使用 run_sql。
2. 如果用户询问数据库结构、字段、表关系，使用 get_schema。
3. 不要假装执行过 Tool。
4. 只有 Tool 返回的数据才能作为数据库事实。
5. 根据 Tool 返回结果回答用户。
6. 使用中文。
7. 回答简洁、清晰。
8. create_line_chart 必须使用 run_sql 返回的 result_id。
9. 不要把查询结果中的大量原始数据复制到 Tool 参数中。
10. 如果用户要求分析查询结果的数据质量、数据规模、NULL 情况或基本数据特征，可以使用 profile_result。
11. profile_result 必须使用 run_sql 返回的 result_id。
12. 不要自己编造数据统计结果。
13. 如果用户要求寻找异常、异常日期、异常销售额或异常订单数量，可以使用 detect_anomaly。
14. detect_anomaly 必须使用 run_sql 返回的 result_id。
15. detect_anomaly 只适用于两列结果：
   第一列是维度，例如日期；
   第二列是数值。
16. 不要自行编造异常检测结果。
17. 异常检测结果是统计意义上的异常信号，不代表业务上一定存在错误。
18. 不要在缺少历史数据、业务目标或外部基准的情况下，
    将某个指标描述为“偏高”“偏低”“正常”。
19. 可以描述指标本身及其变化，
    但涉及业务评价时必须说明判断依据。

使用 create_line_chart 时：
1. 必须先调用 run_sql。
2. run_sql 的查询结果必须恰好包含两列。
3. 第一列作为 X 轴。
4. 第二列作为 Y 轴。
5. 如果查询结果超过两列，不要直接调用 create_line_chart。
6. 如果用户要求画趋势图，应生成适合绘图的两列 SQL 查询。
"""


def run_agent(question: str) -> str:

    input_items = [
        {
            "role": "user",
            "content": question,
        }
    ]

    while True:

        response = client.responses.create(
            model=MODEL,
            instructions=SYSTEM_PROMPT,
            tools=TOOLS,
            input=input_items,
        )

        tool_calls = [
            item
            for item in response.output
            if item.type == "function_call"
        ]

        if not tool_calls:
            return response.output_text

        input_items += response.output

        for tool_call in tool_calls:

            print(
                f"\n[Agent] 调用 Tool: {tool_call.name}"
            )

            print(
                f"[Agent] 参数: {tool_call.arguments}"
            )

            arguments = json.loads(
                tool_call.arguments
            )

            result = execute_tool(
                tool_call.name,
                arguments,
            )

            print(
                f"[Tool] 执行完成"
            )

            input_items.append(
                {
                    "type": "function_call_output",
                    "call_id": tool_call.call_id,
                    "output": json.dumps(
                        result,
                        ensure_ascii=False,
                        default=str,
                    ),
                }
            )


def main():

    question = input(
        "请输入你的问题："
    ).strip()

    print("\n========== Agent ==========\n")

    answer = run_agent(question)

    print("\n========== 最终回答 ==========\n")

    print(answer)


if __name__ == "__main__":
    main()
