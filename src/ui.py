"""DQスタイルのUI (ウィンドウ・メニュー・テキスト表示)"""

import pygame
from src.config import (
    BLACK, WHITE, WINDOW_BG, WINDOW_BORDER,
    TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT,
    KEY_CONFIRM, KEY_CANCEL, KEY_UP, KEY_DOWN,
)


def load_font(size=24):
    """日本語フォントをロード (フォールバック付き)"""
    candidates = [
        'ipagothic', 'ipaexgothic', 'notosanscjkjp',
        'notosansjp', 'vlgothic', 'taaboregothic',
        'sazanami gothic', 'mplus-1p', 'mplus1p',
    ]
    for name in candidates:
        path = pygame.font.match_font(name)
        if path:
            return pygame.font.Font(path, size)
    # フォールバック: デフォルトフォント
    return pygame.font.Font(None, size)


class Font:
    """フォントキャッシュ"""
    _cache = {}

    @classmethod
    def get(cls, size=24):
        if size not in cls._cache:
            cls._cache[size] = load_font(size)
        return cls._cache[size]


class Window:
    """DQスタイルのウィンドウ (黒背景・白枠)"""

    BORDER_WIDTH = 3
    PADDING = 12

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, surface):
        """ウィンドウ枠を描画"""
        # 黒背景
        pygame.draw.rect(surface, WINDOW_BG, self.rect)
        # 白枠 (二重線)
        pygame.draw.rect(surface, WINDOW_BORDER, self.rect, self.BORDER_WIDTH)
        inner = self.rect.inflate(-8, -8)
        pygame.draw.rect(surface, WINDOW_BORDER, inner, 1)

    @property
    def content_rect(self):
        """テキスト描画可能領域"""
        return self.rect.inflate(
            -(self.BORDER_WIDTH + self.PADDING) * 2,
            -(self.BORDER_WIDTH + self.PADDING) * 2,
        )


class TextRenderer:
    """文字送り対応のテキスト描画"""

    def __init__(self, text, window, font_size=24, speed=2):
        self.full_text = text
        self.window = window
        self.font = Font.get(font_size)
        self.font_size = font_size
        self.speed = speed       # 何フレームに1文字表示するか
        self.char_count = 0
        self.frame_count = 0
        self.finished = False
        self.line_height = font_size + 4

    def update(self):
        """1フレーム進める"""
        if self.finished:
            return
        self.frame_count += 1
        if self.frame_count >= self.speed:
            self.frame_count = 0
            self.char_count += 1
            if self.char_count >= len(self.full_text):
                self.char_count = len(self.full_text)
                self.finished = True

    def skip(self):
        """全文を即座に表示"""
        self.char_count = len(self.full_text)
        self.finished = True

    def draw(self, surface):
        """テキストを描画"""
        self.window.draw(surface)
        content = self.window.content_rect
        visible_text = self.full_text[:self.char_count]

        x = content.x
        y = content.y
        for line in visible_text.split('\n'):
            if y + self.line_height > content.bottom:
                break
            if line:
                text_surface = self.font.render(line, True, WHITE)
                surface.blit(text_surface, (x, y))
            y += self.line_height

        # カーソル点滅 (文字送り完了時)
        if self.finished and (pygame.time.get_ticks() // 400) % 2 == 0:
            cursor_y = y - self.line_height + 4
            if cursor_y + 16 <= content.bottom:
                pygame.draw.polygon(surface, WHITE, [
                    (content.right - 16, content.bottom - 12),
                    (content.right - 8, content.bottom - 4),
                    (content.right, content.bottom - 12),
                ])


class Menu:
    """選択メニュー"""

    def __init__(self, x, y, width, items, font_size=24, columns=1):
        self.items = items
        self.font = Font.get(font_size)
        self.font_size = font_size
        self.cursor = 0
        self.columns = columns

        line_height = font_size + 8
        rows = (len(items) + columns - 1) // columns
        height = rows * line_height + Window.PADDING * 2 + Window.BORDER_WIDTH * 2 + 8

        self.window = Window(x, y, width, height)
        self.line_height = line_height

    def handle_event(self, event):
        """キー入力処理。選択されたらインデックスを、キャンセルなら-1を返す"""
        if event.type != pygame.KEYDOWN:
            return None

        if event.key == KEY_UP:
            self.cursor = (self.cursor - self.columns) % len(self.items)
        elif event.key == KEY_DOWN:
            self.cursor = (self.cursor + self.columns) % len(self.items)
        elif event.key == pygame.K_LEFT and self.columns > 1:
            if self.cursor % self.columns > 0:
                self.cursor -= 1
        elif event.key == pygame.K_RIGHT and self.columns > 1:
            if self.cursor % self.columns < self.columns - 1 and self.cursor + 1 < len(self.items):
                self.cursor += 1
        elif event.key == KEY_CONFIRM:
            return self.cursor
        elif event.key == KEY_CANCEL:
            return -1

        return None

    def draw(self, surface):
        """メニューを描画"""
        self.window.draw(surface)
        content = self.window.content_rect

        col_width = content.width // self.columns

        for i, item in enumerate(self.items):
            col = i % self.columns
            row = i // self.columns
            x = content.x + col * col_width + 24
            y = content.y + row * self.line_height

            # カーソル
            if i == self.cursor:
                cursor_x = x - 20
                cursor_y = y + self.font_size // 2
                pygame.draw.polygon(surface, WHITE, [
                    (cursor_x, cursor_y - 6),
                    (cursor_x + 10, cursor_y),
                    (cursor_x, cursor_y + 6),
                ])

            text_surface = self.font.render(str(item), True, WHITE)
            surface.blit(text_surface, (x, y))


class StatusWindow:
    """ステータス表示ウィンドウ"""

    def __init__(self, player):
        self.player = player
        self.window = Window(0, 0, 200, 80)
        self.font = Font.get(20)

    def draw(self, surface):
        """HP/MPを表示"""
        self.window.draw(surface)
        content = self.window.content_rect

        hp_text = f'HP: {self.player.hp:>3}/{self.player.max_hp:>3}'
        mp_text = f'MP: {self.player.mp:>3}/{self.player.max_mp:>3}'

        hp_surface = self.font.render(hp_text, True, WHITE)
        mp_surface = self.font.render(mp_text, True, WHITE)

        surface.blit(hp_surface, (content.x, content.y))
        surface.blit(mp_surface, (content.x, content.y + 24))


class MessageWindow:
    """画面下部のメッセージウィンドウ"""

    def __init__(self, font_size=24):
        self.font_size = font_size
        self.window = Window(
            16, SCREEN_HEIGHT - 160,
            SCREEN_WIDTH - 32, 144,
        )
        self.messages = []       # メッセージキュー
        self.current = None      # 現在のTextRenderer
        self.active = False

    def show(self, text):
        """メッセージを表示キューに追加"""
        self.messages.append(text)
        if not self.active:
            self._next()

    def show_many(self, texts):
        """複数メッセージを追加"""
        for t in texts:
            self.messages.append(t)
        if not self.active:
            self._next()

    def _next(self):
        """次のメッセージを表示開始"""
        if self.messages:
            text = self.messages.pop(0)
            self.current = TextRenderer(
                text, self.window, self.font_size, speed=1,
            )
            self.active = True
        else:
            self.current = None
            self.active = False

    def handle_event(self, event):
        """キー入力。全メッセージ表示完了でTrue"""
        if not self.active:
            return True

        if event.type == pygame.KEYDOWN and event.key == KEY_CONFIRM:
            if self.current and not self.current.finished:
                self.current.skip()
            else:
                self._next()
                if not self.active:
                    return True
        return False

    def update(self):
        if self.current:
            self.current.update()

    def draw(self, surface):
        if self.current:
            self.current.draw(surface)

    def clear(self):
        self.messages.clear()
        self.current = None
        self.active = False
