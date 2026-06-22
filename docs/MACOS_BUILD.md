# MacOS 15 ARM ネイティブアプリ ビルドガイド

## 概要

このドキュメントは、Video Auto Transfer を macOS 15 ARM64 ネイティブアプリケーション（`.app` バンドル）としてビルドするための手順です。

メニューバーに常駐し、ステータス表示、監視フォルダ・ログフォルダへのアクセスが可能な完全な macOS アプリケーションです。

---

## 動作環境

- **macOS**: 15.0 以上
- **CPU**: Apple Silicon（M1, M2, M3, etc.）
- **Python**: 3.8 以上
- **メモリ**: 4GB 以上推奨
- **ディスク容量**: 500MB 以上

---

## 前提条件

### 1. Xcode Command Line Tools をインストール

```bash
xcode-select --install
```

または、App Store から Xcode をインストール:

```bash
xcode-select --switch /Applications/Xcode.app/Contents/Developer
```

### 2. Python 3.8+ がインストールされていることを確認

```bash
python3 --version
```

### 3. Google Drive API の認証情報を準備

- [Google Cloud Console](https://console.cloud.google.com/) から `credentials.json` を取得
- プロジェクトルートに配置

```bash
cp ~/Downloads/credentials.json ./credentials.json
```

---

## ビルド手順

### ステップ 1: リポジトリをクローン

```bash
git clone https://github.com/kato02130628-maker/video-auto-transfer.git
cd video-auto-transfer
```

### ステップ 2: アイコンを生成（オプション）

デフォルトアイコンを生成する場合：

```bash
python3 macos/icon_creator.py
```

**注**: Pillow（PIL）が必要

```bash
pip3 install Pillow
```

既にカスタムアイコンがある場合は、以下のパスに配置:

```
macos/icon.icns      # アプリケーションアイコン（512x512）
macos/icon.png       # メニューバーアイコン（16x16 以上）
```

### ステップ 3: ビルドスクリプトを実行

```bash
chmod +x build_macos_app.sh
bash build_macos_app.sh
```

**スクリプトが実行すること:**
1. 仮想環境を作成
2. 依存パッケージをインストール
3. py2app でネイティブ `.app` をビルド
4. Applications フォルダへのコピーを提案

### ステップ 4: アプリケーションを起動

#### 方法 1: Applications フォルダから起動

```bash
open ~/Applications/"Video Transfer.app"
```

#### 方法 2: ターミナルから直接起動

```bash
open ./dist/"Video Transfer.app"
```

#### 方法 3: Spotlight から検索

`Cmd + Space` → "Video Transfer" と入力 → Enter

---

## 動作確認

### アプリケーションが正常に起動している場合

1. **メニューバーに表示**
   - 画面右上のメニューバーに「Video Transfer」アイコンが表示される
   - アイコンをクリックするとメニューが展開される

2. **メニュー機能**
   - ✅ ステータス表示
   - 📁 監視フォルダを開く
   - 📊 ログフォルダを開く
   - 📈 詳細情報
   - ⚙️ 設定
   - ❌ 終了

3. **バックグラウンド動作**
   - `Desktop/収録素材` フォルダを監視
   - 動画ファイルが追加されると自動で Google Drive に転送

---

## トラブルシューティング

### ビルド時のエラー

#### 1. "py2app not found" エラー

```bash
pip3 install py2app
```

#### 2. "rumps not found" エラー

```bash
pip3 install rumps
```

#### 3. "iconutil: command not found" エラー

Xcode Command Line Tools が正しくインストールされていることを確認:

```bash
xcode-select --install
```

### 起動時のエラー

#### 1. "Cannot verify developer" というダイアログが表示される

**解決方法:**

1. Finder で `Applications/Video Transfer.app` を右クリック
2. "開く" をクリック
3. セキュリティ確認ダイアログで "開く" をクリック

代替方法:

```bash
sudo xattr -rd com.apple.quarantine ~/Applications/"Video Transfer.app"
```

#### 2. "credentials.json not found" エラー

Google Drive API の認証ファイルをプロジェクトルートに配置:

```bash
cp ~/Downloads/credentials.json ./credentials.json
```

#### 3. Google Drive への接続エラー

- ネットワーク接続を確認
- Google Cloud Console で Google Drive API が有効になっているか確認
- `token.json` を削除して再認証

```bash
rm ~/Desktop/video-transfer-logs/token.json
```

### アプリケーションが起動しない

#### ログを確認

```bash
log stream --predicate 'process == "Video Transfer"' --level debug
```

または、ログファイルを直接確認:

```bash
open ~/Desktop/video-transfer-logs/
```

#### コンソールで詳細を表示

```bash
./dist/"Video Transfer.app"/Contents/MacOS/"Video Transfer"
```

---

## カスタマイズ

### アイコンを変更

1. `macos/icon.png` をカスタムアイコンに置き換え
2. ビルド

```bash
bash build_macos_app.sh
```

### メニューバー表示テキストを変更

`menubar_app.py` の以下の部分を編集:

```python
super(VideoTransferMenubarApp, self).__init__(
    name="Video Transfer",  # ← ここを変更
    icon="macos/icon.png",
    quit_button=None
)
```

### 監視フォルダを変更

`config.py` の以下の部分を編集:

```python
WATCH_FOLDER = os.path.expanduser("~/Desktop/収録素材")  # ← ここを変更
```

---

## ビルド出力

### ビルド成功時の構成

```
project-root/
├── dist/
│   └── Video Transfer.app          # ← ネイティブ macOS アプリケーション
│       ├── Contents/
│       │   ├── MacOS/
│       │   │   └── Video Transfer  # 実行ファイル
│       │   ├── Resources/
│       │   ├── Frameworks/
│       │   └── Info.plist          # アプリケーションメタデータ
│
├── build/                           # ビルド中間ファイル
├── venv_macos/                      # 仮想環境（削除可能）
```

### アプリケーションをコピー

```bash
cp -r dist/"Video Transfer.app" ~/Applications/
```

---

## 実行時の動作

### ログファイルの場所

```
~/Desktop/video-transfer-logs/
├── transfer_YYYYMMDD.log           # 転送ログ
└── error_YYYYMMDD.log              # エラーログ
```

### トークンファイルの場所

```
~/.video-transfer/
└── token.json                      # Google Drive API トークン
```

---

## パフォーマンス最適化

### メモリ使用量を減らす

`setup_macos.py` の `semi_standalone: True` を確認:

```python
'semi_standalone': True,  # ← システムライブラリを共有
```

### 起動時間を短縮

不要なパッケージを `excludes` に追加:

```python
'excludes': [
    'matplotlib',
    'numpy',
    'pandas',
    # ← ここに追加
],
```

---

## セキュリティに関する注意

### Gatekeeper について

初回実行時に Gatekeeper による検証が実行されます。これは正常な動作です。

### 署名について

Developer ID による署名をする場合:

```bash
codesign --deep --force --verify --verbose --sign - ./dist/"Video Transfer.app"
```

---

## よくある質問（FAQ）

### Q: アプリケーションを Dock から起動できますか？

**A:** はい。`setup_macos.py` の `LSUIElement: False` により、Dock に表示されます。

Dock に表示させたくない場合:

```python
'LSUIElement': True,  # Dock に表示しない
```

そして再度ビルドしてください。

### Q: 自動起動（ログイン時）をサポートしていますか？

**A:** 現在はサポートされていません。手動で起動が必要です。

ただし、以下の方法で自動起動を設定できます:

**方法 1: System Preferences から**
1. System Preferences → General → Login Items
2. Video Transfer.app を追加

**方法 2: LaunchAgent を使用**

`~/Library/LaunchAgents/com.videotransfer.app.plist` に以下を作成:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.videotransfer.app</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Applications/Video Transfer.app/Contents/MacOS/Video Transfer</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

そして有効化:

```bash
launchctl load ~/Library/LaunchAgents/com.videotransfer.app.plist
```

### Q: アンインストール方法は？

**A:** Finder で以下を削除:

```bash
rm -rf ~/Applications/"Video Transfer.app"
rm -rf ~/Desktop/video-transfer-logs/
```

---

## サポート

問題が発生した場合:

1. ログファイルを確認
2. GitHub Issues で報告
3. ビルドログを添付

---

## ライセンス

MIT License

---

## 更新ログ

### Version 1.0.0
- 初回リリース
- macOS 15 ARM64 対応
- メニューバーアプリケーション実装
- py2app ビルドシステム実装
