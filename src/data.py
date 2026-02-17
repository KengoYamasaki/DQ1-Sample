"""ゲームデータ定義 (敵・アイテム・呪文・レベルテーブル・マップ)"""

# =============================================================================
# レベルテーブル (DQ1準拠の簡略版)
# =============================================================================
# (必要EXP, HP, MP, ちから, すばやさ)
LEVEL_TABLE = {
    1:  (0,      15,  0,   4,  4),
    2:  (7,      22,  0,   5,  4),
    3:  (23,     24,  5,   7,  6),
    4:  (47,     31, 16,   7, 8),
    5:  (110,    35, 20,  12, 10),
    6:  (220,    38, 24,  16, 10),
    7:  (450,    40, 26,  18, 17),
    8:  (800,    46, 29,  22, 15),
    9:  (1300,   50, 36,  30, 17),
    10: (2000,   54, 40,  35, 20),
    11: (2900,   62, 50,  38, 22),
    12: (4000,   63, 58,  40, 26),
    13: (5500,   70, 64,  48, 28),
    14: (7500,   78, 70,  52, 32),
    15: (10000,  86, 72,  60, 35),
    16: (13000,  92, 95,  68, 40),
    17: (17000,  100, 100, 72, 43),
    18: (21000,  115, 108, 80, 48),
    19: (25000,  130, 115, 90, 55),
    20: (29000,  138, 128, 96, 58),
    21: (33000,  149, 135, 98, 64),
    22: (37000,  158, 146, 100, 70),
    23: (41000,  165, 153, 105, 78),
    24: (45000,  170, 161, 110, 84),
    25: (49000,  174, 161, 115, 90),
    26: (53000,  180, 168, 119, 90),
    27: (57000,  189, 175, 125, 96),
    28: (61000,  195, 180, 130, 98),
    29: (65000,  200, 190, 135, 105),
    30: (65535,  210, 200, 140, 110),
}

MAX_LEVEL = 30

# =============================================================================
# 呪文定義
# =============================================================================
SPELLS = {
    'ホイミ': {
        'level': 3,
        'mp': 4,
        'type': 'heal',
        'power': 24,    # 回復量ベース
        'desc': 'HPを回復する',
    },
    'ギラ': {
        'level': 4,
        'mp': 2,
        'type': 'attack',
        'power': 10,    # ダメージベース
        'desc': '炎で敵を攻撃する',
    },
    'ラリホー': {
        'level': 7,
        'mp': 2,
        'type': 'status',
        'effect': 'sleep',
        'desc': '敵を眠らせる',
    },
    'レミーラ': {
        'level': 9,
        'mp': 3,
        'type': 'field',
        'effect': 'light',
        'desc': '洞窟を明るくする',
    },
    'マホトーン': {
        'level': 10,
        'mp': 2,
        'type': 'status',
        'effect': 'stopspell',
        'desc': '敵の呪文を封じる',
    },
    'リレミト': {
        'level': 13,
        'mp': 6,
        'type': 'field',
        'effect': 'outside',
        'desc': '洞窟から脱出する',
    },
    'ルーラ': {
        'level': 15,
        'mp': 8,
        'type': 'field',
        'effect': 'return',
        'desc': 'ラダトーム城に戻る',
    },
    'トヘロス': {
        'level': 15,
        'mp': 2,
        'type': 'field',
        'effect': 'repel',
        'desc': '弱い敵を寄せ付けない',
    },
    'ベホイミ': {
        'level': 17,
        'mp': 10,
        'type': 'heal',
        'power': 85,
        'desc': 'HPを大きく回復する',
    },
    'ベギラマ': {
        'level': 19,
        'mp': 5,
        'type': 'attack',
        'power': 58,
        'desc': '強力な炎で敵を攻撃する',
    },
}

# =============================================================================
# アイテム定義
# =============================================================================
ITEMS = {
    'やくそう': {
        'type': 'consumable',
        'effect': 'heal',
        'power': 25,
        'price': 24,
        'desc': 'HPを少し回復する',
    },
    'たいまつ': {
        'type': 'consumable',
        'effect': 'light',
        'power': 0,
        'price': 8,
        'desc': '洞窟を明るくする',
    },
    'キメラのつばさ': {
        'type': 'consumable',
        'effect': 'return',
        'power': 0,
        'price': 70,
        'desc': 'ラダトーム城に戻る',
    },
    'りゅうのうろこ': {
        'type': 'accessory',
        'defense': 5,
        'price': 20,
        'desc': '守備力+5',
    },
    'せんしのゆびわ': {
        'type': 'accessory',
        'attack': 2,
        'price': 15,
        'desc': '攻撃力+2',
    },
    'ようせいのふえ': {
        'type': 'key_item',
        'desc': '不思議な旋律を奏でる笛',
    },
    'ぎんのたてごと': {
        'type': 'key_item',
        'desc': '魔物を呼び寄せる竪琴',
    },
    'おうじょのあい': {
        'type': 'key_item',
        'desc': '姫の愛が宿った宝玉',
    },
    'にじのしずく': {
        'type': 'key_item',
        'desc': '虹の橋をかける',
    },
}

# =============================================================================
# 武器
# =============================================================================
WEAPONS = {
    'なし': {'attack': 0, 'price': 0},
    'たけざお': {'attack': 2, 'price': 10},
    'こんぼう': {'attack': 4, 'price': 60},
    'どうのつるぎ': {'attack': 10, 'price': 180},
    'てつのおの': {'attack': 15, 'price': 560},
    'はがねのつるぎ': {'attack': 20, 'price': 1500},
    'ほのおのつるぎ': {'attack': 28, 'price': 9800},
    'ロトのつるぎ': {'attack': 40, 'price': 0},
}

# =============================================================================
# 鎧
# =============================================================================
ARMORS = {
    'なし': {'defense': 0, 'price': 0},
    'ぬののふく': {'defense': 2, 'price': 20},
    'かわのふく': {'defense': 4, 'price': 70},
    'くさりかたびら': {'defense': 10, 'price': 300},
    'てつのよろい': {'defense': 16, 'price': 800},
    'はがねのよろい': {'defense': 21, 'price': 3000},
    'まほうのよろい': {'defense': 24, 'price': 7700},
    'ロトのよろい': {'defense': 28, 'price': 0},
}

# =============================================================================
# 盾
# =============================================================================
SHIELDS = {
    'なし': {'defense': 0, 'price': 0},
    'かわのたて': {'defense': 2, 'price': 90},
    'てつのたて': {'defense': 10, 'price': 800},
    'みかがみのたて': {'defense': 20, 'price': 14800},
}

# =============================================================================
# 敵キャラ定義
# =============================================================================
ENEMIES = {
    'スライム': {
        'hp': 3, 'attack': 5, 'defense': 3, 'agility': 3,
        'exp': 1, 'gold': 2, 'spells': [],
        'color': (100, 150, 255),
    },
    'ドラキー': {
        'hp': 6, 'attack': 9, 'defense': 6, 'agility': 6,
        'exp': 2, 'gold': 3, 'spells': [],
        'color': (100, 60, 180),
    },
    'ゴースト': {
        'hp': 7, 'attack': 11, 'defense': 8, 'agility': 8,
        'exp': 3, 'gold': 5, 'spells': [],
        'color': (200, 200, 220),
    },
    'まほうつかい': {
        'hp': 13, 'attack': 11, 'defense': 12, 'agility': 10,
        'exp': 4, 'gold': 12, 'spells': ['ギラ'],
        'color': (120, 40, 180),
    },
    'おおさそり': {
        'hp': 20, 'attack': 18, 'defense': 16, 'agility': 10,
        'exp': 6, 'gold': 16, 'spells': [],
        'color': (180, 60, 30),
    },
    'リカント': {
        'hp': 34, 'attack': 40, 'defense': 30, 'agility': 22,
        'exp': 16, 'gold': 40, 'spells': [],
        'color': (100, 70, 40),
    },
    'ゴーレム': {
        'hp': 70, 'attack': 48, 'defense': 40, 'agility': 18,
        'exp': 5, 'gold': 10, 'spells': [],
        'color': (140, 130, 110),
    },
    'しにがみのきし': {
        'hp': 50, 'attack': 52, 'defense': 35, 'agility': 36,
        'exp': 28, 'gold': 70, 'spells': ['ラリホー'],
        'color': (60, 30, 80),
    },
    'ドラゴン': {
        'hp': 65, 'attack': 56, 'defense': 42, 'agility': 30,
        'exp': 35, 'gold': 150, 'spells': [],
        'special': 'fire_breath',
        'color': (200, 50, 20),
    },
    'りゅうおう(人型)': {
        'hp': 100, 'attack': 80, 'defense': 75, 'agility': 50,
        'exp': 0, 'gold': 0, 'spells': ['ベギラマ', 'ラリホー'],
        'color': (100, 0, 150),
    },
    'りゅうおう(竜)': {
        'hp': 130, 'attack': 120, 'defense': 100, 'agility': 60,
        'exp': 0, 'gold': 0, 'spells': [],
        'special': 'fire_breath_strong',
        'color': (180, 0, 60),
    },
}

# エリア別エンカウントテーブル (敵名, 重み)
ENCOUNTER_TABLES = {
    'field_start': [
        ('スライム', 60),
        ('ドラキー', 30),
        ('ゴースト', 10),
    ],
    'field_mid': [
        ('ゴースト', 20),
        ('まほうつかい', 30),
        ('おおさそり', 40),
        ('ドラキー', 10),
    ],
    'field_far': [
        ('リカント', 30),
        ('しにがみのきし', 30),
        ('おおさそり', 20),
        ('まほうつかい', 20),
    ],
    'dungeon': [
        ('ゴースト', 20),
        ('まほうつかい', 30),
        ('おおさそり', 30),
        ('しにがみのきし', 20),
    ],
}

# =============================================================================
# マップデータ
# =============================================================================

# フィールドマップ (40x40)
# G=草, W=水, M=山, F=森, D=砂漠, B=橋, C=城, T=町, V=洞窟, S=沼
FIELD_MAP = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "WWMMMMGGGGGGGGGGGGWWWWWWGGGGGGGGMMMMMMWW",
    "WWMGGGGGFFGGGGGGGGGWWWGGGGFFGGGGGGGGMWWW",
    "WWGGGGGGFFFFFFFGGGGGBGGGFFFFFFGGGGGGGGWW",
    "WWGFFGGGGGFGGGGGGGGGGGGGGFGGGGGFFGGGGGWW",
    "WWGFGGGGGGGGGVGGGGGGGGGGGGGGGGFFFGGGGMWW",
    "WWGGGGGGGGGGGGGGGGGGGGGGGGGGGGFGGGGGMMWW",
    "WWGGGMMMGGGGGGGGGGGGGGGGGGGGGGGGGGGGMWWW",
    "WWGGMMMMGGGGGGGGGGGGGGGGGFFGGGGGGGGGMWWW",
    "WWGGGMMMGGGGGGGGGGGGGGGFFFFFGGGGGGGGGWWW",
    "WWGGGGGGGGGGGGFFFGGGGGGGFFGGGGGGGGGGGGWW",
    "WWGGGGGGGGGGGFFFFFGGGGGGGGGGGGGGGGDDDGWW",
    "WWGGGGGGGGGGGGGFGGGGGGGGGGGGGGGGDDDDGGWW",
    "WWGGGGGGGGGGGGGGGGGGCGGGGGGGGGGDDDDGGGWW",
    "WWGGGGGGSSGGGGGGGGGGGGGGGGGGGGGGDDDGGGWW",
    "WWGGGGGSSSGGGGGGGGGGGGGGGGGGGGGGGDGGGGWW",
    "WWGGGGGGSGGGGGGGGGGGGGGGMMGGGGGGGGGGGGWW",
    "WWGGGGGGGGGGGGGGGGGGGGGMMMGGGGGGGGGGGWWW",
    "WWGGGGGGGGGGGTGGGGGGGGMMMMGGGGGGFFFFFWWW",
    "WWGGGGGGGGGGGGGGGGGGGGGMMMGGGGGFFFFFFWWW",
    "WWGGFFFGGGGGGGGGGGGGGGGGMGGGGGGGGFFFFWWW",
    "WWGGFFFGGGGGGGGGGGGGGGGGGGGGGGGGGGGGWWWW",
    "WWGGFGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGWWW",
    "WWGGGGGGGGGGGGGGMMMGGGGGGGGGGGGGGGGGGWWW",
    "WWGGGGGGGGGGGGMMMMMGGGGGGGGGGGGGGGGGGWWW",
    "WWWGGGGGGGGGGGMMMMGGGGGGFFFGGGGGGGGGGWWW",
    "WWWGGMMMGGGGGGMMMGGGGGFFFFFGGGGGGDDDGWWW",
    "WWWGGMMMGGGGGGGGGGGGGGFFFGGGGGGGDDDDGWWW",
    "WWWGGGMGGGVGGGGGGGGGGGGGGGGGGGGDDDDGGWWW",
    "WWWGGGGGGGGGGGGGGGGGGGGGGGGGGGGGDDGGGWWW",
    "WWWGGGGGGGGGGGGGGGGGGGTGGGGGGGGGGGGGWWWW",
    "WWWWGGGGFFFGGGGGGGGGGGGGGGGGGGGGGGGWWWWW",
    "WWWWGGGFFFFGGGGGGGGGGGGGGGGGGGGGGGGWWWWW",
    "WWWWGGGGFFGGGGGGGGGGGGGGGGGGGMMMGGWWWWWW",
    "WWWWWGGGGGGGGGGGGGGGGGGGGGGMMMMMGGWWWWWW",
    "WWWWWWGGGGGGGGGGGGGGGGGGGGGMMMMGGGWWWWWW",
    "WWWWWWWGGGGGGGGGGGGGGGGGGGGGGGGGGWWWWWWW",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
]

# ラダトーム城 (16x16)
CASTLE_MAP = [
    "################",
    "#..............#",
    "#..O...........#",
    "#..............#",
    "#....######....#",
    "#....#....#....#",
    "#....#....#....#",
    "#....#+...#....#",
    "#.........#....#",
    "#....######....#",
    "#..............#",
    "#..............#",
    "#.....K........#",
    "#..............#",
    "#......++......#",
    "################",
]

# 町 (16x16)
TOWN_MAP = [
    "################",
    "#..............#",
    "#..RR....RR....#",
    "#..RR....RR....#",
    "#..++....++....#",
    "#..............#",
    "#......RR......#",
    "#......RR......#",
    "#......++......#",
    "#..............#",
    "#..............#",
    "#..RR....KKKK..#",
    "#..RR....K..K..#",
    "#..++....+..K..#",
    "#..............#",
    "#####+##########",
]

# 洞窟 (16x16)
DUNGEON_MAP = [
    "################",
    "#..............#",
    "#..<...........#",
    "#..............#",
    "#...########...#",
    "#...#......#...#",
    "#...#..X...#...#",
    "#...#......#...#",
    "#...#+######...#",
    "#..............#",
    "#..............#",
    "#......####....#",
    "#......#..#....#",
    "#......#>.#....#",
    "#......####....#",
    "################",
]

# 洞窟 B2 (16x16)
DUNGEON_B2_MAP = [
    "################",
    "#..............#",
    "#..<...........#",
    "#..............#",
    "#..............#",
    "####.###..#....#",
    "#........##....#",
    "#..####...#....#",
    "#..#..#...#....#",
    "#..#X.#...#....#",
    "#..####...#....#",
    "#.........#....#",
    "#..#############",
    "#..............#",
    "#..............#",
    "################",
]

# マップ情報
MAP_DATA = {
    'field': {
        'data': FIELD_MAP,
        'encounter_table': 'field_start',
        'encounter_rate': 15,  # 1歩あたりの遭遇確率 (%)
    },
    'castle': {
        'data': CASTLE_MAP,
        'encounter_table': None,
        'encounter_rate': 0,
    },
    'town': {
        'data': TOWN_MAP,
        'encounter_table': None,
        'encounter_rate': 0,
    },
    'dungeon_b1': {
        'data': DUNGEON_MAP,
        'encounter_table': 'dungeon',
        'encounter_rate': 20,
    },
    'dungeon_b2': {
        'data': DUNGEON_B2_MAP,
        'encounter_table': 'dungeon',
        'encounter_rate': 25,
    },
}

# ワープポイント定義 (マップ名, x, y) → (マップ名, x, y)
WARPS = {
    # フィールド → 城
    ('field', 19, 14): ('castle', 7, 14),
    # 城 → フィールド
    ('castle', 7, 15): ('field', 19, 15),
    ('castle', 8, 15): ('field', 19, 15),
    # フィールド → 町1 (上の町)
    ('field', 12, 19): ('town', 7, 15),
    # 町1 → フィールド
    ('town', 7, 15): ('field', 12, 20),
    # フィールド → 洞窟1 (上)
    ('field', 11, 6): ('dungeon_b1', 2, 2),
    # 洞窟1 脱出
    ('dungeon_b1', 2, 2): ('field', 11, 7),
    # 洞窟1 B1→B2
    ('dungeon_b1', 9, 13): ('dungeon_b2', 2, 2),
    # 洞窟2 B2→B1
    ('dungeon_b2', 2, 2): ('dungeon_b1', 9, 13),
    # フィールド → 洞窟2 (下)
    ('field', 9, 29): ('dungeon_b1', 2, 2),
    ('dungeon_b1', 2, 1): ('field', 9, 28),
    # フィールド → 町2
    ('field', 20, 31): ('town', 7, 15),
    ('town', 7, 16): ('field', 20, 32),
}

# NPC定義 (マップ名 → NPCリスト)
NPCS = {
    'castle': [
        {'x': 3, 'y': 2, 'name': '王様', 'color': (255, 215, 0),
         'dialogue': [
             'おお ゆうしゃよ！',
             'このくにを おびやかす りゅうおうを\nたおしてくれ！',
             'わしは おまえを しんじておるぞ。',
         ]},
        {'x': 12, 'y': 5, 'name': '兵士', 'color': (150, 150, 180),
         'dialogue': [
             'ここは ラダトームじょうです。',
             'おうさまが おまちですよ。',
         ]},
        {'x': 5, 'y': 12, 'name': '商人', 'color': (200, 150, 50),
         'dialogue': [
             'なにか おいりようですかな？',
         ],
         'shop': {
             'type': 'weapon',
             'items': ['たけざお', 'こんぼう', 'どうのつるぎ'],
         }},
    ],
    'town': [
        {'x': 3, 'y': 5, 'name': '村人', 'color': (100, 180, 100),
         'dialogue': [
             'ようこそ わがまちへ！',
             'ひがしの どうくつには\nきをつけなされ。',
         ]},
        {'x': 10, 'y': 5, 'name': '老人', 'color': (180, 180, 180),
         'dialogue': [
             'むかし ゆうしゃロトが\nこのちを まもったそうじゃ。',
         ]},
        {'x': 12, 'y': 13, 'name': '道具屋', 'color': (200, 150, 50),
         'dialogue': [
             'いらっしゃい！',
         ],
         'shop': {
             'type': 'item',
             'items': ['やくそう', 'たいまつ', 'キメラのつばさ'],
         }},
        {'x': 3, 'y': 14, 'name': '宿屋', 'color': (180, 120, 80),
         'dialogue': [
             'ひとばん 6ゴールドですが\nおとまりですか？',
         ],
         'inn': {'price': 6}},
    ],
}

# 宝箱の中身 (マップ名, x, y) → アイテム名 or ゴールド
CHESTS = {
    ('dungeon_b1', 7, 6): {'type': 'gold', 'amount': 120},
    ('dungeon_b2', 4, 9): {'type': 'item', 'item': 'てつのおの'},
}

# エンカウントエリア判定 (フィールドマップ上の座標範囲でテーブル切替)
def get_encounter_table(map_name, x, y):
    """座標に応じたエンカウントテーブルを返す"""
    if map_name != 'field':
        info = MAP_DATA.get(map_name, {})
        return info.get('encounter_table')

    # フィールドは座標で難易度が変わる
    # 城(19,14)からの距離でエリアを判定
    dist = abs(x - 19) + abs(y - 14)
    if dist < 10:
        return 'field_start'
    elif dist < 20:
        return 'field_mid'
    else:
        return 'field_far'
