This is MATE Tweak, a fork of [mintDesktop](https://github.com/linuxmint/mintdesktop).

  * MATE Tweak removes the Mint specific configuration options.
  * MATE Tweak adds User Interfacing switching.
  * MATE Tweak adds live Compiz switching.

MATE Tweak needs translators!

  * https://www.transifex.com/projects/p/MATE/resource/mate-tweak/

Compile:
-  meson build --libdir=/usr/lib/ --prefix=/usr/ --sysconfdir=/etc
-  cd build
-  meson compile
-  sudo meson install

Remove:
-  sudo ninja uninstall
