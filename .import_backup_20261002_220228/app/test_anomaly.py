from result_store import result_store
from tools.anomaly_tool import detect_anomaly


columns = ["day", "sales"]

rows = [
    ("2026-09-01", 100),
    ("2026-09-02", 105),
    ("2026-09-03", 98),
    ("2026-09-04", 103),
    ("2026-09-05", 101),
    ("2026-09-06", 500),
    ("2026-09-07", 99),
]

result_id = result_store.save(
    columns=columns,
    rows=rows,
)

result = detect_anomaly(result_id)

print(result)
