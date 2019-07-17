class Config(object):
    DEBUG=False
    CSRF_ENABLED=True

class DevelopmentConfig(Config):
    DEBUG=True
    ENV='development'
    DATA_LOCATION='./devdata/'

class TestingConfig(Config):
    Testing=True
    DEBUG=True
    ENV='testing'
    DATA_LOCATION='./testdata/'

class ProductionConfig(Config):
    DEBUG=False
    ENV='production'
    DATA_LOCATION='./data/'

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}