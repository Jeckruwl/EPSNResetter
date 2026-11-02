# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller specification for a standalone macOS .app bundle."""

from pathlib import Path
import sysconfig

from PyInstaller.utils.hooks import collect_all, collect_submodules


def discover_mypyc_extensions():
    """Include hashed mypyc runtime modules required by compiled wheels."""
    module_names = set()
    site_packages = {
        sysconfig.get_paths().get("purelib"),
        sysconfig.get_paths().get("platlib"),
    }
    for directory in filter(None, site_packages):
        for extension in Path(directory).glob("*__mypyc*.so"):
            module_names.add(extension.name.split(".", 1)[0])
    return sorted(module_names)


black_datas, black_binaries, black_hiddenimports = collect_all("black")
babel_datas, babel_binaries, babel_hiddenimports = collect_all("babel")

hiddenimports = (
    [
        "babel.numbers",
        "pysnmp.hlapi.v1arch.asyncio",
        "pysnmp_sync_adapter",
        "tkcalendar",
        "text_console",
    ]
    + black_hiddenimports
    + babel_hiddenimports
    + collect_submodules("pysnmp")
    + collect_submodules("pysnmp_sync_adapter")
    + collect_submodules("tkcalendar")
    + discover_mypyc_extensions()
)

a = Analysis(
    ["ui.py"],
    pathex=[],
    binaries=black_binaries + babel_binaries,
    datas=black_datas + babel_datas,
    hiddenimports=hiddenimports,
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
    name="Epson Printer Configuration",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,  # Build for the architecture of the Python running PyInstaller.
    codesign_identity=None,
    entitlements_file=None,
)

app = BUNDLE(
    exe,
    a.binaries,
    a.datas,
    name="Epson Printer Configuration.app",
    bundle_identifier="org.epsonprintconf.desktop",
    info_plist={
        "CFBundleDisplayName": "Epson Printer Configuration",
        "LSMinimumSystemVersion": "11.0",
        "LSApplicationCategoryType": "public.app-category.utilities",
        "NSHighResolutionCapable": True,
    },
)
