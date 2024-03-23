class Config:
    pass

class TestingConfig(Config):
    TESTING = True
    DATABASE_URI = "sqlite:///:memory:"

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URI = "postgresql://postgres:password@db:5432/metadata_db"

    