from app.db import get_connection


QUERY_TIMEOUT_MS = 5000
MAX_RESULT_ROWS = 1000


def execute_query(sql: str):

    conn = get_connection()

    try:

        with conn.cursor() as cursor:

            cursor.execute(
                f"SET statement_timeout = {QUERY_TIMEOUT_MS}"
            )

            cursor.execute(sql)

            columns = [
                description[0]
                for description in cursor.description
            ]

            rows = cursor.fetchmany(MAX_RESULT_ROWS + 1)

            if len(rows) > MAX_RESULT_ROWS:
                raise ValueError(
                    f"查询结果超过 {MAX_RESULT_ROWS} 行"
                )

            return columns, rows

    finally:
        conn.close()
