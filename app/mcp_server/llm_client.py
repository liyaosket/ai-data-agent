import asyncio
import json
import os

from openai import OpenAI
from mcp.client import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

from dotenv import load_dotenv
load_dotenv()


MODEL = "deepseek-flash"

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)


def mcp_tool_to_openai_tool(tool):
    return {
        "type": "function",
        "name": tool.name,
        "description": tool.description or "",
        "parameters": tool.input_schema,
    }


async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "app.mcp_server.basic_server"],
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(
            read_stream,
            write_stream,
        ) as session:

            # --------------------------------------------------
            # 1. Initialize MCP
            # --------------------------------------------------

            await session.initialize()

            # --------------------------------------------------
            # 2. Dynamically discover MCP tools
            # --------------------------------------------------

            tool_result = await session.list_tools()

            mcp_tools = tool_result.tools

            print("Discovered MCP tools:")

            for tool in mcp_tools:
                print(f"- {tool.name}")

            # --------------------------------------------------
            # 3. Convert MCP tools -> LLM tools
            # --------------------------------------------------

            llm_tools = [
                mcp_tool_to_openai_tool(tool)
                for tool in mcp_tools
            ]

            # --------------------------------------------------
            # 4. User question
            # --------------------------------------------------

            question = "查询昨天支付订单数量"

            input_items = [
                {
                    "role": "user",
                    "content": question,
                }
            ]

            # --------------------------------------------------
            # 5. Agent Loop
            # --------------------------------------------------

            while True:

                print("\n========== LLM ==========")

                response = client.responses.create(
                    model=MODEL,
                    input=input_items,
                    tools=llm_tools,
                )

                # 非常重要：
                # 把 LLM 的完整 output 加回 conversation
                input_items += response.output

                # --------------------------------------------------
                # 6. 找 Function Tool Call
                # --------------------------------------------------

                tool_calls = [
                    item
                    for item in response.output
                    if item.type == "function_call"
                ]

                # 没有 Tool Call
                # => LLM 已经可以直接回答
                if not tool_calls:
                    print("\n========== FINAL ANSWER ==========")
                    print(response.output_text)
                    break

                # --------------------------------------------------
                # 7. Execute MCP Tools
                # --------------------------------------------------

                for tool_call in tool_calls:

                    tool_name = tool_call.name

                    arguments = json.loads(
                        tool_call.arguments
                    )

                    print(
                        f"\n[MCP TOOL CALL] "
                        f"{tool_name}"
                    )

                    print(
                        "[Arguments]",
                        arguments
                    )

                    # ------------------------------------------
                    # 8. 调用 MCP Server
                    # ------------------------------------------

                    tool_result = await session.call_tool(
                        tool_name,
                        arguments=arguments,
                    )

                    print(
                        "[MCP TOOL RESULT]",
                        tool_result,
                    )

                    # ------------------------------------------
                    # 9. 把 MCP Tool Result 返回给 LLM
                    # ------------------------------------------

                    input_items.append(
                        {
                            "type": "function_call_output",
                            "call_id": tool_call.call_id,
                            "output": str(tool_result),
                        }
                    )


if __name__ == "__main__":
    asyncio.run(main())
