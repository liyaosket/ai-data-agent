from planner import create_plan


question = "帮我分析最近30天的业务情况"

plan = create_plan(question)

print("\n========== PLAN ==========\n")

print(plan)

print("\n========== TASKS ==========\n")

for task in plan["tasks"]:
    print(
        f"{task['id']}: "
        f"{task['description']}"
    )
