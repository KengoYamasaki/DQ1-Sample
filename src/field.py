"""フィールド (マップ移動) ステート"""

import random
import pygame
from src.config import (
    TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT,
    KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT,
    KEY_CONFIRM, KEY_MENU, KEY_CANCEL,
    DIR_UP, DIR_DOWN, DIR_LEFT, DIR_RIGHT,
    MOVE_FRAMES, ENCOUNTER_TILES, TILE_CHEST,
    TILE_STAIRS_DOWN, TILE_STAIRS_UP,
)
from src.data import (
    MAP_DATA, WARPS, NPCS, ENCOUNTER_TABLES, CHESTS,
    get_encounter_table,
)
from src.tilemap import TileMap, draw_player, draw_npc
from src.ui import StatusWindow, MessageWindow, Menu


class FieldState:
    """マップ上を歩くステート"""

    def __init__(self, game):
        self.game = game
        self.player = game.player

        # マップ読み込み
        self.load_map(self.player.map_name)

        # 移動アニメーション
        self.moving = False
        self.move_dx = 0
        self.move_dy = 0
        self.move_progress = 0
        self.pixel_offset_x = 0.0
        self.pixel_offset_y = 0.0

        # UI
        self.status_window = StatusWindow(self.player)
        self.message_window = MessageWindow()
        self.showing_message = False

        # NPC会話 / ショップ / 宿屋
        self.talking_npc = None
        self.shop_menu = None
        self.shop_npc = None
        self.inn_npc = None
        self.inn_confirm = None

        # コマンドメニュー
        self.command_menu = None

    def load_map(self, map_name):
        """マップを切り替え"""
        self.player.map_name = map_name
        map_info = MAP_DATA[map_name]
        self.tilemap = TileMap(map_info['data'])
        self.encounter_rate = map_info['encounter_rate']
        self.npcs = NPCS.get(map_name, [])

    def handle_event(self, event):
        # メッセージ表示中
        if self.showing_message:
            done = self.message_window.handle_event(event)
            if done:
                self.showing_message = False
                # 宿屋確認待ち
                if self.inn_npc and self.inn_confirm is None:
                    self.inn_confirm = Menu(
                        SCREEN_WIDTH // 2 - 80,
                        SCREEN_HEIGHT // 2 - 60,
                        160, ['はい', 'いいえ'],
                    )
                # ショップ処理
                elif self.shop_npc and self.shop_menu is None:
                    npc = self.shop_npc
                    shop = npc.get('shop', {})
                    items = shop.get('items', [])
                    self.shop_menu = Menu(
                        SCREEN_WIDTH // 2 - 120,
                        SCREEN_HEIGHT // 2 - 80,
                        240, items + ['やめる'],
                    )
            return

        # 宿屋確認
        if self.inn_confirm:
            result = self.inn_confirm.handle_event(event)
            if result is not None:
                if result == 0:  # はい
                    inn = self.inn_npc.get('inn', {})
                    price = inn.get('price', 6)
                    if self.player.gold >= price:
                        self.player.gold -= price
                        self.player.heal_at_inn()
                        self.message_window.show('おやすみなさい…\nHPとMPが かいふくした！')
                        self.showing_message = True
                    else:
                        self.message_window.show('おかねが たりません。')
                        self.showing_message = True
                self.inn_confirm = None
                self.inn_npc = None
                return
            return

        # ショップメニュー
        if self.shop_menu:
            result = self.shop_menu.handle_event(event)
            if result is not None:
                if result == -1 or result == len(self.shop_menu.items) - 1:
                    self.shop_menu = None
                    self.shop_npc = None
                else:
                    self._buy_item(result)
                return
            return

        # コマンドメニュー
        if self.command_menu:
            result = self.command_menu.handle_event(event)
            if result is not None:
                self.command_menu = None
                if result >= 0:
                    self._handle_command(result)
            return

        if event.type != pygame.KEYDOWN:
            return

        # 移動中は入力無視
        if self.moving:
            return

        # メニュー表示
        if event.key == KEY_MENU:
            self.command_menu = Menu(
                16, 16, 200,
                ['つよさ', 'じゅもん', 'どうぐ', 'とびら', 'しらべる'],
            )
            return

        # はなす (Zキー)
        if event.key == KEY_CONFIRM:
            self._talk()
            return

        # 方向キーで移動
        direction_map = {
            KEY_UP: DIR_UP,
            KEY_DOWN: DIR_DOWN,
            KEY_LEFT: DIR_LEFT,
            KEY_RIGHT: DIR_RIGHT,
        }
        if event.key in direction_map:
            dx, dy = direction_map[event.key]
            self.player.direction = (dx, dy)
            target_x = self.player.tile_x + dx
            target_y = self.player.tile_y + dy
            if self.tilemap.is_passable(target_x, target_y):
                self._start_move(dx, dy)
            # 通行不可でも向きは変わる

    def _start_move(self, dx, dy):
        """移動開始"""
        self.moving = True
        self.move_dx = dx
        self.move_dy = dy
        self.move_progress = 0
        self.pixel_offset_x = 0.0
        self.pixel_offset_y = 0.0

    def _finish_move(self):
        """移動完了時の処理"""
        self.player.tile_x += self.move_dx
        self.player.tile_y += self.move_dy
        self.moving = False
        self.pixel_offset_x = 0.0
        self.pixel_offset_y = 0.0

        x = self.player.tile_x
        y = self.player.tile_y
        map_name = self.player.map_name

        # ワープチェック
        warp_key = (map_name, x, y)
        if warp_key in WARPS:
            dest_map, dest_x, dest_y = WARPS[warp_key]
            self.player.tile_x = dest_x
            self.player.tile_y = dest_y
            self.load_map(dest_map)
            return

        # 宝箱チェック
        tile = self.tilemap.get_tile(x, y)
        if tile == TILE_CHEST:
            chest_key = (map_name, x, y)
            if chest_key not in self.player.opened_chests:
                self.player.opened_chests.add(chest_key)
                chest_data = CHESTS.get(chest_key)
                if chest_data:
                    if chest_data['type'] == 'gold':
                        self.player.gold += chest_data['amount']
                        self.message_window.show(
                            f"たからばこから\n{chest_data['amount']}ゴールド みつけた！")
                    elif chest_data['type'] == 'item':
                        item = chest_data['item']
                        if self.player.add_item(item):
                            self.message_window.show(
                                f'たからばこから\n{item}を みつけた！')
                        else:
                            self.message_window.show(
                                'しかし もちものが いっぱいだ！')
                else:
                    self.message_window.show('たからばこは からだった。')
                self.showing_message = True
                return

        # エンカウント判定
        if self.encounter_rate > 0 and tile in ENCOUNTER_TILES:
            if random.randint(1, 100) <= self.encounter_rate:
                table_name = get_encounter_table(map_name, x, y)
                if table_name and table_name in ENCOUNTER_TABLES:
                    self._start_battle(table_name)

    def _start_battle(self, table_name):
        """戦闘開始"""
        from src.battle import BattleState
        table = ENCOUNTER_TABLES[table_name]
        # 重み付きランダム選択
        total = sum(w for _, w in table)
        r = random.randint(1, total)
        cumulative = 0
        enemy_name = table[0][0]
        for name, weight in table:
            cumulative += weight
            if r <= cumulative:
                enemy_name = name
                break

        battle = BattleState(self.game, enemy_name, self)
        self.game.push_state(battle)

    def _talk(self):
        """目の前のNPCに話しかける"""
        dx, dy = self.player.direction
        target_x = self.player.tile_x + dx
        target_y = self.player.tile_y + dy

        for npc in self.npcs:
            if npc['x'] == target_x and npc['y'] == target_y:
                self.talking_npc = npc
                self.message_window.show_many(npc['dialogue'])
                self.showing_message = True

                # ショップ / 宿屋の判定
                if 'shop' in npc:
                    self.shop_npc = npc
                elif 'inn' in npc:
                    self.inn_npc = npc
                return

        self.message_window.show('だれも いない。')
        self.showing_message = True

    def _handle_command(self, index):
        """コマンドメニュー選択処理"""
        commands = ['つよさ', 'じゅもん', 'どうぐ', 'とびら', 'しらべる']
        cmd = commands[index]

        if cmd == 'つよさ':
            p = self.player
            text = (
                f'なまえ: {p.name}\n'
                f'レベル: {p.level}\n'
                f'HP: {p.hp}/{p.max_hp}  MP: {p.mp}/{p.max_mp}\n'
                f'こうげき力: {p.attack_power}  しゅび力: {p.defense_power}\n'
                f'EXP: {p.exp}  G: {p.gold}'
            )
            self.message_window.show(text)
            self.showing_message = True

        elif cmd == 'じゅもん':
            spells = self.player.known_spells
            if not spells:
                self.message_window.show('じゅもんを おぼえていない。')
                self.showing_message = True
            else:
                # フィールド呪文
                for spell_name in spells:
                    from src.data import SPELLS
                    spell = SPELLS[spell_name]
                    if spell['type'] == 'heal':
                        if self.player.use_mp(spell['mp']):
                            heal = min(spell['power'], self.player.max_hp - self.player.hp)
                            self.player.heal(spell['power'])
                            self.message_window.show(
                                f'{spell_name}！\nHPが {heal} かいふくした！')
                        else:
                            self.message_window.show('MPが たりない！')
                        self.showing_message = True
                        return
                self.message_window.show(
                    'つかえる じゅもん:\n' + '、'.join(spells))
                self.showing_message = True

        elif cmd == 'どうぐ':
            if not self.player.items:
                self.message_window.show('もちものが ない。')
                self.showing_message = True
            else:
                text = 'もちもの:\n' + '、'.join(self.player.items)
                self.message_window.show(text)
                self.showing_message = True

        elif cmd == 'とびら':
            self.message_window.show('とびらは ない。')
            self.showing_message = True

        elif cmd == 'しらべる':
            self.message_window.show(
                f'{self.player.name}は あしもとを しらべた。\n'
                'しかし なにも みつからなかった。')
            self.showing_message = True

    def _buy_item(self, index):
        """ショップで買い物"""
        shop = self.shop_npc.get('shop', {})
        items = shop.get('items', [])
        item_name = items[index]

        from src.data import ITEMS, WEAPONS, ARMORS, SHIELDS
        # 価格を取得
        price = 0
        for catalog in [ITEMS, WEAPONS, ARMORS, SHIELDS]:
            if item_name in catalog:
                price = catalog[item_name].get('price', 0)
                break

        if self.player.gold < price:
            self.message_window.show('おかねが たりません。')
            self.showing_message = True
            return

        if not self.player.add_item(item_name):
            self.message_window.show('もちものが いっぱいです。')
            self.showing_message = True
            return

        self.player.gold -= price
        self.message_window.show(f'{item_name}を かった！')
        self.showing_message = True

    def update(self):
        # 移動アニメーション
        if self.moving:
            self.move_progress += 1
            step = TILE_SIZE / MOVE_FRAMES
            self.pixel_offset_x = self.move_dx * self.move_progress * step
            self.pixel_offset_y = self.move_dy * self.move_progress * step
            if self.move_progress >= MOVE_FRAMES:
                self._finish_move()

        # キー押しっぱなしで連続移動
        if not self.moving and not self.showing_message and not self.command_menu:
            keys = pygame.key.get_pressed()
            direction_map = {
                KEY_UP: DIR_UP,
                KEY_DOWN: DIR_DOWN,
                KEY_LEFT: DIR_LEFT,
                KEY_RIGHT: DIR_RIGHT,
            }
            for key, (dx, dy) in direction_map.items():
                if keys[key]:
                    self.player.direction = (dx, dy)
                    target_x = self.player.tile_x + dx
                    target_y = self.player.tile_y + dy
                    if self.tilemap.is_passable(target_x, target_y):
                        self._start_move(dx, dy)
                    break

        # メッセージ更新
        self.message_window.update()

    def draw(self, surface):
        # カメラ位置 (プレイヤー中心)
        cam_x = self.player.tile_x * TILE_SIZE + TILE_SIZE // 2 + self.pixel_offset_x
        cam_y = self.player.tile_y * TILE_SIZE + TILE_SIZE // 2 + self.pixel_offset_y

        # 画面外を黒で塗る
        surface.fill((0, 0, 0))

        # 開封済み宝箱を現在のマップ用に変換
        opened = set()
        for (m, x, y) in self.player.opened_chests:
            if m == self.player.map_name:
                opened.add((x, y))

        # マップ描画
        self.tilemap.draw(surface, cam_x, cam_y, opened)

        # NPC描画
        offset_x = cam_x - SCREEN_WIDTH // 2
        offset_y = cam_y - SCREEN_HEIGHT // 2
        for npc in self.npcs:
            nx = npc['x'] * TILE_SIZE - offset_x
            ny = npc['y'] * TILE_SIZE - offset_y
            if -TILE_SIZE < nx < SCREEN_WIDTH + TILE_SIZE and \
               -TILE_SIZE < ny < SCREEN_HEIGHT + TILE_SIZE:
                draw_npc(surface, nx, ny, npc.get('color', (200, 200, 200)))

        # プレイヤー描画 (画面中心)
        player_screen_x = SCREEN_WIDTH // 2 - TILE_SIZE // 2
        player_screen_y = SCREEN_HEIGHT // 2 - TILE_SIZE // 2
        draw_player(surface, player_screen_x, player_screen_y,
                    self.player.direction)

        # ステータスウィンドウ
        self.status_window.draw(surface)

        # メッセージウィンドウ
        if self.showing_message:
            self.message_window.draw(surface)

        # 宿屋確認メニュー
        if self.inn_confirm:
            self.inn_confirm.draw(surface)

        # ショップメニュー
        if self.shop_menu:
            self.shop_menu.draw(surface)

        # コマンドメニュー
        if self.command_menu:
            self.command_menu.draw(surface)
