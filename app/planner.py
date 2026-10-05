import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    base_url = os.getenv("DEEPSEEK_BASE_URL"))

MODEL = "deepseek-flash"


PLANNER_PROMPT = """
你是一个 AI 数据分析任务规划器。

你的职责是：
根据用户的问题，生成一个清晰、合理、可执行的数据分析计划。

注意：

1. 只负责制定计划，不执行任何 Tool。
2. 不生成 SQL。
3. 不编造数据库中的数据。
4. 每个任务应该有明确的目的。
5. 避免重复任务。
6. 如果任务之间存在依赖关系，明确 dependencies。
7. 对简单问题生成尽可能少的任务。
8. 对复杂问题拆分成多个独立任务。
9. 使用中文。
10. 每个 Task 必须是一个独立、明确、可执行的工作单元。

11. 不要创建重复或高度重叠的 Task。

12. 如果多个后续任务需要同一份数据，
    应该让一个 Task 负责获取数据，
    后续 Task 通过 dependencies 复用该 Task 的结果。

13. 如果一个 Task 的结果可以被多个 Task 使用，
    优先设计成共享依赖，而不是重复查询。

14. Task description 必须明确说明：
    - 要分析什么
    - 时间范围
    - 必要的过滤条件
    - 期望结果

15. 如果任务需要先获取数据，
    将“获取数据”和“分析数据”拆成合理的 Task。

16. 图表生成应该作为独立 Task，
    不要与数据查询 Task 混合。

17. 异常检测应该作为独立 Task，
    不要与数据查询 Task 混合。

18. dependencies 只能引用当前 Plan 中已经存在的 Task id。

19. 如果提供了 ROUTER DECISION：
    - 必须尊重 Router 给出的 route。
    - 必须围绕 Router 给出的 intent 制定计划。
    - 优先考虑 Router 推荐的 tools。
    - 不要生成明显超出 Router 意图范围的任务。
    - Router 只负责提供路由和能力提示，
      不决定最终 Task 数量。
    - Planner 仍然负责决定 Task 拆分、
      dependencies 和执行顺序。

20. 数据获取 Task 与数据分析 Task 应尽量分离。
    数据获取 Task 负责产生可复用的数据结果；
    后续分析 Task 应通过 dependencies 复用已有结果。

21. 如果两个 Task 可以独立执行，
    且一个 Task 不需要另一个 Task 的具体结果，
    则不要设置 dependency。
    Planner 应优先产生可以并行执行的 Task。

22. 避免无意义的串行依赖。
    不要仅因为两个 Task 都分析同一个业务问题，
    就让后一个 Task 依赖前一个 Task。

23. 对于复杂分析问题，
    优先采用“核心指标 → 维度下钻 → 深度分析”的渐进式分析方式。
    不要一开始就查询大量无关维度。

24. 单个数据获取 Task 不应一次性包含过多独立分析维度。
    如果多个维度属于不同分析目的，
    应根据后续分析需要合理拆分。

25. 如果多个 Task 需要相同的数据，
    应优先设计共享的数据获取 Task，
    后续 Task 通过 dependencies 复用其 result，
    禁止重复查询同一份数据。

26. Planner 的目标不是生成最多 Task，
    而是在保证分析完整性的前提下，
    用尽可能少的 Task 构建清晰、高效、可并行的 DAG。

27. 对于“为什么/原因/诊断”类问题，
    应优先建立：
    基础指标 → 定位异常维度 → 原因验证 → 综合结论
    的分析链路，
    而不是同时展开大量平行维度分析。

28. 图表 Task 应尽可能复用已有分析结果，
    不应为了生成图表而重新查询已经存在的数据。

29. 每个 Task 必须遵循最小任务原则：
    一个 Task 只完成一个明确动作。
    不要把数据获取、数据分析、异常检测、图表生成混合在同一个 Task 中。
"""


PLAN_SCHEMA = {
    "type": "object",
    "properties": {
        "goal": {
            "type": "string"
        },
        "tasks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string"
                    },
                    "description": {
                        "type": "string"
                    },
                    "dependencies": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    }
                },
                "required": [
                    "id",
                    "description",
                    "dependencies"
                ],
                "additionalProperties": False
            }
        }
    },
    "required": [
        "goal",
        "tasks"
    ],
    "additionalProperties": False
}


def create_plan(
    question: str,
    route_decision=None,
) -> dict:

    planner_input = []

    if route_decision is not None:

        route_context = {
            "route": route_decision.route,
            "intent": route_decision.intent,
            "tools": route_decision.tools,
            "reason": route_decision.reason,
        }

        planner_input.append(
            {
                "role": "system",
                "content": (
                    "===== ROUTER DECISION =====\n"
                    + json.dumps(
                        route_context,
                        ensure_ascii=False,
                        indent=2,
                    )
                    + "\n===== END ROUTER DECISION ====="
                ),
            }
        )

    planner_input.append(
        {
            "role": "user",
            "content": question,
        }
    )

    response = client.responses.create(
        model=MODEL,
        instructions=PLANNER_PROMPT,
        input=planner_input,
        text={
            "format": {
                "type": "json_schema",
                "name": "analysis_plan",
                "strict": True,
                "schema": PLAN_SCHEMA,
            }
        },
    )

    return json.loads(response.output_text)
