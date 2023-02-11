from implicari.config.settings import *


SECRET_KEY = 'soy-una-super-secret-key'
DEBUG = True


ALLOWED_HOSTS = [
    'implicari.localhost',
]

INTERNAL_IPS = [
    '127.0.0.1',
]


ROOT_URLCONF = 'implicari.config.develop.urls'



INSTALLED_APPS += [
    'django_extensions',
    'debug_toolbar',
]


MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]


REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] += [
    'rest_framework.authentication.SessionAuthentication',
    'rest_framework.authentication.BasicAuthentication',
]


DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.history.HistoryPanel',
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]
