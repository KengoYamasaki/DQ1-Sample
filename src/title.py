"""タイトル画面"""

import pygame
from src.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, KEY_CONFIRM,
)
from src.ui import Font


class TitleState:
    """タイトル画面"""

    def __init__(self, game):
        self.game = game
        self.font_large = Font.get(48)
        self.font_medium = Font.get(28)
        self.font_small = Font.get(22)
        self.blink_timer = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == KEY_CONFIRM:
            from src.field import FieldState
            self.game.change_state(FieldState(self.game))

    def update(self):
        self.blink_timer += 1

    def draw(self, surface):
        surface.fill(BLACK)

        # タイトル
        title = self.font_large.render('ドラゴンクエスト', True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 200))
        surface.blit(title, title_rect)

        # サブタイトル
        sub = self.font_medium.render('〜 ロトの伝説 〜', True, (200, 200, 200))
        sub_rect = sub.get_rect(center=(SCREEN_WIDTH // 2, 270))
        surface.blit(sub, sub_rect)

        # 点滅テキスト
        if (self.blink_timer // 30) % 2 == 0:
            start = self.font_small.render(
                'Zキーを押してはじめる', True, (200, 200, 200))
            start_rect = start.get_rect(center=(SCREEN_WIDTH // 2, 450))
            surface.blit(start, start_rect)

        # 操作説明
        help_texts = [
            '方向キー: いどう',
            'Zキー: けってい / はなす',
            'Xキー: キャンセル',
            'スペース: メニュー',
        ]
        for i, text in enumerate(help_texts):
            help_surf = self.font_small.render(text, True, (150, 150, 150))
            help_rect = help_surf.get_rect(
                center=(SCREEN_WIDTH // 2, 540 + i * 30))
            surface.blit(help_surf, help_rect)
