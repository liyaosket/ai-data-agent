from app.chunker import TextChunker


document = """
Kafka 是一个分布式事件流平台。

在数据平台中，Kafka 通常用于实时传输订单事件、
用户行为事件和业务日志。

Kafka Consumer 负责读取 Kafka Topic 中的数据。

Consumer 需要维护 offset，用于记录当前消费位置。

如果 Consumer 处理失败，可以根据 offset 重新消费消息。

Flink 可以从 Kafka 读取数据，并进行实时计算。

Flink Checkpoint 用于保存计算状态，
从而在任务失败后恢复计算。
"""


chunker = TextChunker(
    chunk_size=100,
    overlap=20,
)


chunks = chunker.split(document)


for index, chunk in enumerate(chunks):

    print("=" * 60)
    print(f"CHUNK {index}")
    print("=" * 60)

    print(chunk)
