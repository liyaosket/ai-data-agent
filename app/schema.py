DATABASE_SCHEMA = """
数据库名称：ecommerce

表 users：
- id BIGINT，用户ID
- username VARCHAR，用户名
- region VARCHAR，地区
- created_at TIMESTAMP，用户创建时间

表 products：
- id BIGINT，商品ID
- product_name VARCHAR，商品名称
- category VARCHAR，商品分类
- price NUMERIC，商品价格

表 orders：
- id BIGINT，订单ID
- user_id BIGINT，对应 users.id
- product_id BIGINT，对应 products.id
- amount NUMERIC，订单金额
- status VARCHAR，订单状态
- order_time TIMESTAMP，订单时间

表关系：
- orders.user_id = users.id
- orders.product_id = products.id

订单状态：
- paid：已支付
- cancelled：已取消
"""
