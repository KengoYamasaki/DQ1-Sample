"""プレイヤーキャラクター"""

from src.data import LEVEL_TABLE, SPELLS, WEAPONS, ARMORS, SHIELDS, ITEMS, MAX_LEVEL


class Player:
    """勇者の状態を管理するクラス"""

    def __init__(self):
        self.name = 'ゆうしゃ'
        self.level = 1
        stats = LEVEL_TABLE[1]
        self.max_hp = stats[1]
        self.hp = self.max_hp
        self.max_mp = stats[2]
        self.mp = self.max_mp
        self.strength = stats[3]
        self.agility = stats[4]
        self.exp = 0
        self.gold = 0

        # 装備
        self.weapon = 'なし'
        self.armor = 'なし'
        self.shield = 'なし'

        # アイテム (最大8個)
        self.items = ['やくそう', 'やくそう', 'やくそう']

        # 位置情報
        self.map_name = 'field'
        self.tile_x = 19
        self.tile_y = 15
        self.direction = (0, -1)  # 上向き

        # 開けた宝箱 (set of (map, x, y))
        self.opened_chests = set()

        # フラグ
        self.flags = set()

    @property
    def attack_power(self):
        """こうげき力 = ちから + 武器攻撃力"""
        weapon_atk = WEAPONS.get(self.weapon, {}).get('attack', 0)
        return self.strength + weapon_atk

    @property
    def defense_power(self):
        """しゅび力 = すばやさ/2 + 鎧防御力 + 盾防御力"""
        armor_def = ARMORS.get(self.armor, {}).get('defense', 0)
        shield_def = SHIELDS.get(self.shield, {}).get('defense', 0)
        return self.agility // 2 + armor_def + shield_def

    @property
    def known_spells(self):
        """現在のレベルで使える呪文リスト"""
        return [name for name, info in SPELLS.items()
                if info['level'] <= self.level]

    def gain_exp(self, amount):
        """経験値を得てレベルアップを判定。レベルアップ情報を返す"""
        self.exp += amount
        level_ups = []

        while self.level < MAX_LEVEL:
            next_level = self.level + 1
            needed = LEVEL_TABLE[next_level][0]
            if self.exp >= needed:
                self.level = next_level
                stats = LEVEL_TABLE[next_level]
                old_max_hp = self.max_hp
                old_max_mp = self.max_mp
                old_str = self.strength
                old_agi = self.agility

                self.max_hp = stats[1]
                self.max_mp = stats[2]
                self.strength = stats[3]
                self.agility = stats[4]
                self.hp = self.max_hp
                self.mp = self.max_mp

                # 新しく覚える呪文
                new_spells = [name for name, info in SPELLS.items()
                              if info['level'] == next_level]

                level_ups.append({
                    'level': next_level,
                    'hp_up': self.max_hp - old_max_hp,
                    'mp_up': self.max_mp - old_max_mp,
                    'str_up': self.strength - old_str,
                    'agi_up': self.agility - old_agi,
                    'new_spells': new_spells,
                })
            else:
                break

        return level_ups

    def add_item(self, item_name):
        """アイテムを追加。成功したらTrue"""
        if len(self.items) >= 8:
            return False
        self.items.append(item_name)
        return True

    def remove_item(self, item_name):
        """アイテムを1つ削除"""
        if item_name in self.items:
            self.items.remove(item_name)
            return True
        return False

    def use_item(self, item_name):
        """アイテムを使用。効果の説明テキストを返す"""
        info = ITEMS.get(item_name)
        if not info:
            return None

        if info['type'] == 'consumable':
            if info['effect'] == 'heal':
                heal = min(info['power'], self.max_hp - self.hp)
                self.hp += heal
                self.remove_item(item_name)
                return f'HPが {heal} かいふくした！'
            elif info['effect'] == 'return':
                self.remove_item(item_name)
                return 'ラダトームじょうに もどった！'
            elif info['effect'] == 'light':
                self.remove_item(item_name)
                return 'あたりが あかるくなった！'

        return 'しかし なにも おこらなかった。'

    def can_equip(self, item_name):
        """装備可能かどうか"""
        return (item_name in WEAPONS or
                item_name in ARMORS or
                item_name in SHIELDS)

    def equip(self, item_name):
        """装備する。外した装備を返す"""
        if item_name in WEAPONS:
            old = self.weapon
            self.weapon = item_name
            return old
        elif item_name in ARMORS:
            old = self.armor
            self.armor = item_name
            return old
        elif item_name in SHIELDS:
            old = self.shield
            self.shield = item_name
            return old
        return None

    def heal_at_inn(self):
        """宿屋で全回復"""
        self.hp = self.max_hp
        self.mp = self.max_mp

    def is_dead(self):
        return self.hp <= 0

    def take_damage(self, damage):
        """ダメージを受ける"""
        self.hp = max(0, self.hp - damage)

    def heal(self, amount):
        """HP回復"""
        self.hp = min(self.max_hp, self.hp + amount)

    def use_mp(self, cost):
        """MP消費。足りればTrue"""
        if self.mp >= cost:
            self.mp -= cost
            return True
        return False
