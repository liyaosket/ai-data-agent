from dataclasses import dataclass

from app.agent.router import RouteDecision


@dataclass
class RouteContext:
    decision: RouteDecision

    def to_dict(self):
        return {
            "route": self.decision.route,
            "intent": self.decision.intent,
            "tools": self.decision.tools,
            "reason": self.decision.reason,
        }
