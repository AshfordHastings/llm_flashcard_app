from sqlalchemy import create_engine, text
from db import Base

from api.app import create_app

if __name__ == "__main__":
    app = create_app(config_name="development")
    app.run(port=5001, debug=True)