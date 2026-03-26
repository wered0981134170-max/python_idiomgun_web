# ============================================================
# idiom_data.py
# 成語資料庫 + 題目產生器
# ============================================================
import random

idioms = {

#===================== 2字

"畫蛇添足":{
    0:{"easy":["劃"],"medium":["晝"],"hard":["書"]},
    1:{"easy":["它"]},
    2:{"easy":["填"],"medium":["婖"]}
},

"一鼓作氣":{
    1:{"easy":["股"]},
    2:{"easy":["做"]},
    3:{"easy":["汽"],"medium":["棄"]}
},

"破釜沉舟":{
    0:{"easy":["坡"],"medium":["波"],"hard":["披"]},
    1:{"easy":["斧"]},
    2:{"medium":["沈"]}
},

"一目了然":{
    1:{"easy":["自"],"medium":["且"],"hard":["日"]},
    2:{"easy":["瞭"]},
    3:{"easy":["燃"],"hard":["染"]}
},

"一箭雙鵰":{
    1:{"easy":["剪"],"medium":["劍"]},
    2:{"hard":["爽"]},
    3:{"easy":["雕"],"medium":["凋"],"hard":["鯛"]}
},

"虎視眈眈":{
    1:{"easy":["式"],"medium":["士"],"hard":["示"]},
    2:{"easy":["耽"]},
    3:{"easy":["耽"]}
},

"青出於藍":{
    0:{"easy":["清"]},
    2:{"hard":["于"]},
    3:{"medium":["籃"]}
},

"當機立斷":{
    0:{"easy":["檔"],"medium":["擋"]},
    1:{"easy":["基"],"hard":["奇"]},
    3:{"easy":["段"],"hard":["鍛"]}
},

"半途而廢":{
    0:{"easy":["牛"],"hard":["丰"]},
    1:{"easy":["圖"],"medium":["徒"],"hard":["徙"]},
    3:{"easy":["費"]}
},

"如魚得水":{
    0:{"hard":["奴"]},
    1:{"easy":["漁"]},
    2:{"easy":["德"]}
},

#===================== 4字（保留空位供日後新增）

}

options_pool = list("家國山水風雲花草人口手足心肝腦頭耳目鼻天地日月星空海河湖江田土木火金石")

# ────────────────────────────────────────────────────────────
# 成語解析（請依格式補充內容，key 為成語）
# ────────────────────────────────────────────────────────────
explanations = {
    "畫蛇添足": "「畫」一條「蛇」，又「添」上腳",
    "一鼓作氣": "打一次「鼓」，「作」出「氣勢」",
    "破釜沉舟": "「打破」「鍋釜」，「沉」掉「船」",
    "一目了然": "「一眼」看去，「了解」「然後」全懂",
    "一箭雙鵰": "「一箭」射出，「中」兩隻「鳥」",
    "虎視眈眈": "虎在「看」，「眈眈」地盯著",
    "青出於藍": "「青色」「出自於」「藍色」之調配",
    "當機立斷": "「當下的」「機會」立刻「判斷」要不要",
    "半途而廢": "都到了「一半的路途」，就「作廢」掉了",
    "如魚得水": "「就如」一條「魚」「得到了」水",
}

DIFFICULTY_ORDER = ["easy", "medium", "hard"]

def _pick_wrong_char(pos_data: dict, difficulty: str) -> str | None:
    order = [difficulty] + [d for d in DIFFICULTY_ORDER if d != difficulty]
    for d in order:
        if d in pos_data and pos_data[d]:
            return random.choice(pos_data[d])
    return None


def make_wrong_question(idiom: str, difficulty: str = "easy") -> dict | None:
    pos_data = idioms.get(idiom, {})
    if not pos_data:
        return None

    valid_positions = list(pos_data.keys())
    if not valid_positions:
        return None

    pos = random.choice(valid_positions)
    wrong_char = _pick_wrong_char(pos_data[pos], difficulty)
    if wrong_char is None:
        return None

    correct_char = idiom[pos]
    display = list(idiom)
    display[pos] = wrong_char
    display_str = "".join(display)

    return {
        "type":         "wrong",
        "idiom":        idiom,
        "display":      display_str,
        "wrong_idx":    pos,
        "wrong_char":   wrong_char,
        "correct_char": correct_char,
        "hint":         "找出錯字並秒準 1.5 秒",
        "difficulty":   difficulty,
        "explanation":  explanations.get(idiom, ""),
    }


def make_fill_question(idiom: str, difficulty: str = "easy") -> dict | None:
    pos_data = idioms.get(idiom, {})
    valid_positions = list(pos_data.keys())
    if not valid_positions:
        pos = random.randint(0, len(idiom)-1)
        distractors = []
    else:
        pos = random.choice(valid_positions)
        distractors = []
        for d in DIFFICULTY_ORDER:
            if d in pos_data[pos]:
                distractors.extend(pos_data[pos][d])
        if difficulty == "easy":
            preferred = pos_data[pos].get("easy", [])
            distractors = preferred if preferred else distractors
        elif difficulty == "medium":
            preferred = (pos_data[pos].get("easy", []) +
                         pos_data[pos].get("medium", []))
            distractors = preferred if preferred else distractors

    correct_char = idiom[pos]
    distractors  = [c for c in distractors if c != correct_char]

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

    template = list(idiom)
    template[pos] = "＿"
    template_str = "".join(template)

    return {
        "type":       "fill",
        "idiom":      idiom,
        "template":   template_str,
        "blank_idx":  pos,
        "answer":     correct_char,
        "options":    options[:4],
        "hint":       "秒準正確的字 1.5 秒",
        "difficulty": difficulty,
        "explanation": explanations.get(idiom, ""),
    }


def generate_questions(
    n: int = 10,
    difficulty: str = "mixed",
    wrong_ratio: float = 0.5,
) -> list[dict]:
    all_idioms = list(idioms.keys())
    random.shuffle(all_idioms)

    n_wrong = round(n * wrong_ratio)
    n_fill  = n - n_wrong

    def _random_diff():
        if difficulty == "mixed":
            return random.choice(["easy", "medium", "hard"])
        return difficulty

    # 選錯字題：每個成語最多出一題
    wrong_qs = []
    pool = all_idioms[:]
    random.shuffle(pool)
    for idiom in pool:
        if len(wrong_qs) >= n_wrong:
            break
        q = make_wrong_question(idiom, _random_diff())
        if q:
            wrong_qs.append(q)

    # 填空題：每個成語最多出一題（可與選錯字重複用同成語）
    fill_qs = []
    pool = all_idioms[:]
    random.shuffle(pool)
    for idiom in pool:
        if len(fill_qs) >= n_fill:
            break
        q = make_fill_question(idiom, _random_diff())
        if q:
            fill_qs.append(q)

    # 若還不夠，兩種題型都允許重複出同一成語補足
    questions = wrong_qs + fill_qs
    if len(questions) < n:
        extra_needed = n - len(questions)
        pool = all_idioms[:]
        random.shuffle(pool)
        toggle = True
        for idiom in pool * 3:   # 最多繞三圈
            if extra_needed <= 0:
                break
            if toggle:
                q = make_wrong_question(idiom, _random_diff())
            else:
                q = make_fill_question(idiom, _random_diff())
            if q:
                questions.append(q)
                extra_needed -= 1
            toggle = not toggle

    random.shuffle(questions)
    return questions[:n]


if __name__ == "__main__":
    qs = generate_questions(n=10, difficulty="easy", wrong_ratio=0.5)
    for i, q in enumerate(qs, 1):
        print(f"[{i}] {q['type']:5s} | {q.get('display') or q.get('template'):6s} "
              f"| ans={q.get('wrong_char') or q.get('answer')} "
              f"| difficulty={q['difficulty']}")
        if q["type"] == "fill":
            print(f"       options={q['options']}")
