
# """version setup for project"""

# import os

# VERSION = (0,0,)
# build = (0,) if not os.getenv('TRAVIS_BUILD_NUMBER') else (int(os.getenv('TRAVIS_BUILD_NUMBER')),)
# __version__ = ".".join([str(x) for x in (VERSION + build)])


# import os
# import logging
# import datetime
# from team.reports import config

# #config
# app_config = None
# app_settings = os.getenv('APP_SETTINGS_REPORTS', 'dev')

# if app_settings == 'dev':
#     app_config = config.DevelopmentConfig
# elif app_settings == 'test':
#     app_config = config.TestConfig
# elif app_settings == 'prod':
#     app_config = config.ProductionConfig
# else:
#     raise ValueError('Invalid environment name')

# # #logging
# # LOG_LOCATION = app_config.LOG_LOCATION
# # logging.basicConfig(filename=os.path.join(LOG_LOCATION,'fullrefresh' + datetime.datetime.today().strftime('%Y%m%d%H%M%S') + '.log'), format='%(asctime)s %(message)s', level=logging.DEBUG)
    