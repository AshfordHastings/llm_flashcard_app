import argparse
from gunicorn.app.base import BaseApplication
from multiprocessing import cpu_count

from db import Base
from api.app import create_app

parser = argparse.ArgumentParser(description="Run the backend Flashcard application.")

parser.add_argument("--gunicorn", '-g', action="store_true", help="Option to run application using Gunicorn.")
parser.add_argument("--env", '-e', type=str, help="Option to specify environment.")

args = parser.parse_args()

def number_of_workers():
    return (cpu_count() * 2) + 1

class StandaloneGunicornApplication(BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()
    
    def load_config(self):
        config = {key: value for key, value in self.options.items() if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application
    
def run_flask():
    app = create_app(config_name="development")
    options = {
        'bind': '0.0.0.0:5000',
        # 'workers': number_of_workers(),
        'workers': 4,
        'timeout': 120
    }
    StandaloneGunicornApplication(app, options).run()

if __name__ == "__main__":
    if args.env:
        config_name = args.env
    else:
        config_name = "development"

    if args.gunicorn:
        run_flask()
    else:
        app = create_app(config_name)
        app.run(port=5001, debug=True)