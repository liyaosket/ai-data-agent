class MockLLM:

    def generate(self, system_prompt, user_prompt):
        return (
            "这是一个模拟 LLM 响应。\n\n"
            "LLM 收到的 System Prompt:\n"
            f"{system_prompt}\n\n"
            "LLM 收到的 User Prompt:\n"
            f"{user_prompt}"
        )
