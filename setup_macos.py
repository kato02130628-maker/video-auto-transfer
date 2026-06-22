#!/usr/bin/env python3
"""
py2app setup script for macOS

macOS ネイティブアプリケーション（.app）をビルドするためのセットアップスクリプト

使用方法:
  python setup_macos.py py2app
"""

from setuptools import setup
from pathlib import Path

# プロジェクトルート
PROJECT_ROOT = Path(__file__).parent

APP = [
    {
        'script': 'menubar_app.py',
        'plist': {
            'CFBundleName': 'Video Transfer',
            'CFBundleDisplayName': 'Video Transfer',
            'CFBundleIdentifier': 'com.videotransfer.app',
            'CFBundleVersion': '1.0.0',
            'CFBundleShortVersionString': '1.0.0',
            'NSPrincipalClass': 'NSApplication',
            'NSHighResolutionCapable': True,
            'LSUIElement': False,  # Dock に表示
            'NSRequiresIPhoneOS': False,
            'NSHumanReadableCopyright': 'Copyright © 2026. All rights reserved.',
        }
    }
]

OPTIONS = {
    'py2app': {
        'argv_emulation': False,
        'packages': [
            'watchdog',
            'google',
            'googleapiclient',
            'openpyxl',
            'rumps',
        ],
        'includes': [
            'config',
            'file_monitor',
            'close_detector',
            'upload_manager',
            'google_drive_api',
            'retry_handler',
            'log_manager',
            'excel_schedule',
            'transfer_queue',
        ],
        'excludes': [
            'matplotlib',
            'numpy',
            'pandas',
        ],
        'plist': {
            'CFBundleName': 'Video Transfer',
            'CFBundleDisplayName': 'Video Transfer',
            'CFBundleIdentifier': 'com.videotransfer.app',
            'CFBundleVersion': '1.0.0',
            'CFBundleShortVersionString': '1.0.0',
            'NSPrincipalClass': 'NSApplication',
            'NSHighResolutionCapable': True,
            'NSRequiresIPhoneOS': False,
            'LSUIElement': False,
            'NSHumanReadableCopyright': 'Copyright © 2026. All rights reserved.',
            'NSUserNotificationAlertStyle': 'banner',
        },
        'iconfile': 'macos/icon.icns',  # アプリアイコン
        'resources': [
            'config.py',
            'file_monitor.py',
            'close_detector.py',
            'upload_manager.py',
            'google_drive_api.py',
            'retry_handler.py',
            'log_manager.py',
            'excel_schedule.py',
            'transfer_queue.py',
            'credentials.json',  # Google Drive 認証情報
        ],
        'strip': True,
        'semi_standalone': True,
    }
}

setup(
    name='Video Transfer',
    version='1.0.0',
    description='Google Drive へ動画ファイルを自動転送するメニューバーアプリケーション',
    author='Video Transfer Team',
    url='https://github.com/kato02130628-maker/video-auto-transfer',
    app=APP,
    options=OPTIONS,
    setup_requires=['py2app'],
    install_requires=[
        'google-auth-oauthlib>=1.2.0',
        'google-auth-httplib2>=0.2.0',
        'google-api-python-client>=2.108.0',
        'watchdog>=4.0.0',
        'openpyxl>=3.1.2',
        'rumps>=0.3.0',
        'python-dateutil>=2.8.2',
        'requests>=2.32.3',
    ],
)
