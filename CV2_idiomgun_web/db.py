# db.py  ── SQLite 積分榜資料層

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "leaderboard.db")


def _conn():
    return sqlite3.connect(DB_PATH)


def init_db():
    """建立資料表（若不存在）"""
    with _conn() as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                name      TEXT    NOT NULL,
                score     INTEGER NOT NULL,
                total     INTEGER NOT NULL DEFAULT 100,
                created_at DATETIME DEFAULT (datetime('now','localtime'))
            )
        """)
        c.commit()


def save_score(name: str, score: int, total: int = 100) -> dict:
    """儲存一筆分數，回傳插入的資料"""
    name = name.strip()[:20] or "匿名"
    with _conn() as c:
        cur = c.execute(
            "INSERT INTO scores (name, score, total) VALUES (?, ?, ?)",
            (name, score, total)
        )
        c.commit()
        return {"id": cur.lastrowid, "name": name, "score": score}


def get_top(limit: int = 10) -> list[dict]:
    """取得前 N 名（分數高→低，同分依時間早→晚）"""
    with _conn() as c:
        rows = c.execute(
            """SELECT id, name, score, total, created_at
               FROM scores
               ORDER BY score DESC, created_at ASC
               LIMIT ?""",
            (limit,)
        ).fetchall()
    return [
        {"rank": i + 1, "id": r[0], "name": r[1], "score": r[2],
         "total": r[3], "time": r[4]}
        for i, r in enumerate(rows)
    ]

def delete_score(score_id: int) -> bool:
    with _conn() as c:
        cur = c.execute(
            "DELETE FROM scores WHERE id = ?",
            (score_id,)
        )
        c.commit()

        if cur.rowcount > 0:
            print(f"成功刪除 id = {score_id}")
            return True
        else:
            print("找不到資料")
            return False

if __name__ == "__main__":
    print("目前資料：")
    print(get_top())

    print("刪除 id=：", delete_score(5)) #要刪除的資料(玩家名稱)

    print("刪除後：")
    print(get_top())