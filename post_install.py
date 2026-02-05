#!/usr/bin/env python3

import os
import glob
import subprocess
import sysconfig
from compileall import compile_dir

prefix = os.environ.get('MESON_INSTALL_PREFIX', '/usr/local')
datadir = os.path.join(prefix, 'share')
destdir = os.environ.get('DESTDIR', '')

if __name__=="__main__":
    print('Compiling python bytecode...')
    puredir = sysconfig.get_path('purelib', vars={'base': str(prefix)})
    module_dir = os.path.join(destdir + os.path.join(puredir, 'Mate-Tweak'))
    compile_dir(module_dir, optimize=2)

    if destdir == '':
        print('Updating icon cache...')
        icon_cache_dir = os.path.join(datadir, 'icons', 'hicolor')
        if not os.path.exists(icon_cache_dir):
            os.makedirs(icon_cache_dir)
        subprocess.call(['gtk-update-icon-cache', '-qtf', icon_cache_dir])

        print('Updating desktop database...')
        desktop_database_dir = os.path.join(datadir, 'applications')
        if not os.path.exists(desktop_database_dir):
            os.makedirs(desktop_database_dir)
        subprocess.call(['update-desktop-database', '-q', desktop_database_dir])
