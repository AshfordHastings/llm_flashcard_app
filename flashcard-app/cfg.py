class Config:
    pass

class TestingConfig(Config):
    TESTING = True
    DATABASE_URI = "sqlite:///:memory:"

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URI = "postgresql://postgres:password@localhost:5432/flashcard_db"

    