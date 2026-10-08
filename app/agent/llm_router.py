import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from app.agent.router import RouteDecision
from app.agent.router_schema import ROUTER_SCHEMA

load_dotenv()


MODEL = "deepseek-flash"


ROUTER_PROMPT = """
你是一个 AI Data Agent 的 Router。

你的任务不是回答用户问题，而是判断这个问题应该交给哪一种 Agent/Workflow。

可选 route：

1. knowledge
   用户主要询问知识、原理、概念、技术文档。

2. data_query
   用户需要查询数据库中的实际业务数据。

3. analysis
   用户需要分析、诊断、解释原因。
   通常需要组合多个工具。

4. system
   用户询问系统当前状态、运行状态、元数据。

允许的工具：

- rag_search
- run_sql
- kafka_status
- flink_status
- iceberg_metadata

规则：

1. 只输出结构化决策。
2. 不要回答用户的问题。
3. 不要执行任何工具。
4. tools 只能从允许的工具列表中选择。
5. 如果需要多个工具，可以返回多个 tools。
6. analysis 通常可以同时使用 run_sql 和 rag_search。
7. system 优先使用系统状态工具。
8. knowledge 通常优先使用 rag_search。
"""


class LLMRouter:

    def __init__(self, client=None):

        if client is not None:
            self.client = client
            return

        api_key = os.getenv("DEEPSEEK_API_KEY")
        base_url = os.getenv("DEEPSEEK_BASE_URL")

        if not api_key:
            raise ValueError(
                "DEEPSEEK_API_KEY is not configured"
            )

        if not base_url:
            raise ValueError(
                "DEEPSEEK_BASE_URL is not configured"
            )

        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )

    def route(self, query: str) -> RouteDecision:

        response = self.client.responses.create(
            model=MODEL,
            input=[
                {
                    "role": "system",
                    "content": ROUTER_PROMPT,
                },
                {
                    "role": "user",
                    "content": query,
                },
            ],
            tools=[
                {
                    "type": "function",
                    "name": "route_request",
                    "description": (
                        "决定用户请求应该进入哪个 Agent route"
                    ),
                    "parameters": ROUTER_SCHEMA,
                }
            ],
        )

        for item in response.output:

            if item.type == "function_call":

                arguments = json.loads(
                    item.arguments
                )

                return RouteDecision(
                    route=arguments["route"],
                    intent=arguments["intent"],
                    tools=arguments["tools"],
                    reason=arguments["reason"],
                )

        raise RuntimeError(
            "LLM Router did not return route_request function call"
        )
