# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src/duplocloud/cli.py'],
    pathex=['src'],
    binaries=[],
    datas=[],
    hiddenimports=[
        'duplocloud.formats',
        'duplo_resource',
        'duplo_resource.asg',
        'duplo_resource.configmap',
        'duplo_resource.cronjob',
        'duplo_resource.job',
        'duplo_resource.ecs_service',
        'duplo_resource.hosts',
        'duplo_resource.infrastructure',
        'duplo_resource.ingress',
        'duplo_resource.jit',
        'duplo_resource.lambda',
        'duplo_resource.secret',
        'duplo_resource.service',
        'duplo_resource.system',
        'duplo_resource.tenant',
        'duplo_resource.user',
        'duplo_resource.version',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='duploctl',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='cli',
)
