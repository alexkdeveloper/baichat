project('baichat',
          version: '0.1.1',
    meson_version: '>= 0.62.0',
  default_options: [ 'warning_level=2', 'werror=false', ],
)

i18n = import('i18n')
gnome = import('gnome')
python = import('python')

# Constants
PROJECT_RDNN_NAME = 'io.github.alexkdeveloper.baichat'

PROJECT_URL = 'https://github.com/alexkdeveloper/baichat'

git_bin = find_program('git', required: false)

# Set APPLICATION_ID and VERSION_SUFFIX
  VERSION_SUFFIX = ''
  APPLICATION_ID = PROJECT_RDNN_NAME

# Python installation directory
PY_INSTALLDIR = python.find_installation('python3', required: true, modules: ['lxml'])

# Check if python3 is installed
if not PY_INSTALLDIR.found()
    error('No valid python3 binary found')
endif

PKGDATA_DIR = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
MODULE_DIR = join_paths(PKGDATA_DIR, 'baichat')

conf = configuration_data()
conf.set('APP_ID', APPLICATION_ID)
conf.set('PKGDATA_DIR', PKGDATA_DIR)
conf.set('DATA_DIR', join_paths(get_option('prefix'), get_option('datadir')))
conf.set('LOCALE_DIR', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('PYTHON', PY_INSTALLDIR.full_path())
conf.set('VERSION', meson.project_version() + VERSION_SUFFIX)
conf.set('BUILD_TYPE', get_option('buildtype'))
conf.set('SCHEMAS_DIR', PKGDATA_DIR)
conf.set('SOURCE_DIR', meson.current_source_dir())
conf.set('BUILD_DIR', meson.current_build_dir())

subdir('data')
subdir('src')
subdir('po')

gnome.post_install(
     glib_compile_schemas: true,
    gtk_update_icon_cache: true,
  update_desktop_database: true,
)
