from flask import make_response, jsonify

def response_with(response, value=None, errors=None, headers={}):
    result = {}
    if response.get("message") is not None:
        result.update({"message": response.get("message")})
    if value is not None:
        result.update({"value": value})
    if errors is not None:
        result.update({"error": errors})

    headers.update({'Access-Control-Allow-Origin': '*'})
    headers.update({'server': 'Flask REST API'})

    return make_response(jsonify(result), response['http_code'], headers)

SUCCESS_200 = {
    "http_code": 200,
    'message': 'OK'
}

SUCCESS_201 = {
    "http_code": 201,
    'message': 'Created'
}

SUCCESS_204 = {
    "http_code": 204,
    'message': 'No Content'
}

BAD_REQUEST_400 = {
    "http_code": 400,
    'message': 'Bad Request'
}

UNAUTHORIZED_401 = {
    "http_code": 401,
    'message': 'Unauthorized'
}

FORBIDDEN_403 = {
    "http_code": 403,
    'message': 'Forbidden'
}

NOT_FOUND_404 = {
    "http_code": 404,
    'message': 'Not Found'
}

ERROR_500 = {
    "http_code": 500,
    'message': 'Internal Server Error'
}