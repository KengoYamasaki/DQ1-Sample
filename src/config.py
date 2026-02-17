"""ゲーム設定・定数"""

import pygame

# 画面設定
TILE_SIZE = 48
SCREEN_TILES_X = 16
SCREEN_TILES_Y = 15
SCREEN_WIDTH = TILE_SIZE * SCREEN_TILES_X   # 768
SCREEN_HEIGHT = TILE_SIZE * SCREEN_TILES_Y  # 720
FPS = 60

# プレイヤー移動速度 (1タイル移動にかかるフレーム数)
MOVE_FRAMES = 8

# カラーパレット (FC風)
BLACK = (0, 0, 0)
WHITE = (252, 252, 252)
WINDOW_BORDER = (252, 252, 252)
WINDOW_BG = (0, 0, 0)

# タイルタイプ
TILE_GRASS = 0
TILE_WATER = 1
TILE_MOUNTAIN = 2
TILE_FOREST = 3
TILE_DESERT = 4
TILE_BRIDGE = 5
TILE_FLOOR = 6
TILE_WALL = 7
TILE_DOOR = 8
TILE_STAIRS_DOWN = 9
TILE_STAIRS_UP = 10
TILE_CASTLE = 11
TILE_TOWN = 12
TILE_CAVE = 13
TILE_SWAMP = 14
TILE_ROOF = 15
TILE_COUNTER = 16
TILE_CHEST = 17
TILE_THRONE = 18

# マップ文字 → タイルID変換
CHAR_TO_TILE = {
    'G': TILE_GRASS,
    'W': TILE_WATER,
    'M': TILE_MOUNTAIN,
    'F': TILE_FOREST,
    'D': TILE_DESERT,
    'B': TILE_BRIDGE,
    '.': TILE_FLOOR,
    '#': TILE_WALL,
    '+': TILE_DOOR,
    '>': TILE_STAIRS_DOWN,
    '<': TILE_STAIRS_UP,
    'C': TILE_CASTLE,
    'T': TILE_TOWN,
    'V': TILE_CAVE,
    'S': TILE_SWAMP,
    'R': TILE_ROOF,
    'K': TILE_COUNTER,
    'X': TILE_CHEST,
    'O': TILE_THRONE,
}

# タイルカラー定義
TILE_COLORS = {
    TILE_GRASS:       (34, 139, 34),
    TILE_WATER:       (30, 60, 200),
    TILE_MOUNTAIN:    (139, 90, 43),
    TILE_FOREST:      (0, 100, 0),
    TILE_DESERT:      (210, 180, 100),
    TILE_BRIDGE:      (160, 120, 60),
    TILE_FLOOR:       (180, 160, 120),
    TILE_WALL:        (80, 80, 80),
    TILE_DOOR:        (140, 100, 40),
    TILE_STAIRS_DOWN: (120, 80, 40),
    TILE_STAIRS_UP:   (120, 80, 40),
    TILE_CASTLE:      (192, 192, 192),
    TILE_TOWN:        (180, 140, 80),
    TILE_CAVE:        (60, 60, 60),
    TILE_SWAMP:       (80, 100, 60),
    TILE_ROOF:        (180, 60, 30),
    TILE_COUNTER:     (140, 100, 60),
    TILE_CHEST:       (200, 160, 40),
    TILE_THRONE:      (200, 180, 60),
}

# 通行不可タイル
IMPASSABLE_TILES = {TILE_WATER, TILE_MOUNTAIN, TILE_WALL, TILE_ROOF, TILE_COUNTER}

# エンカウントが発生するタイル
ENCOUNTER_TILES = {TILE_GRASS, TILE_FOREST, TILE_DESERT, TILE_SWAMP, TILE_BRIDGE}

# キー設定
KEY_UP = pygame.K_UP
KEY_DOWN = pygame.K_DOWN
KEY_LEFT = pygame.K_LEFT
KEY_RIGHT = pygame.K_RIGHT
KEY_CONFIRM = pygame.K_z      # 決定
KEY_CANCEL = pygame.K_x       # キャンセル
KEY_MENU = pygame.K_SPACE     # メニュー

# 方向
DIR_UP = (0, -1)
DIR_DOWN = (0, 1)
DIR_LEFT = (-1, 0)
DIR_RIGHT = (1, 0)
