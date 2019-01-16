import os
from teamreports import appconfig

VERSION = (0,0,)
build = (0,) if not os.getenv('TRAVIS_BUILD_NUMBER') else (int(os.getenv('TRAVIS_BUILD_NUMBER')),)
__version__ = ".".join([str(x) for x in (VERSION + build)])

app_config = None
app_settings = os.getenv('APP_SETTINGS_TEAMREPORTS', 'heroku')

if app_settings == 'dev':
    app_config = appconfig.DevelopmentConfig
elif app_settings == 'docker':
    app_config = appconfig.DockerConfig    
elif app_settings == 'test':
    app_config = appconfig.TestConfig
elif app_settings == 'prod':
    app_config = appconfig.ProductionConfig
elif app_settings == 'heroku':
    app_config = appconfig.HerokuConfig    
else:
    raise ValueError('Invalid environment name')