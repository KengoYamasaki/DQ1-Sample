# CLAUDE.md

## Project Overview

**DQ1-Sample** はファミコン版ドラゴンクエスト1を再現するPython + Pygameプロジェクトです。

- **言語:** Python 3.11+
- **フレームワーク:** Pygame 2.5+
- **ゲーム内容:** タイルベース2D RPG、ターン制1対1戦闘、NPC会話、装備・アイテム・呪文システム

## Quick Start

```bash
pip install -r requirements.txt
python main.py
```

### 操作方法

| キー | 操作 |
|------|------|
| 方向キー | 移動 |
| Z | 決定 / はなす |
| X | キャンセル |
| Space | メニュー |
| Escape | 終了 |

## Repository Structure

```
DQ1-Sample/
├── main.py              # エントリポイント
├── requirements.txt     # 依存パッケージ (pygame)
├── CLAUDE.md            # このファイル
├── README.md            # プロジェクト概要
└── src/
    ├── __init__.py
    ├── config.py        # 定数・設定 (画面サイズ、タイル定義、カラー、キー設定)
    ├── data.py          # ゲームデータ (敵・アイテム・呪文・レベルテーブル・マップ)
    ├── player.py        # プレイヤークラス (ステータス・装備・インベントリ)
    ├── ui.py            # DQスタイルUI (ウィンドウ・メニュー・テキスト表示)
    ├── tilemap.py       # タイルマップ描画・当たり判定
    ├── game.py          # メインゲームループ・ステート管理
    ├── title.py         # タイトル画面ステート
    ├── field.py         # フィールド（マップ移動）ステート
    └── battle.py        # 戦闘ステート
```

## Architecture

### State Stack Pattern

ゲームは `Game.state_stack` でステートを管理します:

- **push_state(state)**: 新しいステートをスタックに追加 (例: 戦闘開始)
- **pop_state()**: 現在のステートを除去 (例: 戦闘終了 → フィールドに戻る)
- **change_state(state)**: 現在のステートを入れ替え (例: タイトル → フィールド)

各ステートは `handle_event(event)`, `update()`, `draw(surface)` を実装します。

### Key Modules

- **config.py**: タイルサイズ (48px)、画面サイズ (768x720 = 16x15タイル)、キー設定、タイル種別定義
- **data.py**: 全ゲームデータを一元管理。マップは文字列配列で定義 (`G`=草, `W`=水, `M`=山, etc.)
- **player.py**: 攻撃力=ちから+武器、守備力=すばやさ/2+鎧+盾。DQ1準拠の計算式
- **ui.py**: DQ風の黒背景白枠ウィンドウ、文字送り、選択メニュー
- **tilemap.py**: タイルをプログラムで描画 (スプライト不要)。カメラはプレイヤー中心

### Map Format

マップは `data.py` に文字列リストで定義:
```
G=草  W=水  M=山  F=森  D=砂漠  B=橋
.=床  #=壁  +=ドア  >=下り階段  <=上り階段
C=城  T=町  V=洞窟  S=沼  R=屋根  K=カウンター  X=宝箱  O=玉座
```

### Combat System

- DQ1準拠の1対1ターン制
- ダメージ = こうげき力 - しゅび力/2 ± ランダム
- 素早さで先攻後攻を判定
- エンカウントは城からの距離でテーブルが変化 (field_start → field_mid → field_far)

## Conventions

### Language

- コード内のdocstring・コメントは日本語
- ゲームテキスト (会話・メッセージ) は全て日本語
- 変数名・関数名は英語 (snake_case)
- クラス名は英語 (PascalCase)

### Code Style

- Python標準のスタイル (PEP 8準拠)
- 型ヒントは必要に応じて
- import順序: 標準ライブラリ → pygame → src内モジュール

### Adding Content

- **新しい敵**: `data.py` の `ENEMIES` に追加、`ENCOUNTER_TABLES` のテーブルにも追加
- **新しいアイテム/装備**: `data.py` の `ITEMS`, `WEAPONS`, `ARMORS`, `SHIELDS` に追加
- **新しいマップ**: `data.py` にマップ文字列を定義 → `MAP_DATA` に追加 → `WARPS` で接続
- **新しいNPC**: `data.py` の `NPCS` にマップ名をキーにして追加
- **新しい呪文**: `data.py` の `SPELLS` に追加。戦闘時処理は `battle.py` の `_player_action` と `_enemy_action`

## For AI Assistants

### Before making changes

1. `config.py` でタイルサイズ・画面設定を確認
2. `data.py` で既存のゲームデータ構造を確認
3. ステート間の遷移フロー (`game.py` の push/pop/change) を理解する

### Key guidance

- DQ1のゲーム性を尊重する。派手な演出より堅実なRPGメカニクスを優先
- マップは文字列ベースで管理。JSONファイルへの移行は将来の改善として可能
- スプライトアセットは未使用。`tilemap.py` でプログラム描画。スプライト対応は追加可能
- フォントは日本語対応システムフォントを自動検出 (`ui.py` の `load_font`)
- テスト: 現在テストフレームワークは未設定。`python -c "from src.* import ..."` でインポート確認可能

### Known limitations / future work

- セーブ/ロード機能が未実装
- 音楽・効果音が未実装
- 呪文メニューがフィールドで簡略化 (最初の回復呪文のみ使用)
- ショップの売却機能なし
- ダンジョンの暗闘/照明システムなし
- 竜王の城が未実装
