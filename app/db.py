import psycopg2


DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "ecommerce",
    "user": "ai_reader",
    "password": "ai_reader_password",
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)
