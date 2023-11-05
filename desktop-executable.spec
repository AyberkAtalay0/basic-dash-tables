# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['desktop-executable.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['dash', 'dash_auth', 'dash_mantine_components', 'flask', 'pandas', 'plotly', 'tabula', 'unidecode', 'gunicorn', 'openpyxl', 'PyQt5', 'PyQt5-Frameless-Window', 'PyQtWebEngine', 'PyQt5.QtWebEngineWidgets', 'PyQtWebEngine-Qt5', 'requests', 'pyautogui', 'pywin32', 'qframelesswindow', 'win32crypt'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='mhal_panel',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['bin\\assets\\favicon.png'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='mhal_panel',
)
