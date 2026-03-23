# ============================================================
# idiom_quiz.py
# 整合 DB 版：成語資料庫 + 題目產生器
# ============================================================
import random
from idiom_data import options_pool
from dataBase import IdiomDBManager, Idiom

# 1. 初始化資料庫連線
db = IdiomDBManager("sqlite:///idiom_game.db")

DIFFICULTY_ORDER = ["easy", "medium", "hard"]
DIFF_MAP = {"easy": 1, "medium": 2, "hard": 3}

from sqlalchemy.sql.expression import func


def get_random_idioms(limit_num: int) -> list[str]:
    """直接讓 SQLite 隨機排序並只取需要的數量"""
    with db.Session() as session:
        # ORDER BY RANDOM() 在資料庫層面打亂，LIMIT 限制回傳筆數
        idioms = session.query(Idiom).order_by(func.random()).limit(limit_num).all()
        return [i.word for i in idioms]


def make_wrong_question(idiom_word: str, difficulty: str = "easy") -> dict | None:
    db_data = db.get_idiom(idiom_word)
    if not db_data or not db_data["distractors"]:
        return None

    # 將 DB 拉出來的 flat list 整理成以 pos 為 key 的結構，方便隨機抽位置
    pos_dict = {}
    for d in db_data["distractors"]:
        pos = d["pos"]
        if pos not in pos_dict:
            pos_dict[pos] = {}
        diff_str = [k for k, v in DIFF_MAP.items() if v == d["difficulty"]][0]
        if diff_str not in pos_dict[pos]:
            pos_dict[pos][diff_str] = []
        pos_dict[pos][diff_str].append(d["char"])

    valid_positions = list(pos_dict.keys())
    if not valid_positions:
        return None

    pos = random.choice(valid_positions)
    pos_data = pos_dict[pos]

    # 依照原本的難度降級尋找邏輯
    order = [difficulty] + [d for d in DIFFICULTY_ORDER if d != difficulty]
    wrong_char = None
    for d_level in order:
        if d_level in pos_data and pos_data[d_level]:
            wrong_char = random.choice(pos_data[d_level])
            break

    if not wrong_char:
        return None

    correct_char = idiom_word[pos]
    display = list(idiom_word)
    display[pos] = wrong_char
    display_str = "".join(display)

    return {
        "type": "wrong",
        "idiom": idiom_word,
        "display": display_str,
        "wrong_idx": pos,
        "wrong_char": wrong_char,
        "correct_char": correct_char,
        "hint": "找出錯字並秒準 1.5 秒",
        "difficulty": difficulty,
    }


def make_fill_question(idiom_word: str, difficulty: str = "easy") -> dict | None:
    db_data = db.get_idiom(idiom_word)

    if not db_data or not db_data["distractors"]:
        pos = random.randint(0, len(idiom_word) - 1)
        distractors = []
    else:
        # 找出有設定干擾字的位置
        valid_positions = list(set([d["pos"] for d in db_data["distractors"]]))
        pos = random.choice(valid_positions)

        # 依照難度過濾允許的干擾字
        allowed_diffs = []
        if difficulty == "easy":
            allowed_diffs = [1]
        elif difficulty == "medium":
            allowed_diffs = [1, 2]
        else:  # hard
            allowed_diffs = [1, 2, 3]

        distractors = [
            d["char"]
            for d in db_data["distractors"]
            if d["pos"] == pos and d["difficulty"] in allowed_diffs
        ]

        # 若該難度沒有對應的字，降級抓取該位置的所有字
        if not distractors:
            distractors = [d["char"] for d in db_data["distractors"] if d["pos"] == pos]

    correct_char = idiom_word[pos]

    # 強制排除正確解答，避免選項重複的 Bug
    distractors = [c for c in distractors if c != correct_char]

    options = [correct_char]
    for c in distractors:
        if c not in options:
            options.append(c)
        if len(options) == 4:
            break

    pool_copy = [c for c in options_pool if c not in options]
    random.shuffle(pool_copy)
    while len(options) < 4 and pool_copy:
        options.append(pool_copy.pop())

    random.shuffle(options)

    template = list(idiom_word)
    template[pos] = "＿"
    template_str = "".join(template)

    return {
        "type": "fill",
        "idiom": idiom_word,
        "template": template_str,
        "blank_idx": pos,
        "answer": correct_char,
        "options": options[:4],
        "hint": "秒準正確的字 1.5 秒",
        "difficulty": difficulty,
    }


def generate_questions(
    n: int = 10,
    difficulty: str = "mixed",
    wrong_ratio: float = 0.5,
) -> list[dict]:

    # 為了防止某些成語無法產出題目（例如缺乏干擾字），多抓一倍的備用池
    pool = get_random_idioms(n * 2)

    if not pool:
        print("警告：資料庫中沒有成語資料！")
        return []

    n_wrong = round(n * wrong_ratio)
    questions = []
    wrong_count = 0
    fill_count = 0

    def _random_diff():
        return (
            random.choice(["easy", "medium", "hard"])
            if difficulty == "mixed"
            else difficulty
        )

    # 直接遍歷隨機池產出題目
    for idiom in pool:
        if len(questions) >= n:
            break

        q = None
        # 優先滿足找錯字題的數量
        if wrong_count < n_wrong:
            q = make_wrong_question(idiom, _random_diff())
            if q:
                wrong_count += 1
        # 錯字題滿了，或錯字題產出失敗，改作填空題
        if not q:
            q = make_fill_question(idiom, _random_diff())
            if q:
                fill_count += 1

        if q:
            questions.append(q)

    # 最後把題目順序打亂，避免前面全是錯字題、後面全是填空題
    random.shuffle(questions)
    return questions


if __name__ == "__main__":
    qs = generate_questions(n=10, difficulty="mixed", wrong_ratio=0.5)
    for i, q in enumerate(qs, 1):
        print(
            f"[{i}] {q['type']:5s} | {q.get('display') or q.get('template'):6s} "
            f"| ans={q.get('wrong_char') or q.get('answer')} "
            f"| difficulty={q['difficulty']}"
        )
        if q["type"] == "fill":
            print(f"       options={q['options']}")
