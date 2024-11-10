from flask import jsonify
import datetime


def get_response(status: str, message: str, data: dict):
    data = {
        "status": status,
        "message": message,
        "timestamp": datetime.datetime.now(),
        "data": None
    }
    return jsonify(data)
