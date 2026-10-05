import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("DASHSCOPE_BASE_URL"),
)

texts = [
    "订单数据每天凌晨 2 点同步到数据仓库。",
    "用户信息每天凌晨 3 点同步到数据仓库。",
    "Kafka 用于实时传输订单事件。",
    "Flink 用于实时计算订单指标。",
    "北京今天的天气很好。",
]


response = client.embeddings.create(
    model="qwen3.7-text-embedding",
    input=texts,
)


for text, item in zip(texts, response.data):
    print("=" * 60)
    print(text)
    print("dimensions:", len(item.embedding))
    print("first 10:", item.embedding[:10])
