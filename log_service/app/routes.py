from app.service import log_message

from app import app
from flask import request, Response

@app.route('/log', methods=['POST'])
def log():
    try:
        log_message(request.json)
        return Response(status=200)
    except Exception as e:
        return Response(f"An error occurred: {str(e)}\n", status=500)
