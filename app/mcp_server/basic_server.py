from mcp.server.mcpserver import MCPServer

from app.query import execute_query
from app.schema import DATABASE_SCHEMA
from app.sql_validator import validate_sql


server = MCPServer("AI Data Agent PostgreSQL")


@server.tool()
def get_schema() -> str:
    """
    Get the database schema available to the AI Data Agent.
    """
    return DATABASE_SCHEMA


@server.tool()
def run_sql(sql: str) -> str:
    """
    Execute a read-only SQL query against the AI Data Agent PostgreSQL database.
    """

    validate_sql(sql)

    rows = execute_query(sql)

    return str(rows)


if __name__ == "__main__":
    server.run()
