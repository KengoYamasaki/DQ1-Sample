"""メインゲームクラス"""

import pygame
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from src.player import Player
from src.title import TitleState


class Game:
    """ゲーム全体の管理"""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('ドラゴンクエスト I')
        self.clock = pygame.time.Clock()
        self.running = True

        # プレイヤー
        self.player = Player()

        # ステートスタック
        self.state_stack = []
        self.push_state(TitleState(self))

    @property
    def current_state(self):
        if self.state_stack:
            return self.state_stack[-1]
        return None

    def push_state(self, state):
        """ステートをスタックに追加"""
        self.state_stack.append(state)

    def pop_state(self):
        """現在のステートを除去"""
        if self.state_stack:
            self.state_stack.pop()

    def change_state(self, state):
        """現在のステートを入れ替え"""
        if self.state_stack:
            self.state_stack.pop()
        self.state_stack.append(state)

    def run(self):
        """メインゲームループ"""
        while self.running:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(FPS)

        pygame.quit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
                return
            if self.current_state:
                self.current_state.handle_event(event)

    def _update(self):
        if self.current_state:
            self.current_state.update()

    def _draw(self):
        if self.current_state:
            self.current_state.draw(self.screen)
        pygame.display.flip()
