from api.responses import response_with, ERROR_500, NOT_FOUND_404
from exc import ResourceNotFound

def init_app(app):

    @app.errorhandler(ResourceNotFound)
    def handle_not_found(error):
        return response_with(NOT_FOUND_404, errors=str(error))

    @app.errorhandler(Exception)
    def handle_exceptions(error):
        return response_with(ERROR_500, errors=str(error))
