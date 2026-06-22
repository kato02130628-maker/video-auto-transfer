# macOS リソース

## ファイル構成

```
macos/
├── icon_creator.py         # アイコン生成スクリプト
├── icon.png               # メニューバーアイコン（自動生成）
├── icon.icns              # macOS アプリアイコン（自動生成）
├── Info.plist             # アプリメタデータ
└── README.md              # このファイル
```

## アイコンの生成

### デフォルトアイコンを生成

```bash
python3 macos/icon_creator.py
```

このコマンドで以下が自動生成されます:
- `icon.png` - メニューバーアイコン
- `icon.icns` - macOS アプリケーションアイコン

### カスタムアイコンを使用

1. カスタムアイコンを PNG 形式で準備（512x512 推奨）
2. `icon.png` に上書き
3. ビルドスクリプトを実行

```bash
bash build_macos_app.sh
```

## Info.plist

アプリケーションのメタデータを定義する XML ファイルです。

### 主要設定項目

| キー | 値 | 説明 |
|------|-----|------|
| CFBundleName | Video Transfer | アプリ名 |
| CFBundleIdentifier | com.videotransfer.app | ユニーク ID |
| CFBundleVersion | 1.0.0 | アプリバージョン |
| LSUIElement | false | Dock に表示 |
| LSMinimumSystemVersion | 10.13 | 最小 macOS バージョン |
| NSHighResolutionCapable | true | Retina 対応 |

## カスタマイズ

### アプリ名を変更

`Info.plist` を編集:

```xml
<key>CFBundleName</key>
<string>Your App Name</string>
```

### Dock への表示を非表示にする

```xml
<key>LSUIElement</key>
<true/>  <!-- メニューバーのみに表示 -->
```

### 最小 macOS バージョンを変更

```xml
<key>LSMinimumSystemVersion</key>
<string>11.0</string>  <!-- macOS 11 以上 -->
```

## トラブルシューティング

### アイコン生成エラー

Pillow がインストールされているか確認:

```bash
pip3 install Pillow
```

### iconutil エラー

Xcode Command Line Tools が必要:

```bash
xcode-select --install
```
