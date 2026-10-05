import re

MAX_SQL_LENGTH = 5000
FORBIDDEN_KEYWORDS = [
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "GRANT",
    "REVOKE",
]


def validate_sql(sql: str) -> tuple[bool, str]:

    sql = sql.strip()

    if len(sql) > MAX_SQL_LENGTH:
        return False, "SQL 长度超过限制"

    if not sql:
        return False, "SQL 为空"

    # 禁止多条 SQL
    statements = [
        statement.strip()
        for statement in sql.split(";")
        if statement.strip()
    ]

    if len(statements) != 1:
        return False, "只允许执行一条 SQL"

    normalized_sql = sql.upper()

    # 必须 SELECT
    if not normalized_sql.startswith("SELECT"):
        return False, "只允许执行 SELECT 查询"

    # 禁止危险操作
    for keyword in FORBIDDEN_KEYWORDS:

        pattern = rf"\b{keyword}\b"

        if re.search(pattern, normalized_sql):

            return False, f"禁止执行 {keyword} 操作"

    return True, "SQL 检查通过"
