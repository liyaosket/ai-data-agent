import asyncio

from mcp.client import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


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

            await session.initialize()

            result = await session.list_tools()

            print("Available MCP tools:")

            for tool in result.tools:
                print(f"\nName: {tool.name}")
                print(f"Description: {tool.description}")
                print(f"Input schema: {tool.input_schema}")


if __name__ == "__main__":
    asyncio.run(main())
