"""タイルマップの描画・管理"""

import pygame
from src.config import (
    TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT,
    SCREEN_TILES_X, SCREEN_TILES_Y,
    CHAR_TO_TILE, TILE_COLORS, IMPASSABLE_TILES,
    TILE_WATER, TILE_FOREST, TILE_MOUNTAIN, TILE_CASTLE,
    TILE_TOWN, TILE_CAVE, TILE_STAIRS_DOWN, TILE_STAIRS_UP,
    TILE_CHEST, TILE_THRONE, TILE_BRIDGE, TILE_SWAMP,
    TILE_DOOR, TILE_ROOF, TILE_WALL, TILE_COUNTER,
)


class TileMap:
    """タイルマップ"""

    def __init__(self, map_strings):
        self.height = len(map_strings)
        self.width = len(map_strings[0])
        self.tiles = []
        for row_str in map_strings:
            row = []
            for ch in row_str:
                row.append(CHAR_TO_TILE.get(ch, 0))
            self.tiles.append(row)

        # タイルサーフェスキャッシュ
        self._tile_cache = {}

    def get_tile(self, x, y):
        """指定座標のタイルIDを返す"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return -1  # 範囲外

    def is_passable(self, x, y):
        """通行可能か"""
        tile = self.get_tile(x, y)
        if tile == -1:
            return False
        return tile not in IMPASSABLE_TILES

    def _render_tile(self, tile_id):
        """1タイル分のサーフェスを生成"""
        if tile_id in self._tile_cache:
            return self._tile_cache[tile_id]

        s = pygame.Surface((TILE_SIZE, TILE_SIZE))
        color = TILE_COLORS.get(tile_id, (0, 0, 0))
        s.fill(color)

        # タイルごとにパターンを描く
        if tile_id == TILE_WATER:
            # 波線
            for i in range(3):
                y = 12 + i * 14
                points = [(x, y + (3 if x % 16 < 8 else -3))
                          for x in range(0, TILE_SIZE, 4)]
                if len(points) > 1:
                    pygame.draw.lines(s, (80, 120, 255), False, points, 1)

        elif tile_id == TILE_FOREST:
            # 木のシルエット
            cx, cy = TILE_SIZE // 2, TILE_SIZE // 2
            pygame.draw.circle(s, (0, 140, 0), (cx, cy - 6), 14)
            pygame.draw.circle(s, (0, 120, 0), (cx - 8, cy), 10)
            pygame.draw.circle(s, (0, 120, 0), (cx + 8, cy), 10)
            pygame.draw.rect(s, (100, 70, 30), (cx - 3, cy + 8, 6, 12))

        elif tile_id == TILE_MOUNTAIN:
            # 三角形
            pygame.draw.polygon(s, (180, 130, 70), [
                (TILE_SIZE // 2, 4),
                (4, TILE_SIZE - 4),
                (TILE_SIZE - 4, TILE_SIZE - 4),
            ])
            pygame.draw.polygon(s, (200, 200, 220), [
                (TILE_SIZE // 2, 4),
                (TILE_SIZE // 2 - 6, 14),
                (TILE_SIZE // 2 + 6, 14),
            ])

        elif tile_id == TILE_CASTLE:
            # 城アイコン
            s.fill((34, 139, 34))  # 草地の上
            pygame.draw.rect(s, (192, 192, 192), (8, 12, 32, 28))
            pygame.draw.rect(s, (160, 160, 160), (14, 8, 6, 8))
            pygame.draw.rect(s, (160, 160, 160), (28, 8, 6, 8))
            pygame.draw.rect(s, (100, 70, 30), (18, 28, 12, 12))

        elif tile_id == TILE_TOWN:
            # 町アイコン
            s.fill((34, 139, 34))
            pygame.draw.rect(s, (180, 140, 80), (10, 16, 28, 24))
            pygame.draw.polygon(s, (180, 60, 30), [
                (8, 16), (24, 4), (40, 16),
            ])
            pygame.draw.rect(s, (100, 70, 30), (18, 28, 10, 12))

        elif tile_id == TILE_CAVE:
            # 洞窟入口
            s.fill((34, 139, 34))
            pygame.draw.ellipse(s, (40, 40, 40), (10, 10, 28, 30))
            pygame.draw.ellipse(s, (20, 20, 20), (14, 16, 20, 22))

        elif tile_id == TILE_STAIRS_DOWN:
            # 下り階段
            for i in range(4):
                y = 8 + i * 10
                w = TILE_SIZE - 16 - i * 4
                x = 8 + i * 2
                pygame.draw.rect(s, (80, 60, 30), (x, y, w, 8))

        elif tile_id == TILE_STAIRS_UP:
            # 上り階段
            for i in range(4):
                y = 8 + i * 10
                w = 16 + i * 4
                x = (TILE_SIZE - w) // 2
                pygame.draw.rect(s, (160, 140, 100), (x, y, w, 8))

        elif tile_id == TILE_CHEST:
            # 宝箱
            pygame.draw.rect(s, (160, 120, 30), (10, 14, 28, 22))
            pygame.draw.rect(s, (200, 160, 40), (12, 16, 24, 8))
            pygame.draw.rect(s, (140, 100, 20), (12, 26, 24, 8))
            pygame.draw.circle(s, (255, 255, 200), (24, 24), 3)

        elif tile_id == TILE_THRONE:
            # 玉座
            pygame.draw.rect(s, (200, 180, 60), (12, 8, 24, 36))
            pygame.draw.rect(s, (180, 50, 50), (8, 4, 32, 8))
            pygame.draw.rect(s, (180, 50, 50), (8, 4, 6, 24))
            pygame.draw.rect(s, (180, 50, 50), (34, 4, 6, 24))

        elif tile_id == TILE_BRIDGE:
            # 橋
            s.fill((30, 60, 200))  # 水の上
            pygame.draw.rect(s, (160, 120, 60), (4, 0, TILE_SIZE - 8, TILE_SIZE))
            for i in range(0, TILE_SIZE, 12):
                pygame.draw.line(s, (120, 80, 30), (4, i), (TILE_SIZE - 4, i), 1)

        elif tile_id == TILE_SWAMP:
            # 沼
            pygame.draw.circle(s, (60, 80, 40), (16, 20), 12)
            pygame.draw.circle(s, (60, 80, 40), (32, 28), 10)
            pygame.draw.circle(s, (70, 90, 50), (24, 32), 8)

        elif tile_id == TILE_DOOR:
            # ドア
            pygame.draw.rect(s, (160, 110, 50), (8, 4, 32, 40))
            pygame.draw.rect(s, (120, 80, 30), (10, 6, 28, 36))
            pygame.draw.circle(s, (200, 180, 80), (32, 24), 3)

        elif tile_id == TILE_WALL:
            # 壁 (レンガ風)
            for row in range(0, TILE_SIZE, 12):
                offset = 0 if (row // 12) % 2 == 0 else 16
                for col in range(-16 + offset, TILE_SIZE, 32):
                    pygame.draw.rect(s, (100, 100, 100),
                                     (col, row, 30, 10))
                    pygame.draw.rect(s, (60, 60, 60),
                                     (col, row, 30, 10), 1)

        elif tile_id == TILE_ROOF:
            # 屋根
            pygame.draw.polygon(s, (200, 80, 30), [
                (0, TILE_SIZE), (TILE_SIZE // 2, 0), (TILE_SIZE, TILE_SIZE),
            ])
            pygame.draw.polygon(s, (160, 60, 20), [
                (0, TILE_SIZE), (TILE_SIZE // 2, 0), (TILE_SIZE, TILE_SIZE),
            ], 2)

        self._tile_cache[tile_id] = s
        return s

    def draw(self, surface, camera_x, camera_y, opened_chests=None):
        """マップを描画 (camera_x/yはプレイヤーのピクセル座標)"""
        # カメラをプレイヤー中心に
        offset_x = camera_x - SCREEN_WIDTH // 2
        offset_y = camera_y - SCREEN_HEIGHT // 2

        start_tx = max(0, int(offset_x // TILE_SIZE) - 1)
        start_ty = max(0, int(offset_y // TILE_SIZE) - 1)
        end_tx = min(self.width, start_tx + SCREEN_TILES_X + 3)
        end_ty = min(self.height, start_ty + SCREEN_TILES_Y + 3)

        for ty in range(start_ty, end_ty):
            for tx in range(start_tx, end_tx):
                tile_id = self.tiles[ty][tx]
                screen_x = tx * TILE_SIZE - offset_x
                screen_y = ty * TILE_SIZE - offset_y

                # 画面外スキップ
                if (screen_x + TILE_SIZE < 0 or screen_x > SCREEN_WIDTH or
                        screen_y + TILE_SIZE < 0 or screen_y > SCREEN_HEIGHT):
                    continue

                # 開封済み宝箱は床タイルで描画
                if tile_id == TILE_CHEST and opened_chests and (tx, ty) in opened_chests:
                    tile_surf = self._render_tile(6)  # TILE_FLOOR
                else:
                    tile_surf = self._render_tile(tile_id)

                surface.blit(tile_surf, (int(screen_x), int(screen_y)))


def draw_player(surface, screen_x, screen_y, direction):
    """プレイヤーキャラを描画"""
    cx = int(screen_x + TILE_SIZE // 2)
    cy = int(screen_y + TILE_SIZE // 2)

    # 体
    pygame.draw.rect(surface, (60, 60, 200),
                     (cx - 10, cy - 8, 20, 24))
    # 頭
    pygame.draw.circle(surface, (240, 200, 160), (cx, cy - 14), 10)
    # 髪
    pygame.draw.arc(surface, (100, 60, 20),
                    (cx - 10, cy - 26, 20, 16), 0, 3.14, 3)
    # 向き表示 (目)
    dx, dy = direction
    eye_x = cx + dx * 4
    eye_y = cy - 14 + dy * 2
    pygame.draw.circle(surface, (20, 20, 20), (eye_x - 3, eye_y), 2)
    pygame.draw.circle(surface, (20, 20, 20), (eye_x + 3, eye_y), 2)
    # 足
    pygame.draw.rect(surface, (150, 100, 50),
                     (cx - 8, cy + 16, 6, 6))
    pygame.draw.rect(surface, (150, 100, 50),
                     (cx + 2, cy + 16, 6, 6))


def draw_npc(surface, screen_x, screen_y, color):
    """NPCを描画"""
    cx = int(screen_x + TILE_SIZE // 2)
    cy = int(screen_y + TILE_SIZE // 2)

    # 体
    pygame.draw.rect(surface, color,
                     (cx - 10, cy - 8, 20, 24))
    # 頭
    pygame.draw.circle(surface, (240, 210, 170), (cx, cy - 14), 10)
    # 目
    pygame.draw.circle(surface, (20, 20, 20), (cx - 3, cy - 14), 2)
    pygame.draw.circle(surface, (20, 20, 20), (cx + 3, cy - 14), 2)
