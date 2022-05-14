from flask import Blueprint, jsonify

error_handler = Blueprint('error_handlers', __name__)


@error_handler.errorhandler(404)
def not_found(error):
    return (jsonify({"success": False, "error": 404,
                     "message": "resource not found"}), 404, )


@error_handler.errorhandler(422)
def unprocessable(error):
    return (
        jsonify({"success": False, "error": 422, "message": "unprocessable"}),
        422,
    )


@error_handler.errorhandler(400)
def bad_request(error):
    return jsonify({"success": False, "error": 400,
                   "message": "bad request"}), 400


@error_handler.errorhandler(401)
def unauthorized(error):
    return (
        jsonify(
            {
                "success": False,
                "error": 401,
                "message": "unauthorization"
            }
        ),
        401,
    )
