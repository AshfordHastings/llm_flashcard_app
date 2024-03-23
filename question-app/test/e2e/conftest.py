import pytest 
from sqlalchemy import create_engine, text
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import sessionmaker
from api.app import create_app
from db import Base
#from .db_scripts.insert_artist_data import insert_artist_data
#import domain.permissions as p



@pytest.fixture()
def app():
    app = create_app('testing')
    Base.metadata.create_all(bind=app.engine)
    return app


@pytest.fixture()
def client(app):
    with app.test_client() as client:
        with app.app_context():
            yield client

@pytest.fixture()
def populate_deck_data(app): 
    with open('../sql_scripts/insert_deck_data.sql') as f:
        raw_data = f.read()
    statements = raw_data.split(';')
    with app.engine.connect() as conn:
        for statement in statements:
            stmt = text(statement)
            conn.execute(stmt)
        conn.commit()
    return 

@pytest.fixture()
def populate_song_data(app, populate_deck_data):
    with open('../sql_scripts/insert_deck_data.sql') as f:
        raw_data = f.read()
    statements = raw_data.split(';')
    with app.engine.connect() as conn:
        for statement in statements:
            stmt = text(statement)
            conn.execute(stmt)
        conn.commit()
    return 

