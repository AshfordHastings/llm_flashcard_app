class Config:
    pass

class TestingConfig(Config):
    TESTING = True
    # DATABASE_URI = "sqlite:///:memory:"
    DATABASE_URI = "postgresql://postgres:password@localhost:5432/flashcard_db"

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URI = "postgresql://postgres:password@fc_db:5432/flashcard_db"

    