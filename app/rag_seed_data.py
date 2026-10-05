from dataclasses import dataclass


@dataclass
class KnowledgeDocument:
    title: str
    content: str
    source_type: str = "technical_doc"


DOCUMENTS = [
    KnowledgeDocument(
        title="Kafka 基础架构",
        content="""
Kafka 是一个分布式事件流平台。
Producer 将消息写入 Kafka Topic。
Topic 可以被划分为多个 Partition。
Partition 是 Kafka 实现水平扩展和并行消费的基础。
Consumer 通过 Consumer Group 读取 Kafka 中的数据。
同一个 Consumer Group 中，一个 Partition 在同一时刻通常只会被一个 Consumer 消费。
Kafka 通过 Broker 集群提供高吞吐和高可用能力。
消息通常按照 offset 顺序存储在 Partition 中。
""",
    ),

    KnowledgeDocument(
        title="Kafka Offset",
        content="""
Kafka offset 是消息在 Partition 中的逻辑位置。
Consumer 使用 offset 表示当前消费进度。
Consumer Group 会维护消费位点。
当 Consumer 重启时，可以根据已经提交的 offset 恢复消费。
Offset commit 策略会影响消息处理语义。
自动提交 offset 使用简单，但在复杂业务场景下可能存在重复消费风险。
手动提交 offset 可以让应用在业务处理成功后再提交消费进度。
""",
    ),

    KnowledgeDocument(
        title="Flink Checkpoint",
        content="""
Flink Checkpoint 用于保存流处理作业的一致性状态。
Checkpoint 可以帮助 Flink 在发生故障后恢复计算状态。
Flink 会周期性触发 Checkpoint。
Checkpoint 的状态通常写入持久化存储。
在 Exactly-Once 场景中，Checkpoint 是重要的基础机制。
Checkpoint interval 会影响系统的恢复点和运行开销。
""",
    ),

    KnowledgeDocument(
        title="Flink State",
        content="""
Flink State 用于保存流处理过程中需要跨事件维护的数据。
常见 State 类型包括 ValueState、ListState、MapState 和 ReducingState。
Keyed State 按照 key 进行隔离。
Operator State 通常与算子的实例相关。
State Backend 决定状态如何存储以及如何进行快照。
对于大规模状态，需要考虑 RocksDB 或其他持久化状态存储方案。
""",
    ),

    KnowledgeDocument(
        title="PostgreSQL 索引",
        content="""
PostgreSQL Index 可以减少查询需要扫描的数据量。
B-tree 是 PostgreSQL 最常用的索引类型。
对于等值查询和范围查询，B-tree 通常非常有效。
Hash Index 主要适用于等值查询。
GIN Index 常用于数组、JSONB 和全文搜索场景。
BRIN Index 适合数据和物理存储顺序高度相关的大型表。
创建索引可以提高查询性能，但也会增加写入成本和存储空间。
""",
    ),

    KnowledgeDocument(
        title="PostgreSQL 事务",
        content="""
PostgreSQL 使用事务保证数据库操作的一致性。
事务具有 Atomicity、Consistency、Isolation 和 Durability 特性。
BEGIN 可以开始事务。
COMMIT 提交事务。
ROLLBACK 可以撤销当前事务中的修改。
事务隔离级别会影响并发事务之间的数据可见性。
长事务可能导致锁竞争和 MVCC 垃圾无法及时清理。
""",
    ),

    KnowledgeDocument(
        title="Redis 缓存",
        content="""
Redis 是一个内存数据存储系统。
Redis 常用于缓存、Session、排行榜和分布式锁等场景。
Redis 支持 String、Hash、List、Set 和 Sorted Set 等数据结构。
缓存系统需要考虑缓存穿透、缓存击穿和缓存雪崩。
TTL 可以控制缓存数据的生命周期。
Redis Pipeline 可以减少网络往返次数。
""",
    ),

    KnowledgeDocument(
        title="Iceberg Table",
        content="""
Apache Iceberg 是一种开放表格式。
Iceberg 支持 Schema Evolution 和 Partition Evolution。
Iceberg 使用 Snapshot 表示表在某个时间点的状态。
通过 Snapshot 可以实现 Time Travel。
Iceberg 的元数据机制可以帮助查询引擎避免扫描不必要的数据文件。
Iceberg 可以运行在对象存储之上。
""",
    ),
]


def build_documents(repetitions: int = 125):
    documents = []

    for i in range(repetitions):
        for doc in DOCUMENTS:
            documents.append(
                KnowledgeDocument(
                    title=f"{doc.title} #{i}",
                    content=doc.content,
                    source_type=doc.source_type,
                )
            )

    return documents


if __name__ == "__main__":
    documents = build_documents()

    print("Documents:", len(documents))
    print()

    for doc in documents[:3]:
        print("=" * 60)
        print(doc.title)
        print(doc.content.strip())
