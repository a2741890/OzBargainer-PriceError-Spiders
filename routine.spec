# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['routine.py'],
             pathex=['/Users/a2741890/Desktop/Profolio/WebCrawling/ozBargainer'],
             binaries=[('/System/Library/Frameworks/Tk.framework/Tk', 'tk'), ('/System/Library/Frameworks/Tcl.framework/Tcl', 'tcl')],
             datas=[("./scrapy.cfg",".")],
             hiddenimports=["ozBargainer.items","ozBargainer.middlewares",'ozBargainer.pipelines','ozBargainer.settings','ozBargainer.priceError'],
             hookspath=["./hooks/"],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='routine',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='routine')
