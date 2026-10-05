import os

from dotenv import load_dotenv
from openai import OpenAI

from schema import DATABASE_SCHEMA


load_dotenv()

client = OpenAI(
    #api_key=os.getenv('DEEPSEEK_API_KEY'),
    api_key="sk-13111e3767894ddea5c899adbc1be6f1",
    base_url="https://api.deepseek.com")


def generate_sql(question: str) -> str:

    prompt = f"""
你是一名资深数据工程师。

你的任务是把用户的自然语言问题转换成 PostgreSQL SQL。

数据库结构如下：

{DATABASE_SCHEMA}

请遵守以下规则：

1. 只能使用数据库中存在的表和字段。
2. 只生成 SELECT 查询。
3. 不允许 INSERT。
4. 不允许 UPDATE。
5. 不允许 DELETE。
6. 不允许 DROP。
7. 不允许 ALTER。
8. 不允许修改数据库。
9. SQL 必须使用 PostgreSQL 语法。
10. 订单金额统计默认只统计 status = 'paid' 的订单。
11. 只返回 SQL，不要解释。
12. 如果查询明细数据，默认最多返回 100 条。
13. 如果用户明确要求 TOP N，则使用 LIMIT N。
14. 如果用户没有要求大量明细，不要返回大规模原始数据。

用户问题：

{question}
"""

    response = client.responses.create(
        model="deepseek-flash",
        input=prompt
    )

    return response.output_text.strip()


if __name__ == "__main__":

    question = "查询过去30天每天的销售额"

    sql = generate_sql(question)

    print("用户问题：")
    print(question)

    print("\n生成的 SQL：")
    print(sql)
