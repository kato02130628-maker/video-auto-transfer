#!/bin/bash

##############################################################################
# Video Auto Transfer - macOS ビルドスクリプト
#
# 使用方法:
#   bash build_macos_app.sh
#
# このスクリプトは以下を実行します:
#   1. 仮想環境の作成
#   2. 依存パッケージのインストール
#   3. py2app でネイティブ .app バンドルをビルド
#   4. アプリケーションを Applications フォルダにコピー
##############################################################################

set -e  # エラーで停止

echo "========================================="
echo "Video Transfer - macOS ビルド"
echo "========================================="

# カラー定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# プロジェクトルート
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="$PROJECT_ROOT/build"
DIST_DIR="$PROJECT_ROOT/dist"
VENV_DIR="$PROJECT_ROOT/venv_macos"

echo -e "${YELLOW}プロジェクトルート: $PROJECT_ROOT${NC}"

# 既存ビルドをクリア
echo -e "${YELLOW}既存ビルドをクリアしています...${NC}"
rm -rf "$BUILD_DIR" "$DIST_DIR" "$VENV_DIR"

# Python バージョン確認
echo -e "${YELLOW}Python バージョンを確認中...${NC}"
python3 --version

# 仮想環境を作成
echo -e "${YELLOW}仮想環境を作成中...${NC}"
python3 -m venv "$VENV_DIR"

# 仮想環境を有効化
echo -e "${YELLOW}仮想環境を有効化中...${NC}"
source "$VENV_DIR/bin/activate"

# pip をアップグレード
echo -e "${YELLOW}pip をアップグレード中...${NC}"
pip install --upgrade pip setuptools wheel

# 依存パッケージをインストール
echo -e "${YELLOW}依存パッケージをインストール中...${NC}"
pip install -r requirements-macos.txt

# py2app をインストール
echo -e "${YELLOW}py2app をインストール中...${NC}"
pip install py2app

# 仮想環境を非有効化
deactivate

# py2app でビルド（仮想環境内で実行）
echo -e "${YELLOW}ネイティブ .app バンドルをビルド中...${NC}"
echo "（これには数分かかる場合があります）"
echo ""

source "$VENV_DIR/bin/activate"
cd "$PROJECT_ROOT"
python setup_macos.py py2app
deactivate

# ビルド成功確認
if [ -d "$DIST_DIR/Video Transfer.app" ]; then
    echo -e "${GREEN}✓ ビルド成功！${NC}"
    echo ""
    echo -e "${GREEN}アプリケーション作成完了:${NC}"
    echo -e "  ${GREEN}$DIST_DIR/Video Transfer.app${NC}"
    echo ""
    
    # Applications フォルダにコピーするか確認
    echo -e "${YELLOW}Applications フォルダにコピーしますか？ (y/n)${NC}"
    read -r response
    
    if [[ "$response" =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Applications フォルダにコピー中...${NC}"
        cp -r "$DIST_DIR/Video Transfer.app" ~/Applications/
        echo -e "${GREEN}✓ コピー完了${NC}"
        echo -e "  ${GREEN}~/Applications/Video Transfer.app${NC}"
        echo ""
        echo -e "${GREEN}アプリケーションは以下の方法で起動できます:${NC}"
        echo -e "  • Finder → Applications → Video Transfer をダブルクリック"
        echo -e "  • Spotlight（cmd+space）で 'Video Transfer' を検索"
        echo -e "  • ターミナルで: open ~/Applications/Video\\ Transfer.app"
    fi
    echo ""
    echo -e "${GREEN}=========================================${NC}"
    echo -e "${GREEN}ビルド完了！${NC}"
    echo -e "${GREEN}=========================================${NC}"
else
    echo -e "${RED}✗ ビルド失敗${NC}"
    echo -e "${RED}エラーログを確認してください${NC}"
    exit 1
fi

# クリーンアップ
echo ""
echo -e "${YELLOW}仮想環境をクリーンアップしますか？ (y/n)${NC}"
read -r cleanup

if [[ "$cleanup" =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}仮想環境を削除中...${NC}"
    rm -rf "$VENV_DIR"
    echo -e "${GREEN}削除完了${NC}"
fi

echo ""
echo -e "${GREEN}完了！${NC}"
