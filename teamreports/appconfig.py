# team/reports/appconfig.py

import os

class DevelopmentConfig:
    """Development configuration."""
    DEBUG = True
    API_USERNAME = 'a@pi.com'
    API_PWD = 'api123'
    URL = 'http://127.0.0.1:5000/'
    LOG_LOCATION = 'C:\Project\TeamAssets\deploy\Logs'

class DockerConfig:
    """Development configuration."""
    DEBUG = True
    API_USERNAME = 'a@pi.com'
    API_PWD = 'api123'
    URL = 'http://127.0.0.1:8000/'
    LOG_LOCATION = 'C:\Project\deploy\Logs'    

class TestConfig:
    """Development slawek configuration."""
    DEBUG = True
    API_USERNAME = 'a@pi.com'
    API_PWD = 'api123'
    URL = 'http://127.0.0.1:5000/'
    LOG_LOCATION = 'C:\Project\TeamAssets\deploy\Logs'

class ProductionConfig:
    """TeamPolska prod config"""
    DEBUG = False
    API_USERNAME = os.getenv('APP_SETTINGS_API_USERNAME')
    API_PWD = os.getenv('APP_SETTINGS_API_PWD')
    URL = 'http://35.189.122.45:5000/'
    LOG_LOCATION = os.getenv('APP_SETTINGS_LOG_LOCATION')

class UATConfig:
    """TeamPolska uat config (heroku for now)"""
    DEBUG = True
    URL = 'https://team-services-uat.herokuapp.com/'


    

