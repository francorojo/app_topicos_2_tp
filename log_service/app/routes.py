from app.service import log_message

from app import app
from flask import request, Response

@app.route('/log', methods=['POST'])
def log():
    log_message(request.json)
    return Response(status=200)
