import random
from datetime import datetime, timedelta

import psycopg2
from faker import Faker


fake = Faker()

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="ecommerce",
    user="dev",
    password="dev123456",
)

cursor = conn.cursor()

regions = ["华东", "华南", "华北", "西南", "西北"]
categories = ["手机", "电脑", "家电", "服装", "食品"]


print("Generating users...")

users = []

for i in range(1, 10001):
    users.append(
        (
            fake.user_name(),
            random.choice(regions),
            fake.date_time_between(
                start_date="-2y",
                end_date="now",
            ),
        )
    )

cursor.executemany(
    """
    INSERT INTO users(username, region, created_at)
    VALUES (%s, %s, %s)
    """,
    users,
)

conn.commit()


print("Generating products...")

products = []

for i in range(1, 1001):
    products.append(
        (
            f"商品-{i}",
            random.choice(categories),
            round(random.uniform(10, 5000), 2),
        )
    )

cursor.executemany(
    """
    INSERT INTO products(product_name, category, price)
    VALUES (%s, %s, %s)
    """,
    products,
)

conn.commit()


print("Generating orders...")

start_date = datetime.now() - timedelta(days=365)

batch_size = 10000

for batch_start in range(0, 1_000_000, batch_size):

    orders = []

    for _ in range(batch_size):

        order_time = start_date + timedelta(
            seconds=random.randint(
                0,
                int((datetime.now() - start_date).total_seconds()),
            )
        )

        user_id = random.randint(1, 10000)
        product_id = random.randint(1, 1000)

        amount = round(random.uniform(10, 5000), 2)

        status = random.choice(
            ["paid", "paid", "paid", "cancelled"]
        )

        orders.append(
            (
                user_id,
                product_id,
                amount,
                status,
                order_time,
            )
        )

    cursor.executemany(
        """
        INSERT INTO orders(
            user_id,
            product_id,
            amount,
            status,
            order_time
        )
        VALUES (%s, %s, %s, %s, %s)
        """,
        orders,
    )

    conn.commit()

    print(
        f"Inserted {batch_start + batch_size:,} orders"
    )


cursor.close()
conn.close()

print("Done.")
