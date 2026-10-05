import sqlite3
import json
from datetime import datetime
from pathlib import Path

class MetricsBackend:


    def __init__(
        self,
        db_path=None,
    ):

        if db_path is None:

            project_root = (
                Path(__file__)
                .resolve()
                .parent
                .parent
            )

            db_path = (
                project_root
                / "metrics.db"
            )

        self.db_path = str(db_path)

        self.init_db()

    def connect(self):

        return sqlite3.connect(
            self.db_path
        )


    def init_db(self):

        conn = self.connect()

        cursor = conn.cursor()


        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS metrics_snapshot (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                timestamp TEXT NOT NULL,

                data TEXT NOT NULL

            )
            """
        )


        conn.commit()

        conn.close()



    def save(
        self,
        metrics,
    ):

        conn = self.connect()

        cursor = conn.cursor()


        cursor.execute(
            """
            INSERT INTO metrics_snapshot
            (
                timestamp,
                data
            )
            VALUES
            (?,?)
            """,
            (
                datetime.utcnow()
                .isoformat(),

                json.dumps(
                    metrics,
                    ensure_ascii=False,
                ),
            )
        )


        conn.commit()

        conn.close()



    def latest(self):

        conn = self.connect()

        cursor = conn.cursor()


        cursor.execute(
            """
            SELECT data
            FROM metrics_snapshot
            ORDER BY id DESC
            LIMIT 1
            """
        )


        row = cursor.fetchone()


        conn.close()


        if not row:

            return None


        return json.loads(
            row[0]
        )
