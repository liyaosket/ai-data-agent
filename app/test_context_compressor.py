from app.context_compressor import ContextCompressor



def main():

    compressor = ContextCompressor()


    documents = [
        {
            "content":
            """
            Kafka 是一个分布式事件流平台。
            Consumer 通过 Consumer Group 读取 Kafka 数据。
            Offset commit 策略影响消费语义。
            Producer 写入 Topic。
            """
        }
    ]


    result = compressor.compress(
        "Kafka consumer offset commit",
        documents
    )


    print(result)



if __name__ == "__main__":
    main()
