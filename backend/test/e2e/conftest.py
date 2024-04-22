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
def populate_flashcard_data(app, populate_deck_data):
    with open('../sql_scripts/insert_flashcard_data.sql') as f:
        raw_data = f.read()
    statements = raw_data.split(';')
    with app.engine.connect() as conn:
        for statement in statements:
            stmt = text(statement)
            conn.execute(stmt)
        conn.commit()
    return 

@pytest.fixture()
def test_flashcard_payload_kubernetes():
    return [
        {
            "question": "What is the role of Ingress controller in Kubernetes?",
            "answer": "In Kubernetes, the Ingress controller is responsible for fulfilling the Ingress, usually with a load balancer, though it can also configure your edge router or additional frontends to help handle the traffic."
        },
        {
            "question": "How does Ingress control external access to services in a Kubernetes cluster?",
            "answer": "Ingress in Kubernetes manages external access to services in a cluster by routing external HTTP or HTTPS requests to internal services based on defined rules."
        },
        {
            "question": "What are the differences between Ingress and Service in Kubernetes?",
            "answer": "Ingress is a collection of routing rules that govern how external users access services running in a Kubernetes cluster. Service, on the other hand, is an abstraction that defines a logical set of pods and a policy to access them."
        },
        {
            "question": "What are the benefits of using Service Discovery in Kubernetes?",
            "answer": "Service Discovery in Kubernetes provides a flexible and scalable way for services to find and communicate with each other. It allows services to be loosely coupled, enhances service availability, and enables load balancing."
        },
        {
            "question": "Why is it necessary to use Ingress in a Kubernetes cluster?",
            "answer": "Ingress is necessary in a Kubernetes cluster to efficiently manage access to services from outside the cluster. It provides load balancing, SSL termination, and name-based virtual hosting."
        },
    ]