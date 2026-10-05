from dataclasses import dataclass
from typing import Literal


from dataclasses import dataclass
from typing import Literal


RouteType = Literal[
    "knowledge",
    "data_query",
    "analysis",
    "system",
]


@dataclass
class RouteDecision:
    route: RouteType
    intent: str
    tools: list[str]
    reason: str

class AgentRouter:

    def route(self, query: str) -> RouteDecision:
        q = query.lower()

        # 知识库 / 技术原理类问题
        knowledge_keywords = [
            "为什么",
            "什么是",
            "原理",
            "区别",
            "如何实现",
            "怎么实现",
            "kafka offset",
            "consumer group",
            "flink checkpoint",
            "iceberg",
        ]

        for keyword in knowledge_keywords:
            if keyword.lower() in q:
                return RouteDecision(
                    route="knowledge",
                    reason="检测到技术知识或原理类问题",
                )

        # 数据查询类问题
        data_keywords = [
            "多少",
            "数量",
            "订单量",
            "销售额",
            "统计",
            "查询",
            "top",
            "排名",
        ]

        for keyword in data_keywords:
            if keyword.lower() in q:
                return RouteDecision(
                    route="data_query",
                    reason="检测到数据查询或统计需求",
                )

        # 分析类问题
        analysis_keywords = [
            "分析",
            "原因",
            "为什么下降",
            "趋势",
            "异常",
            "对比",
        ]

        for keyword in analysis_keywords:
            if keyword.lower() in q:
                return RouteDecision(
                    route="analysis",
                    reason="检测到数据分析需求",
                )

        # 系统类问题
        system_keywords = [
            "kafka 状态",
            "kafka lag",
            "consumer lag",
            "flink job",
            "flink 作业",
            "iceberg 表",
            "checkpoint 状态",
        ]

        for keyword in system_keywords:
            if keyword.lower() in q:
                return RouteDecision(
                    route="system",
                    reason="检测到基础设施或系统状态查询",
                )

        # 默认走知识库
        return RouteDecision(
            route="knowledge",
            reason="无法明确分类，默认使用知识库检索",
        )
