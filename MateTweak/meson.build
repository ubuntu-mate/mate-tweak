config_py = configuration_data()
config_py.set('prefix', prefix)
config_py.set('datadir', datadir)
config_py.set('pkgdatadir', join_paths(datadir, meson.project_name()))
config_py.set('PACKAGE', meson.project_name())
config_py.set('VERSION', meson.project_version())
config_py.set('GETTEXT_PACKAGE', meson.project_name())
config_py.set('libexecdir', libexecdir)
config_py.set('libdir', libdir)
config_py.set('localedir', localedir)
config_py.set('sysconfdir',sysconfdir)
config_py.set('bindir',bindir)


config = configure_file(
  input: 'config.py.in',
  output: 'config.py',
  configuration: config_py,
  )

matetweak_sources = [
  config,
  'MainWindow.py',
  '__init__.py',
]

py_inst = python.find_installation('python3')
py_inst.install_sources(matetweak_sources,
  pure: true,
  subdir: 'MateTweak'
  )
