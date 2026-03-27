# idiom_data.py
# 成語資料庫 + 題目產生器


# "三思而行":{
#     1:{"easy":["恩"]}
# },

#===================== 1字

# "水落石出":{
#     1:{"easy":["洛"],"medium":["絡"],"hard":["駱"]},
#     2:{"easy":["右"]}
# },

# "手忙腳亂":{
#     1:{"easy":["茫"],"medium":["盲"],"hard":["芒"]},
#     3:{"medium":["辭"]}
# },

# "怒髮衝冠":{
#     0:{"easy":["努"],"medium":["弩"],"hard":["恕"]},
#     2:{"easy":["沖"],"medium":["充"]},
# },

# "亡羊補牢":{
#     0:{"easy":["忘"],"medium":["芒"]},
#     2:{"easy":["捕"]}
# },

# "對症下藥":{
#     0:{"easy":["隊"],"hard":["對"]},
#     1:{"easy":["証"],"medium":["政"]}
# },

#===================== 2字

# "四面楚歌":{
#     0:{"easy":["西"],"medium":["死"],"hard":["匹"]},
#     2:{"easy":["處"],"hard":["濋"]},
#     3:{"easy":["哥"]}
# },

# "刻苦耐勞":{
#     0:{"easy":["克"],"medium":["剋"]},
#     1:{"easy":["奈"]},
#     2:{"easy":["牢"]}
# },

# "五花八門":{
#     1:{"medium":["化"]},
#     2:{"easy":["人"],"medium":["入"]},
#     3:{"hard":["們"]}
# },

# "心驚膽跳":{
#     0:{"easy":["必"]},
#     2:{"easy":["擔"],"hard":["憚"]},
#     3:{"medium":["挑"],"hard":["眺"]}
# },

# "按部就班":{
#     0:{"easy":["案"],"medium":["暗"],"hard":["黯"]},
#     1:{"easy":["陪"],"medium":["步"],"hard":["倍"]},
#     3:{"easy":["般"],"medium":["斑"],"hard":["搬"]}
# },

#===================== 3字

# "守株待兔":{
#     0:{"easy":["首"],"medium":["宋"],"hard":["宇"]},
#     1:{"easy":["珠"],"medium":["殊"],"hard":["朱"]},
#     2:{"hard":["侍"]},
#     3:{"medium":["免"]}
# },

# "自相矛盾":{
#     0:{"easy":["白"],"medium":["目"],"hard":["由"]},
#     1:{"medium":["湘"],"hard":["箱"]},
#     2:{"easy":["予"],"medium":["茅"]},
#     3:{"easy":["頓"],"medium":["鈍"],"hard":["遁"]}
# },

# "魚目混珠":{
#     0:{"easy":["漁"]},
#     1:{"easy":["自"],"medium":["且"],"hard":["日"]},
#     2:{"hard":["渾"]},
#     3:{"easy":["株"],"hard":["誅"]}
# },

# "百發百中":{
#     0:{"easy":["白"]},
#     1:{"medium":["廢"]},
#     2:{"easy":["白"]},
#     3:{"easy":["忠"],"medium":["仲"]}
# },

# "名列前茅":{
#     0:{"easy":["各"],"hard":["洛"]},
#     1:{"medium":["烈"],"hard":["裂"]},
#     2:{"medium":["煎"],"hard":["箭"]},
#     3:{"medium":["矛"]}
# },

# "全神貫注":{
#     0:{"easy":["金"]},
#     1:{"easy":["伸"],"hard":["紳"]},
#     2:{"easy":["串"],"medium":["慣"],"hard":["摜"]},
#     3:{"easy":["住"],"medium":["註"],"hard":["柱"]}
# },

# "前功盡棄":{
#     0:{"easy":["剪"],"hard":["煎"]},
#     1:{"easy":["工"],"medium":["攻"],"hard":["公"]},
#     2:{"easy":["儘"],"medium":["進"],"hard":["禁"]},
#     3:{"easy":["氣"]}
# },

# "持之以恆":{
#     0:{"hard":["待"]},
#     1:{"easy":["支"]},
#     2:{"easy":["已"],"medium":["己"],"hard":["乙"]},
#     3:{"easy":["衡"]}
# },

import random

# 成語資料
idioms = {

"畫蛇添足":{
    0:["劃","晝","書"],
    1:["它"],
    2:["填","婖"]
},

"一鼓作氣":{
    1:["股"],
    2:["做"],
    3:["汽","棄"]
},

"破釜沉舟":{
    0:["坡","波","披"],
    1:["斧"],
    2:["沈"]
},

"一目了然":{
    1:["自","且","日"],
    2:["瞭"],
    3:["燃","染"]
},

"一箭雙鵰":{
    1:["剪","劍"],
    2:["爽"],
    3:["雕","凋","鯛"]
},

"虎視眈眈":{
    1:["式","士","示"],
    2:["耽"],
    3:["耽"]
},

"青出於藍":{
    0:["清"],
    2:["于"],
    3:["籃"]
},

"當機立斷":{
    0:["檔","擋"],
    1:["基","奇"],
    3:["段","鍛"]
},

"半途而廢":{
    0:["牛","丰"],
    1:["圖","徒","徙"],
    3:["費"]
},

"如魚得水":{
    0:["奴"],
    1:["漁"],
    2:["德"]
},

}

# 選項池
options_pool = list("家國山水風雲花草人口手足心肝腦頭耳目鼻天地日月星空海河湖江田土木火金石")


# 成語解析
explanations = {
    # "三思而行": "",
    # "水落石出": "",
    # "手忙腳亂": "",
    # "怒髮衝冠": "",
    # "亡羊補牢": "",
    # "對症下藥": "",
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
    # "四面楚歌": "",
    # "刻苦耐勞": "",
    # "五花八門": "",
    # "心驚膽跳": "",
    # "按部就班": "",
    # "守株待兔": "",
    # "自相矛盾": "",
    # "魚目混珠": "",
    # "百發百中": "",
    # "名列前茅": "",
    # "全神貫注": "",
    # "前功盡棄": "",
    # "持之以恆": "",
}

# 錯字題
def make_wrong_question(idiom: str) -> dict | None:
    pos_data = idioms.get(idiom, {})
    if not pos_data:
        return None

    pos = random.choice(list(pos_data.keys()))
    wrong_char = random.choice(pos_data[pos])

    correct_char = idiom[pos]

    display = list(idiom)
    display[pos] = wrong_char

    return {
        "type": "wrong",
        "idiom": idiom,
        "display": "".join(display),
        "wrong_idx": pos,
        "wrong_char": wrong_char,
        "correct_char": correct_char,
        "hint": "找出錯字並秒準 1.5 秒",
        "explanation": explanations.get(idiom, ""),
    }

# 填空題
def make_fill_question(idiom: str) -> dict | None:
    pos_data = idioms.get(idiom, {})

    if pos_data:
        pos = random.choice(list(pos_data.keys()))
        distractors = pos_data[pos][:]
    else:
        pos = random.randint(0, len(idiom)-1)
        distractors = []

    correct_char = idiom[pos]

    options = [correct_char]

    for c in distractors:
        if c != correct_char and c not in options:
            options.append(c)
        if len(options) == 4:
            break

    while len(options) < 4:
        c = random.choice(options_pool)
        if c not in options:
            options.append(c)

    random.shuffle(options)

    template = list(idiom)
    template[pos] = "＿"

    return {
        "type": "fill",
        "idiom": idiom,
        "template": "".join(template),
        "blank_idx": pos,
        "answer": correct_char,
        "options": options,
        "hint": "秒準正確的字 1.5 秒",
        "explanation": explanations.get(idiom, ""),
    }

# 題目生成
def generate_questions(n=10, wrong_ratio=0.5):
    all_idioms = list(idioms.keys())

    if n > len(all_idioms):
        raise ValueError("成語數量不足，無法產生不重複題目")

    selected = random.sample(all_idioms, n)  # ⭐關鍵

    questions = []

    for idiom in selected:
        if random.random() < wrong_ratio:
            q = make_wrong_question(idiom)
        else:
            q = make_fill_question(idiom)

        if q:
            questions.append(q)

    random.shuffle(questions)
    return questions


# 測試
# if __name__ == "__main__":
#     qs = generate_questions(10)

#     for i, q in enumerate(qs, 1):
#         if q["type"] == "wrong":
#             print(f"[{i}] 找錯字：{q['display']} → 答案：{q['correct_char']}")
#         else:
#             print(f"[{i}] 填空：{q['template']} → {q['options']} 答案：{q['answer']}")