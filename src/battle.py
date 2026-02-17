"""戦闘システム"""

import random
import math
import pygame
from src.config import (
    TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT,
    BLACK, WHITE, KEY_CONFIRM,
)
from src.data import ENEMIES, SPELLS
from src.ui import Window, Menu, MessageWindow, Font


class BattleState:
    """1対1ターン制バトル"""

    # 戦闘フェーズ
    PHASE_APPEAR = 'appear'         # 敵出現メッセージ
    PHASE_COMMAND = 'command'        # コマンド選択
    PHASE_SPELL_SELECT = 'spell'    # 呪文選択
    PHASE_ITEM_SELECT = 'item'      # 道具選択
    PHASE_EXECUTE = 'execute'       # ターン実行中 (メッセージ表示)
    PHASE_RESULT = 'result'         # 勝利/敗北
    PHASE_LEVEL_UP = 'levelup'      # レベルアップ表示
    PHASE_END = 'end'               # 戦闘終了

    def __init__(self, game, enemy_name, field_state):
        self.game = game
        self.player = game.player
        self.field_state = field_state

        # 敵データ
        self.enemy_name = enemy_name
        enemy_data = ENEMIES[enemy_name]
        self.enemy_hp = enemy_data['hp']
        self.enemy_max_hp = enemy_data['hp']
        self.enemy_attack = enemy_data['attack']
        self.enemy_defense = enemy_data['defense']
        self.enemy_agility = enemy_data['agility']
        self.enemy_exp = enemy_data['exp']
        self.enemy_gold = enemy_data['gold']
        self.enemy_spells = enemy_data.get('spells', [])
        self.enemy_special = enemy_data.get('special', None)
        self.enemy_color = enemy_data.get('color', (200, 200, 200))
        self.enemy_asleep = False

        # UI
        self.message_window = MessageWindow(font_size=22)
        self.command_menu = None
        self.spell_menu = None
        self.item_menu = None
        self.font = Font.get(22)
        self.font_large = Font.get(28)

        # フェーズ
        self.phase = self.PHASE_APPEAR
        self.message_window.show(f'{enemy_name}が あらわれた！')
        self.showing_message = True
        self.battle_over = False
        self.player_won = False
        self.level_ups = []
        self.ran_away = False

    def handle_event(self, event):
        if self.phase == self.PHASE_END:
            return

        # メッセージ表示中
        if self.showing_message:
            done = self.message_window.handle_event(event)
            if done:
                self.showing_message = False
                self._advance_phase()
            return

        # コマンド選択
        if self.phase == self.PHASE_COMMAND and self.command_menu:
            result = self.command_menu.handle_event(event)
            if result is not None and result >= 0:
                self._handle_command(result)
            return

        # 呪文選択
        if self.phase == self.PHASE_SPELL_SELECT and self.spell_menu:
            result = self.spell_menu.handle_event(event)
            if result is not None:
                if result == -1:
                    self.phase = self.PHASE_COMMAND
                    self.spell_menu = None
                    self._show_command_menu()
                else:
                    self._cast_spell(result)
            return

        # 道具選択
        if self.phase == self.PHASE_ITEM_SELECT and self.item_menu:
            result = self.item_menu.handle_event(event)
            if result is not None:
                if result == -1:
                    self.phase = self.PHASE_COMMAND
                    self.item_menu = None
                    self._show_command_menu()
                else:
                    self._use_item(result)
            return

    def _advance_phase(self):
        """次のフェーズへ"""
        if self.phase == self.PHASE_APPEAR:
            self.phase = self.PHASE_COMMAND
            self._show_command_menu()

        elif self.phase == self.PHASE_EXECUTE:
            if self.battle_over:
                if self.player_won:
                    self._show_victory()
                else:
                    self._show_defeat()
            else:
                # 次のターン
                self.phase = self.PHASE_COMMAND
                self._show_command_menu()

        elif self.phase == self.PHASE_RESULT:
            if self.level_ups:
                self._show_level_up()
            else:
                self.phase = self.PHASE_END
                self.game.pop_state()

        elif self.phase == self.PHASE_LEVEL_UP:
            if self.level_ups:
                self._show_level_up()
            else:
                self.phase = self.PHASE_END
                self.game.pop_state()

    def _show_command_menu(self):
        """コマンドメニュー表示"""
        self.command_menu = Menu(
            16, SCREEN_HEIGHT // 2 - 80,
            200, ['たたかう', 'じゅもん', 'どうぐ', 'にげる'],
        )

    def _handle_command(self, index):
        """コマンド選択処理"""
        commands = ['たたかう', 'じゅもん', 'どうぐ', 'にげる']
        cmd = commands[index]
        self.command_menu = None

        if cmd == 'たたかう':
            self._execute_turn('attack')

        elif cmd == 'じゅもん':
            spells = self.player.known_spells
            battle_spells = []
            for s in spells:
                info = SPELLS[s]
                if info['type'] in ('attack', 'heal', 'status'):
                    battle_spells.append(s)
            if not battle_spells:
                self.message_window.show('つかえる じゅもんが ない！')
                self.showing_message = True
                self.phase = self.PHASE_EXECUTE
                self.battle_over = False
                return
            self.spell_menu = Menu(
                220, SCREEN_HEIGHT // 2 - 80,
                240,
                battle_spells,
            )
            self.phase = self.PHASE_SPELL_SELECT

        elif cmd == 'どうぐ':
            if not self.player.items:
                self.message_window.show('もちものが ない！')
                self.showing_message = True
                self.phase = self.PHASE_EXECUTE
                self.battle_over = False
                return
            self.item_menu = Menu(
                220, SCREEN_HEIGHT // 2 - 80,
                240,
                self.player.items[:],
            )
            self.phase = self.PHASE_ITEM_SELECT

        elif cmd == 'にげる':
            self._try_run()

    def _cast_spell(self, index):
        """呪文を使う"""
        spells = [s for s in self.player.known_spells
                  if SPELLS[s]['type'] in ('attack', 'heal', 'status')]
        spell_name = spells[index]
        spell = SPELLS[spell_name]
        self.spell_menu = None

        if not self.player.use_mp(spell['mp']):
            self.message_window.show('MPが たりない！')
            self.showing_message = True
            self.phase = self.PHASE_COMMAND
            self._show_command_menu()
            return

        self._execute_turn('spell', spell_name=spell_name)

    def _use_item(self, index):
        """道具を使う"""
        item_name = self.player.items[index]
        self.item_menu = None
        self._execute_turn('item', item_name=item_name)

    def _try_run(self):
        """逃走判定"""
        # 逃走成功率: プレイヤーの素早さ / 敵の素早さ * 0.75
        chance = self.player.agility / max(1, self.enemy_agility) * 0.75
        if random.random() < chance:
            self.message_window.show(f'{self.player.name}は にげだした！')
            self.showing_message = True
            self.battle_over = True
            self.ran_away = True
            self.phase = self.PHASE_EXECUTE
        else:
            self.message_window.show('しかし まわりこまれてしまった！')
            self.showing_message = True
            # 敵のターン
            self._enemy_turn()

    def _execute_turn(self, action, spell_name=None, item_name=None):
        """1ターン実行"""
        messages = []

        # 素早さ判定で先攻後攻を決定
        player_first = (self.player.agility + random.randint(0, 10) >=
                        self.enemy_agility + random.randint(0, 10))

        if player_first:
            messages.extend(self._player_action(action, spell_name, item_name))
            if self.enemy_hp > 0 and not self.enemy_asleep:
                messages.extend(self._enemy_action())
            elif self.enemy_asleep:
                messages.append(f'{self.enemy_name}は ねむっている。')
                if random.random() < 0.33:
                    self.enemy_asleep = False
                    messages.append(f'{self.enemy_name}は めをさました！')
        else:
            if not self.enemy_asleep:
                messages.extend(self._enemy_action())
            else:
                messages.append(f'{self.enemy_name}は ねむっている。')
                if random.random() < 0.33:
                    self.enemy_asleep = False
                    messages.append(f'{self.enemy_name}は めをさました！')
            if self.player.hp > 0:
                messages.extend(self._player_action(action, spell_name, item_name))

        self.message_window.show_many(messages)
        self.showing_message = True
        self.phase = self.PHASE_EXECUTE

        # 勝敗判定
        if self.enemy_hp <= 0:
            self.battle_over = True
            self.player_won = True
        elif self.player.is_dead():
            self.battle_over = True
            self.player_won = False

    def _player_action(self, action, spell_name=None, item_name=None):
        """プレイヤーの行動"""
        messages = []

        if action == 'attack':
            # ダメージ計算: ATK - DEF/2 + random
            base_dmg = self.player.attack_power - self.enemy_defense // 2
            damage = max(1, base_dmg + random.randint(-2, 2))
            self.enemy_hp = max(0, self.enemy_hp - damage)
            messages.append(
                f'{self.player.name}の こうげき！\n'
                f'{self.enemy_name}に {damage}の ダメージ！')

        elif action == 'spell':
            spell = SPELLS[spell_name]
            messages.append(f'{self.player.name}は {spell_name}を となえた！')

            if spell['type'] == 'attack':
                damage = spell['power'] + random.randint(-3, 3)
                # 魔法防御はないので直接ダメージ
                damage = max(1, damage)
                self.enemy_hp = max(0, self.enemy_hp - damage)
                messages.append(f'{self.enemy_name}に {damage}の ダメージ！')

            elif spell['type'] == 'heal':
                heal = min(spell['power'], self.player.max_hp - self.player.hp)
                self.player.heal(spell['power'])
                messages.append(f'HPが {heal} かいふくした！')

            elif spell['type'] == 'status':
                if spell.get('effect') == 'sleep':
                    if random.random() < 0.5:
                        self.enemy_asleep = True
                        messages.append(f'{self.enemy_name}は ねむりについた！')
                    else:
                        messages.append('しかし きかなかった！')
                elif spell.get('effect') == 'stopspell':
                    if random.random() < 0.5:
                        self.enemy_spells = []
                        messages.append(f'{self.enemy_name}の じゅもんを ふうじた！')
                    else:
                        messages.append('しかし きかなかった！')

        elif action == 'item':
            from src.data import ITEMS
            info = ITEMS.get(item_name)
            if info and info['type'] == 'consumable' and info['effect'] == 'heal':
                heal = min(info['power'], self.player.max_hp - self.player.hp)
                self.player.heal(info['power'])
                self.player.remove_item(item_name)
                messages.append(
                    f'{item_name}を つかった！\n'
                    f'HPが {heal} かいふくした！')
            else:
                messages.append(f'{item_name}を つかった！\nしかし なにも おこらなかった。')

        return messages

    def _enemy_action(self):
        """敵の行動"""
        messages = []

        # 呪文使用判定 (30%の確率で呪文を使う)
        if self.enemy_spells and random.random() < 0.3:
            spell_name = random.choice(self.enemy_spells)
            spell = SPELLS.get(spell_name)
            if spell:
                messages.append(f'{self.enemy_name}は {spell_name}を となえた！')
                if spell['type'] == 'attack':
                    damage = spell['power'] + random.randint(-3, 3)
                    damage = max(1, damage)
                    self.player.take_damage(damage)
                    messages.append(f'{self.player.name}は {damage}の ダメージをうけた！')
                elif spell['type'] == 'status':
                    if spell.get('effect') == 'sleep':
                        messages.append('しかし きかなかった！')  # プレイヤーには効かない (簡略化)
                return messages

        # 特殊攻撃
        if self.enemy_special == 'fire_breath':
            damage = random.randint(16, 24)
            self.player.take_damage(damage)
            messages.append(
                f'{self.enemy_name}は ひをはいた！\n'
                f'{self.player.name}は {damage}の ダメージをうけた！')
            return messages
        elif self.enemy_special == 'fire_breath_strong':
            damage = random.randint(30, 45)
            self.player.take_damage(damage)
            messages.append(
                f'{self.enemy_name}は はげしく ひをはいた！\n'
                f'{self.player.name}は {damage}の ダメージをうけた！')
            return messages

        # 通常攻撃
        base_dmg = self.enemy_attack - self.player.defense_power // 2
        damage = max(1, base_dmg + random.randint(-2, 2))
        self.player.take_damage(damage)
        messages.append(
            f'{self.enemy_name}の こうげき！\n'
            f'{self.player.name}は {damage}の ダメージをうけた！')

        return messages

    def _enemy_turn(self):
        """逃げ失敗時の敵ターン"""
        messages = self._enemy_action()
        self.message_window.show_many(messages)
        self.showing_message = True
        self.phase = self.PHASE_EXECUTE

        if self.player.is_dead():
            self.battle_over = True
            self.player_won = False

    def _show_victory(self):
        """勝利メッセージ"""
        messages = [
            f'{self.enemy_name}を たおした！',
            f'{self.enemy_exp}の けいけんちと\n{self.enemy_gold}ゴールドを かくとく！',
        ]
        self.player.gold += self.enemy_gold
        self.level_ups = self.player.gain_exp(self.enemy_exp)

        self.message_window.show_many(messages)
        self.showing_message = True
        self.phase = self.PHASE_RESULT

    def _show_defeat(self):
        """敗北メッセージ"""
        messages = [
            f'{self.player.name}は しんでしまった！',
            'おきのどくですが\nぼうけんのしょは きえてしまいました…',
        ]
        self.message_window.show_many(messages)
        self.showing_message = True
        self.phase = self.PHASE_RESULT

        # 復活処理 (簡易: 城に戻してHP半分回復)
        self.player.hp = self.player.max_hp // 2
        self.player.mp = self.player.max_mp // 2
        self.player.gold = self.player.gold // 2
        self.player.map_name = 'castle'
        self.player.tile_x = 7
        self.player.tile_y = 4
        self.field_state.load_map('castle')

    def _show_level_up(self):
        """レベルアップメッセージ"""
        if not self.level_ups:
            return
        lu = self.level_ups.pop(0)
        messages = [
            f'レベルが {lu["level"]}に あがった！',
            f'HP +{lu["hp_up"]}  MP +{lu["mp_up"]}\n'
            f'ちから +{lu["str_up"]}  すばやさ +{lu["agi_up"]}',
        ]
        for spell in lu['new_spells']:
            messages.append(f'{spell}の じゅもんを おぼえた！')

        self.message_window.show_many(messages)
        self.showing_message = True
        self.phase = self.PHASE_LEVEL_UP

    def update(self):
        self.message_window.update()

    def draw(self, surface):
        # 背景 (黒)
        surface.fill(BLACK)

        # 敵の描画エリア (上半分)
        enemy_area = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT // 2 - 40)

        # 敵キャラ描画
        if self.enemy_hp > 0:
            self._draw_enemy(surface, enemy_area)

        # HPバー
        bar_y = enemy_area.bottom + 10
        self._draw_hp_bar(surface, bar_y)

        # ステータス表示
        status_text = (
            f'{self.player.name}  Lv{self.player.level}  '
            f'HP:{self.player.hp}/{self.player.max_hp}  '
            f'MP:{self.player.mp}/{self.player.max_mp}')
        status_surf = self.font.render(status_text, True, WHITE)
        surface.blit(status_surf, (20, bar_y + 30))

        # 敵ステータス
        enemy_status = f'{self.enemy_name}  HP:{self.enemy_hp}/{self.enemy_max_hp}'
        enemy_surf = self.font.render(enemy_status, True, WHITE)
        surface.blit(enemy_surf, (20, bar_y + 56))

        # コマンドメニュー
        if self.phase == self.PHASE_COMMAND and self.command_menu:
            self.command_menu.draw(surface)

        # 呪文メニュー
        if self.phase == self.PHASE_SPELL_SELECT and self.spell_menu:
            self.spell_menu.draw(surface)

        # 道具メニュー
        if self.phase == self.PHASE_ITEM_SELECT and self.item_menu:
            self.item_menu.draw(surface)

        # メッセージ
        if self.showing_message:
            self.message_window.draw(surface)

    def _draw_enemy(self, surface, area):
        """敵キャラを描画 (簡易的なドット絵風)"""
        cx = area.centerx
        cy = area.centery

        # 敵の大きさ (HPベース)
        size = min(120, 40 + self.enemy_max_hp)

        # 体
        body_rect = pygame.Rect(cx - size // 2, cy - size // 2, size, size)
        pygame.draw.ellipse(surface, self.enemy_color, body_rect)

        # 目
        eye_offset = size // 4
        eye_size = max(4, size // 10)
        pygame.draw.circle(surface, WHITE,
                           (cx - eye_offset, cy - size // 6), eye_size + 2)
        pygame.draw.circle(surface, WHITE,
                           (cx + eye_offset, cy - size // 6), eye_size + 2)
        pygame.draw.circle(surface, BLACK,
                           (cx - eye_offset, cy - size // 6), eye_size)
        pygame.draw.circle(surface, BLACK,
                           (cx + eye_offset, cy - size // 6), eye_size)

        # 口
        mouth_y = cy + size // 6
        mouth_w = size // 3
        pygame.draw.arc(surface, (200, 50, 50),
                        (cx - mouth_w // 2, mouth_y - 5, mouth_w, 10),
                        3.14, 0, 2)

        # 名前
        name_surf = self.font_large.render(self.enemy_name, True, WHITE)
        name_rect = name_surf.get_rect(center=(cx, area.bottom - 30))
        surface.blit(name_surf, name_rect)

    def _draw_hp_bar(self, surface, y):
        """HP/MPバーを描画"""
        bar_width = 200
        bar_height = 8

        # HPバー
        hp_ratio = self.player.hp / max(1, self.player.max_hp)
        pygame.draw.rect(surface, (60, 60, 60),
                         (SCREEN_WIDTH - bar_width - 30, y, bar_width, bar_height))
        hp_color = (0, 200, 0) if hp_ratio > 0.3 else (200, 200, 0) if hp_ratio > 0.15 else (200, 0, 0)
        pygame.draw.rect(surface, hp_color,
                         (SCREEN_WIDTH - bar_width - 30, y,
                          int(bar_width * hp_ratio), bar_height))

        # MPバー
        mp_ratio = self.player.mp / max(1, self.player.max_mp)
        pygame.draw.rect(surface, (60, 60, 60),
                         (SCREEN_WIDTH - bar_width - 30, y + 14, bar_width, bar_height))
        pygame.draw.rect(surface, (0, 100, 200),
                         (SCREEN_WIDTH - bar_width - 30, y + 14,
                          int(bar_width * mp_ratio), bar_height))
