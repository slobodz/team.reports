import os
from teamreports import appconfig

app_config = None
app_settings = os.getenv('APP_SETTINGS_TEAMREPORTS', 'heroku')

if app_settings == 'dev':
    app_config = appconfig.DevelopmentConfig
elif app_settings == 'test':
    app_config = appconfig.TestConfig
elif app_settings == 'prod':
    app_config = appconfig.ProductionConfig
elif app_settings == 'heroku':
    app_config = appconfig.HerokuConfig    
else:
    raise ValueError('Invalid environment name')