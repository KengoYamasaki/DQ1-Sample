#!/usr/bin/env python3
"""ドラゴンクエスト I - メインエントリポイント"""

from src.game import Game


def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
