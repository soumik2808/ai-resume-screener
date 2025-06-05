class DefaultConfig:
    DEBUG = True
    UPLOAD_FOLDER = 'uploads'

class ProductionConfig(DefaultConfig):
    DEBUG = False
