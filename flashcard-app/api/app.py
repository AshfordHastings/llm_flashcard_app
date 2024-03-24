from flask import Flask, g
from api.routes import health_bp, deck_bp, flashcard_bp
from api.middleware import init_db_session, init_error_handlers
from cfg import TestingConfig, DevelopmentConfig

CONFIG_MAPPER = {
    'testing': TestingConfig,
    'development': DevelopmentConfig
}

def create_app(config_name='testing'):
    app = Flask(__name__)
    app.config.from_object(CONFIG_MAPPER[config_name])

    init_db_session(app)
    init_error_handlers(app)

    app.register_blueprint(deck_bp, url_prefix='/api/decks')
    #app.register_blueprint(flashcard_bp, url_prefix='/api/decks/<int:deck_id>/flashcards')
    app.register_blueprint(flashcard_bp)

    app.register_blueprint(health_bp, url_prefix='/api/health')
    
    return app