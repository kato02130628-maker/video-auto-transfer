# Video Auto Transfer - 日本語ドキュメント

Google Drive へ動画ファイルを自動転送するメニューバーアプリケーション

## 📋 目次

1. [概要](#概要)
2. [機能](#機能)
3. [動作環境](#動作環境)
4. [インストール](#インストール)
5. [使用方法](#使用方法)
6. [設定](#設定)
7. [トラブルシューティング](#トラブルシューティング)
8. [FAQ](#faq)

---

## 概要

Video Auto Transfer は、macOS メニューバーに常駐し、指定されたフォルダの動画ファイルを監視し、自動で Google Drive にアップロードするアプリケーションです。

### 主な特徴

- 🎬 **自動監視**: `Desktop/収録素材` フォルダを自動で監視
- 🔄 **並行転送**: 最大 2 本のファイルを同時にアップロード
- 📹 **複数形式対応**: `.mxf`, `.mov`, `.mp4` に対応
- 🔁 **自動リトライ**: 失敗時は自動で再試行（最大 3 回）
- 📊 **詳細ログ**: すべての転送操作をログに記録
- ☁️ **Google Drive 統合**: 自動フォルダ構造を作成
- 📅 **スケジュール連携**: Excel から翌日の予定を取得

---

## 機能

### ファイル監視

- 指定フォルダを常時監視
- 新規ファイル自動検出
- ファイルが完全に書き込まれたかを判定（3 回チェック）

### 並行転送

- 最大 2 本のファイルを同時転送
- 形式制限:
  - ✅ `mxf + mov`, `mxf + mp4`, `mov + mp4` は可能
  - ❌ `mxf + mxf`, `mov + mov`, `mp4 + mp4` は不可

### 転送速度

アップロード速度 350 Mbps を基準に自動計算:

- 7GB: 約 160 分（2 時間 40 分）
- 3.5GB: 約 80 分（1 時間 20 分）

### 自動リトライ

- 転送失敗時に自動で再試行
- 指数バックオフで待機時間を延長
  - 1 回目: 1 秒待機
  - 2 回目: 2 秒待機
  - 3 回目: 4 秒待機

### Google Drive フォルダ構造

```
WorldCup_Soccer/
└── 20260622-0625/          # 4 日間の期間
    └── 0622/               # 日付別フォルダ
        ├── video1.mp4
        ├── video2.mov
        └── video3.mxf
```

### ログ出力

- 日次ログファイル
- エラーログを別ファイルに記録
- 保存先: `~/Desktop/video-transfer-logs/`

---

## 動作環境

### 必須

- **macOS**: 15.0 以上
- **CPU**: Apple Silicon（M1, M2, M3 など）
- **Python**: 3.8 以上

### 推奨

- **メモリ**: 4GB 以上
- **ディスク容量**: 500MB 以上
- **ネットワーク**: 光回線など安定した接続

---

## インストール

### ステップ 1: 前提条件の確認

```bash
# Xcode Command Line Tools をインストール
xcode-select --install

# Python バージョンを確認
python3 --version  # 3.8 以上であること
```

### ステップ 2: リポジトリをクローン

```bash
git clone https://github.com/kato02130628-maker/video-auto-transfer.git
cd video-auto-transfer
```

### ステップ 3: Google Drive API 認証情報を準備

1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. 新規プロジェクトを作成
3. Google Drive API を有効化
4. OAuth 2.0 クライアント ID（デスクトップアプリ）を作成
5. `credentials.json` をダウンロード
6. プロジェクトルートに配置

```bash
cp ~/Downloads/credentials.json ./
```

### ステップ 4: ビルドと インストール

```bash
# ビルドスクリプトを実行
chmod +x build_macos_app.sh
bash build_macos_app.sh
```

スクリプトが以下を自動実行:
- 仮想環境作成
- 依存パッケージインストール
- ネイティブ .app バンドル生成
- Applications フォルダへのコピー提案

---

## 使用方法

### アプリケーションの起動

#### 方法 1: Spotlight から検索（推奨）

1. `Cmd + Space` を押下
2. "Video Transfer" と入力
3. `Enter` キーを押下

#### 方法 2: Finder から起動

1. Finder → Applications
2. "Video Transfer" を見つける
3. ダブルクリック

#### 方法 3: ターミナルから起動

```bash
open ~/Applications/"Video Transfer.app"
```

### メニューバーの操作

メニューバー（画面右上）に「Video Transfer」アイコンが表示されます。

クリックすると以下のメニューが展開:

- **ステータス**: 現在の転送状況を表示
- **📁 監視フォルダを開く**: `Desktop/収録素材` を Finder で開く
- **📊 ログフォルダを開く**: ログフォルダを Finder で開く
- **📈 詳細情報**: キュー数、転送中のファイルなどを表示
- **⚙️ 設定**: 現在の設定を表示
- **❌ 終了**: アプリケーションを終了

### ファイル転送の流れ

1. **自動検出**
   - `Desktop/収録素材` に動画ファイルが追加される
   - アプリが自動で検出

2. **クローズ判定**
   - ファイルサイズの変化がないか 3 回確認
   - 書き込みが完了したと判定

3. **キューに登録**
   - 転送キューに自動追加
   - 形式をチェック

4. **転送開始**
   - 最大 2 本を同時転送
   - 転送中はメニューバーに「🔄」表示

5. **完了またはエラー**
   - 成功時: Google Drive に保存
   - 失敗時: 自動で再試行（最大 3 回）

---

## 設定

### 基本設定ファイル

`config.py` で以下をカスタマイズ可能:

```python
# 監視フォルダ
WATCH_FOLDER = os.path.expanduser("~/Desktop/収録素材")

# クローズ判定
CLOSE_CHECK_INTERVAL = 10  # チェック間隔（秒）
CLOSE_CHECK_COUNT = 3      # チェック回数

# Google Drive 基本フォルダ
GOOGLE_DRIVE_BASE_FOLDER = "WorldCup_Soccer"

# Excel スケジュール
EXCEL_SCHEDULE_FILE = os.path.expanduser("~/Desktop/schedule.xlsx")
```

### カスタマイズ方法

1. `config.py` をテキストエディタで開く
2. 設定値を変更
3. アプリを再起動

### Excel スケジュール ファイル形式

`~/Desktop/schedule.xlsx` の形式:

| 列 A | 列 B |
|------|------|
| 日付 | 予定 |
| 2026-06-23 | World Cup Match A |
| 2026-06-24 | Training |

---

## トラブルシューティング

### アプリが起動しない

#### 1. "Cannot verify developer" エラーが表示される

**解決方法:**

```bash
sudo xattr -rd com.apple.quarantine ~/Applications/"Video Transfer.app"
```

または:

1. Finder → Applications
2. "Video Transfer" を右クリック → 開く
3. セキュリティダイアログで "開く" をクリック

#### 2. "credentials.json not found" エラー

Google Drive 認証ファイルを配置:

```bash
cp ~/Downloads/credentials.json ./credentials.json
```

### ファイルが転送されない

#### 1. ファイルが検出されない

- ファイルが `Desktop/収録素材` フォルダにあるか確認
- ファイル形式が `.mxf`, `.mov`, `.mp4` であるか確認
- ファイルが読み取り可能か確認

#### 2. Google Drive への接続エラー

- インターネット接続を確認
- Google Cloud Console で Drive API が有効か確認
- `token.json` を削除して再認証

```bash
rm ~/Library/Application\ Support/Video\ Transfer/token.json
```

#### 3. ディスク容量が足りない

Google Drive の空き容量を確認:

https://drive.google.com/drive/storage

### パフォーマンスが低い

#### 1. 転送速度が遅い

- ネットワーク接続速度を確認
- 他のアップロードを停止
- WiFi より有線接続を使用

#### 2. CPU/メモリ使用率が高い

- 同時に転送されているファイル数を確認
- 大容量ファイルの場合は待機時間を延長

### ログファイルの確認

ログは以下の場所に保存:

```bash
open ~/Desktop/video-transfer-logs/
```

または ターミナルで:

```bash
tail -f ~/Desktop/video-transfer-logs/transfer_$(date +%Y%m%d).log
```

---

## FAQ

### Q: 複数のファイルを同時に転送できますか？

**A:** はい。最大 2 本まで同時転送可能です。

ただし、以下の制限があります:
- 同じ形式は同時転送不可
- 例: `mp4 + mp4` は不可、`mp4 + mov` は可能

### Q: ファイルサイズが大きい場合の転送時間は？

**A:** アップロード速度 350 Mbps を基準に計算されます:

- 7GB: 約 160 分
- 3.5GB: 約 80 分
- その他: （ファイルサイズ MB / 350）× 60 × 1.2（マージン）

### Q: 転送に失敗したら？

**A:** 自動で再試行されます:

- 1 回目: 1 秒後
- 2 回目: 2 秒後
- 3 回目: 4 秒後
- 3 回すべて失敗: ログに記録

### Q: Google Drive のフォルダ構造を変更できますか？

**A:** はい。`config.py` の `GOOGLE_DRIVE_BASE_FOLDER` と `get_google_drive_folder_path()` 関数を編集してください。

### Q: ログファイルはどこに保存されますか？

**A:** 以下の場所に日次ログが保存されます:

```
~/Desktop/video-transfer-logs/
├── transfer_20260622.log    # 転送ログ
└── error_20260622.log       # エラーログ
```

### Q: アプリケーションをアンインストールするには？

**A:**

```bash
# アプリケーションを削除
rm -rf ~/Applications/"Video Transfer.app"

# 関連ファイルを削除
rm -rf ~/Desktop/video-transfer-logs/
rm -rf ~/Library/Application\ Support/Video\ Transfer/
```

### Q: ログイン時に自動起動させたい

**A:** システム環境設定から設定:

1. システム設定 → 一般 → ログイン項目
2. "Video Transfer" を追加

または LaunchAgent を使用（詳細は `MACOS_BUILD.md` を参照）

---

## サポート

問題が発生した場合:

1. ログファイルを確認
2. このドキュメントのトラブルシューティングを参照
3. GitHub Issues で報告

---

## ライセンス

MIT License

---

## 更新ログ

### Version 1.0.0
- 初回リリース
- macOS 15 ARM64 対応
- メニューバーアプリケーション実装
