#!/usr/bin/env python3
"""
macOS アイコン生成スクリプト

PNG アイコンから .icns フォーマットに変換

使用方法:
  python macos/icon_creator.py
"""

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

def create_default_icon():
    """デフォルトアイコン（PNG）を作成"""
    print("[INFO] デフォルトアイコンを生成中...")
    
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("[ERROR] PIL がインストールされていません")
        print("        以下のコマンドを実行してください:")
        print("        pip install Pillow")
        return False
    
    # アイコンサイズ
    size = 512
    
    # 背景色（青）
    bg_color = (41, 128, 185)  # #2980B9
    
    # アイコンを作成
    img = Image.new('RGBA', (size, size), bg_color + (255,))
    draw = ImageDraw.Draw(img)
    
    # 中央に「VT」テキストを描画
    try:
        # システムフォントを使用
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 200)
    except:
        font = ImageFont.load_default()
    
    text = "VT"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
    
    # PNG として保存
    icon_path = PROJECT_ROOT / "macos" / "icon.png"
    img.save(icon_path, 'PNG')
    print(f"[INFO] アイコン作成完了: {icon_path}")
    
    return True

def convert_to_icns():
    """PNG を .icns に変換"""
    print("[INFO] PNG を .icns に変換中...")
    
    icon_png = PROJECT_ROOT / "macos" / "icon.png"
    icon_icns = PROJECT_ROOT / "macos" / "icon.icns"
    
    if not icon_png.exists():
        print(f"[ERROR] {icon_png} が見つかりません")
        return False
    
    # macOS の iconutil コマンドを使用
    import subprocess
    
    # .iconset フォルダを作成
    iconset_dir = PROJECT_ROOT / "macos" / "icon.iconset"
    iconset_dir.mkdir(exist_ok=True)
    
    try:
        from PIL import Image
        img = Image.open(icon_png)
        
        # 必要なサイズで PNG を生成
        sizes = [16, 32, 64, 128, 256, 512]
        
        for size in sizes:
            # 通常サイズ
            resized = img.resize((size, size), Image.Resampling.LANCZOS)
            resized.save(iconset_dir / f"icon_{size}x{size}.png")
            
            # 2x サイズ（Retina 対応）
            resized_2x = img.resize((size * 2, size * 2), Image.Resampling.LANCZOS)
            resized_2x.save(iconset_dir / f"icon_{size}x{size}@2x.png")
        
        print(f"[INFO] iconset フォルダを生成完了: {iconset_dir}")
        
        # iconutil で .icns に変換
        result = subprocess.run(
            ['iconutil', '-c', 'icns', str(iconset_dir), '-o', str(icon_icns)],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"[INFO] .icns 変換完了: {icon_icns}")
            return True
        else:
            print(f"[ERROR] iconutil 変換失敗: {result.stderr}")
            return False
    
    except Exception as e:
        print(f"[ERROR] 変換エラー: {str(e)}")
        return False

def main():
    """メイン関数"""
    print("========================================")
    print("macOS アイコン生成")
    print("========================================")
    print()
    
    # デフォルトアイコン作成
    if create_default_icon():
        print()
        # .icns に変換
        if convert_to_icns():
            print()
            print("[INFO] アイコン生成完了！")
            print()
        else:
            print("[WARNING] .icns 変換に失敗しました")
            print("          PNG アイコンは生成されました")
    else:
        print("[ERROR] アイコン生成失敗")

if __name__ == "__main__":
    main()
