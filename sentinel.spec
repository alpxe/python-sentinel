# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('bgm.mp3', '.')],
    hiddenimports=['win32gui'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'pygame', 'numpy', 'matplotlib', 'pandas', 'tkinter',
        'PyQt5.QtWebEngine', 'PyQt5.QtWebEngineCore', 'PyQt5.QtWebEngineWidgets',
        'PyQt5.QtWebKit', 'PyQt5.QtWebKitWidgets',
        'PyQt5.QtSql', 'PyQt5.QtTest', 'PyQt5.QtXml', 'PyQt5.QtDesigner',
        'PyQt5.QtPrintSupport', 'PyQt5.QtBluetooth', 'PyQt5.QtLocation',
        'PyQt5.QtPositioning', 'PyQt5.QtSensors', 'PyQt5.QtSvg',
        'libcrypto', 'libssl', 'opengl32sw'
    ],
    noarchive=False,
    optimize=2,
)

# --- 强力割肉环节 ---
# 定义我们要彻底干掉的关键词（不区分大小写）
excluded_dlls = [
    'opengl32sw', 'd3dcompiler', 'qt5quick', 'qt5qml',
    'qt5svg', 'qt5sql', 'qt5test', 'qt5xml', 'qt5designer'
]

def is_excluded(name):
    name = name.lower()
    for skip in excluded_dlls:
        if skip in name:
            return True
    return False

# 重新构建二进制列表
old_count = len(a.binaries)
a.binaries = [x for x in a.binaries if not is_excluded(x[0])]
new_count = len(a.binaries)

print(f"\n[瘦身成功] 删除了 {old_count - new_count} 个多余二进制文件！\n")
# --------------------

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='sentinel',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
