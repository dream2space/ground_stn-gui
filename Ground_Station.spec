# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['Ground_Station.py'],
#             pathex=['C:\\Users\\65844\\Desktop\\ground_stn-gui'],
             pathex=['C:\\Users\\user\\Desktop\\ground_stn-gui'],
             binaries=[],
             datas=[],
             hiddenimports=["babel.numbers"],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

a.datas += [('assets/refresh.jpg', 'C:\\Users\\user\\Desktop\\ground_stn-gui\\assets\\refresh.jpg', 'DATA')]
a.datas += [('assets/d2s.png', 'C:\\Users\\user\\Desktop\\ground_stn-gui\\assets\\d2s.png', 'DATA')]
a.datas += [('assets/satellite.ico', 'C:\\Users\\user\\Desktop\\ground_stn-gui\\assets\\satellite.ico', 'DATA')]

#a.datas += [('assets/refresh.jpg', 'C:\\Users\\65844\\Desktop\\ground_stn-gui\\assets\\refresh.jpg', 'DATA')]
#a.datas += [('assets/d2s.png', 'C:\\Users\\65844\\Desktop\\ground_stn-gui\\assets\\d2s.png', 'DATA')]
#a.datas += [('assets/satellite.ico', 'C:\\Users\\65844\\Desktop\\ground_stn-gui\\assets\\satellite.ico', 'DATA')]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Ground_Station',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='assets\\satellite.ico')
