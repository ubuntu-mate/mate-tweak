project('mate-tweak',
  version : '22.10.0',
  meson_version: '>= 0.47.0'
  )

i18n = import('i18n')
python = import('python')
py3 = find_program('python3', required:true)

# The dependency are optional (= not needed to build ).
# Otherwise install it: example: sudo apt install python-gi-dev libgtk-3-dev libnotify-dev
dependency('pygobject-3.0', required: false)
dependency('gtk+-3.0', required: false)
dependency('libnotify', required: false)

prefix = get_option('prefix')
datadir = join_paths(prefix, get_option('datadir'))
bindir = join_paths(prefix, get_option('bindir'))
libexecdir = join_paths(prefix, get_option('libexecdir'))
libdir = join_paths(prefix, get_option('libdir'))
localedir = join_paths(prefix, get_option('localedir'))
sysconfdir = join_paths(prefix, get_option('sysconfdir'))

policydir = join_paths (datadir, 'polkit-1', 'actions')

mate_tweak_in_in = configuration_data()
mate_tweak_in_in.set('PYTHON', py3.path())
mate_tweak_in_in.set('PYOPTIONS', '-OOt')

mate_tweak_in = configure_file(input: 'mate-tweak.in.in',
  output: 'mate-tweak.in',
  configuration: mate_tweak_in_in,
  )

install_data(mate_tweak_in,
  install_mode: 'rwxr-xr-x',
  rename: 'mate-tweak',
  install_dir: get_option('bindir')
  )
install_data(['marco-compton','marco-glx','marco-no-composite','marco-picom','marco-xrender','marco-xr_glx_hybrid'],
  install_mode: 'rwxr-xr-x',
  install_dir: get_option('bindir')
  )

subdir('po')
subdir('MateTweak')
subdir('data')
subdir('util')

meson.add_install_script('post_install.py')
