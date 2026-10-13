# PyInstaller onedir specification for the Linux game bundle.
from pathlib import Path

PROJECT_ROOT = Path(SPECPATH).resolve()

data_files = [
    (str(path), str(path.parent.relative_to(PROJECT_ROOT)))
    for root in (PROJECT_ROOT / "assets", PROJECT_ROOT / "themes")
    for path in root.rglob("*")
    if path.is_file()
]

a = Analysis(
    [str(PROJECT_ROOT / "src" / "__main__.py")],
    pathex=[str(PROJECT_ROOT)],
    binaries=[],
    datas=data_files,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="Pac-Man",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    contents_directory=".",
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="Pac-Man",
)
