from flask import Blueprint

from api.responses import (
    response_with,
    SUCCESS_204,  
)

health_bp = Blueprint('health', __name__)

@health_bp.route('/', methods=["GET"])
def is_alive():
    return response_with(SUCCESS_204)