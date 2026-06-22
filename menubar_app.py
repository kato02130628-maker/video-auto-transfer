#!/usr/bin/env python3
"""
Menubar Application for Video Auto Transfer

macOS メニューバーに常駐するビデオ自動転送アプリケーション

依存パッケージ: rumps（macOS メニューバーアプリフレームワーク）
"""

import rumps
import logging
import threading
import os
from pathlib import Path
from datetime import datetime
import json

from config import WATCH_FOLDER, get_google_drive_folder_path
from file_monitor import FileMonitor
from upload_manager import UploadManager
from excel_schedule import ExcelScheduleReader
from log_manager import LogManager

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('video_transfer_menubar')

class VideoTransferMenubarApp(rumps.App):
    """メニューバーアプリケーション"""
    
    def __init__(self):
        super(VideoTransferMenubarApp, self).__init__(
            name="Video Transfer",
            icon="macos/icon.png",  # メニューバーアイコン
            quit_button=None  # 終了ボタンをカスタマイズ
        )
        
        self.log_manager = LogManager()
        self.upload_manager = UploadManager()
        self.file_monitor = FileMonitor(self.on_file_ready)
        self.schedule_reader = ExcelScheduleReader()
        self.is_running = False
        self.app_thread = None
        
        # UI 状態
        self.status_message = "初期化中..."
        self.queue_size = 0
        self.active_uploads = 0
        self.completed_count = 0
        self.failed_count = 0
        self.current_files = []
        
        # メニューレイアウトを構築
        self._build_menu()
        
        logger.info("[MENUBAR] Application initialized")
    
    def _build_menu(self):
        """メニューアイテムを構築"""
        # メニューアイテムを定義（上から順に表示）
        self.menu_items = [
            # ステータス
            rumps.MenuItem(
                f"ステータス: {self.status_message}",
                callback=None  # クリック不可
            ),
            None,  # セパレーター
            
            # 監視フォルダを開く
            rumps.MenuItem(
                "📁 監視フォルダを開く",
                callback=self.open_watch_folder
            ),
            
            # ログフォルダを開く
            rumps.MenuItem(
                "📊 ログフォルダを開く",
                callback=self.open_log_folder
            ),
            
            None,  # セパレーター
            
            # 詳細情報
            rumps.MenuItem(
                "📈 詳細情報",
                callback=self.show_detailed_info
            ),
            
            # 設定
            rumps.MenuItem(
                "⚙️ 設定",
                callback=self.show_settings
            ),
            
            None,  # セパレーター
            
            # 終了
            rumps.MenuItem(
                "❌ 終了",
                callback=self.quit_app
            ),
        ]
    
    def on_file_ready(self, file_path):
        """ファイルがクローズ判定完了時のコールバック"""
        logger.info(f"[MENUBAR] File ready for upload: {Path(file_path).name}")
        self.upload_manager.add_task(file_path)
        self.update_status()
    
    @rumps.clicked("📁 監視フォルダを開く")
    def open_watch_folder(self, sender):
        """監視フォルダを Finder で開く"""
        os.system(f'open "{WATCH_FOLDER}"')
        logger.info("[MENUBAR] Opened watch folder in Finder")
    
    @rumps.clicked("📊 ログフォルダを開く")
    def open_log_folder(self, sender):
        """ログフォルダを Finder で開く"""
        log_folder = Path(self.log_manager.get_log_file_path()).parent
        os.system(f'open "{log_folder}"')
        logger.info("[MENUBAR] Opened log folder in Finder")
    
    @rumps.clicked("📈 詳細情報")
    def show_detailed_info(self, sender):
        """詳細情報をポップアップで表示"""
        status = self.upload_manager.get_status()
        
        info_text = f"""Video Auto Transfer - 詳細情報
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【転送状況】
• キュー内: {status['queue_size']} ファイル
• 進行中: {status['active_uploads']} ファイル
• 完了: {status['completed']} ファイル
• 失敗: {status['failed']} ファイル

【アクティブ転送】
"""
        
        if status['active_files']:
            for f in status['active_files']:
                info_text += f"  • {f}\n"
        else:
            info_text += "  (なし)\n"
        
        info_text += f"\n【設定】\n• 監視パス: {WATCH_FOLDER}\n• 転送先: {get_google_drive_folder_path()}"
        
        rumps.alert(
            title="詳細情報",
            message=info_text,
            ok="閉じる"
        )
        logger.info("[MENUBAR] Showed detailed info")
    
    @rumps.clicked("⚙️ 設定")
    def show_settings(self, sender):
        """設定ダイアログを表示"""
        settings_text = f"""【現在の設定】

監視フォルダ:
{WATCH_FOLDER}

Google Drive 転送先:
{get_google_drive_folder_path()}

サポート形式:
• .mxf
• .mov
• .mp4

並行転送数:
最大 2 本同時

リトライ:
最大 3 回

ログ出力:
{self.log_manager.get_log_file_path()}
"""
        
        rumps.alert(
            title="設定",
            message=settings_text,
            ok="了解"
        )
        logger.info("[MENUBAR] Showed settings")
    
    def update_status(self):
        """ステータスを更新"""
        if not self.is_running:
            self.status_message = "停止中"
            return
        
        status = self.upload_manager.get_status()
        self.queue_size = status['queue_size']
        self.active_uploads = status['active_uploads']
        self.completed_count = status['completed']
        self.failed_count = status['failed']
        self.current_files = status['active_files']
        
        # メニューバー表示テキストを更新
        if self.active_uploads > 0:
            self.status_message = f"転送中: {self.active_uploads} / キュー: {self.queue_size}"
            self.title = f"🔄 {self.active_uploads}"
        elif self.queue_size > 0:
            self.status_message = f"キュー待機: {self.queue_size}"
            self.title = f"⏳ {self.queue_size}"
        else:
            self.status_message = "待機中"
            self.title = "✅"
    
    def run_app_thread(self):
        """アプリケーション実行スレッド"""
        logger.info("[MENUBAR] Starting app thread")
        
        try:
            # ファイル監視を開始
            self.file_monitor.start()
            logger.info("[MENUBAR] File monitor started")
            
            # アップロードマネージャーを開始
            self.upload_manager.start()
            logger.info("[MENUBAR] Upload manager started")
            
            # スケジュール読み込み
            self.schedule_reader.read_schedule()
            tomorrow_schedule = self.schedule_reader.get_tomorrow_schedule()
            if tomorrow_schedule:
                logger.info(f"[MENUBAR] Tomorrow's schedule: {tomorrow_schedule}")
            
            self.log_manager.log("Application started (Menubar mode)")
            
            # メインループ
            while self.is_running:
                self.update_status()
                import time
                time.sleep(1)
        
        except Exception as e:
            logger.error(f"[MENUBAR] Error in app thread: {str(e)}")
            self.log_manager.log_error(f"App thread error: {str(e)}")
        
        finally:
            if self.file_monitor.is_running():
                self.file_monitor.stop()
            self.upload_manager.stop()
            logger.info("[MENUBAR] App thread stopped")
    
    @rumps.clicked("❌ 終了")
    def quit_app(self, sender):
        """アプリケーションを終了"""
        logger.info("[MENUBAR] Quit requested")
        self.log_manager.log("Application quit requested")
        
        # バックグラウンドタスクを停止
        self.is_running = False
        
        if self.app_thread and self.app_thread.is_alive():
            self.app_thread.join(timeout=5)
        
        rumps.quit_app()
    
    def run(self, *args, **kwargs):
        """アプリケーションを実行（オーバーライド）"""
        logger.info("[MENUBAR] Application starting")
        
        # アプリケーションスレッドを開始
        self.is_running = True
        self.app_thread = threading.Thread(target=self.run_app_thread, daemon=True)
        self.app_thread.start()
        
        logger.info("[MENUBAR] App thread created, starting menubar event loop")
        
        # rumps メインループ
        super().run(*args, **kwargs)


def main():
    """メイン関数"""
    app = VideoTransferMenubarApp()
    app.run()


if __name__ == "__main__":
    main()
