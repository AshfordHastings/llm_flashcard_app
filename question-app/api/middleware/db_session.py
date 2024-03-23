from flask import g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker  


def init_app(app):
    app.engine = create_engine(app.config['DATABASE_URI'])
    app.Session = sessionmaker(bind=app.engine)

    @app.before_request
    def init_db_context():
        g.db_session = app.Session()

    @app.after_request
    def teardown_db_context(response):
        db_session = getattr(g, 'db_session', None)
        if db_session is not None:
            db_session.close()
        return response