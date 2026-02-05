

desktop_in = configuration_data()
desktop_in.set('VERSION', meson.project_version())

desktop_file = 'mate-tweak.desktop'
i18n.merge_file(
  input: configure_file(
    input: desktop_file + '.in.in',
    output: desktop_file + '.in',
    configuration : desktop_in,
    ),
  output: desktop_file,
  po_dir: join_paths(meson.source_root(), 'po'),
  type: 'desktop',
  install: true,
  install_dir : join_paths(datadir, 'applications')
  )

desktop_file = 'marco-xrender.desktop'
i18n.merge_file(
  input: configure_file(
    input: desktop_file + '.in.in',
    output: desktop_file + '.in',
    configuration : desktop_in,
    ),
  output: desktop_file,
  po_dir: join_paths(meson.source_root(), 'po'),
  type: 'desktop',
  install: true,
  install_dir : join_paths(datadir, 'applications')
  )

desktop_file = 'marco-glx.desktop'
i18n.merge_file(
  input: configure_file(
    input: desktop_file + '.in.in',
    output: desktop_file + '.in',
    configuration : desktop_in,
    ),
  output: desktop_file,
  po_dir: join_paths(meson.source_root(), 'po'),
  type: 'desktop',
  install: true,
  install_dir : join_paths(datadir, 'applications')
  )

desktop_file = 'marco-xr_glx_hybrid.desktop'
i18n.merge_file(
  input: configure_file(
    input: desktop_file + '.in.in',
    output: desktop_file + '.in',
    configuration : desktop_in,
    ),
  output: desktop_file,
  po_dir: join_paths(meson.source_root(), 'po'),
  type: 'desktop',
  install: true,
  install_dir : join_paths(datadir, 'applications')
  )

desktop_file = 'marco-no-composite.desktop'
i18n.merge_file(
  input: configure_file(
    input: desktop_file + '.in.in',
    output: desktop_file + '.in',
    configuration : desktop_in,
    ),
  output: desktop_file,
  po_dir: join_paths(meson.source_root(), 'po'),
  type: 'desktop',
  install: true,
  install_dir : join_paths(datadir, 'applications')
  )

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


org_mate_mate_tweak_policy = configure_file(
  input: 'org.mate.mate-tweak.policy.in',
  output: 'org.mate.mate-tweak.policy',
  configuration: config_py,
  )

install_data(org_mate_mate_tweak_policy,
    install_dir: policydir
)

install_man('mate-tweak.1')
install_data('mate-tweak.ui',
    install_dir: join_paths(datadir, meson.project_name())
)

