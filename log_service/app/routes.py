from app.service import log_message,get_all_logs

from app import app
from flask import request, Response

@app.route('/log', methods=['POST'])
def log():
    try:
        log_message(request.json)
        return Response(status=200)
    except Exception as e:
        return Response(f"An error occurred: {str(e)}\n", status=500)

@app.route('/logs', methods=['GET'])
def get_logs():
    try:
        # Extract specific query parameters
        service = request.args.get('service')
        limit = request.args.get('limit', type=int, default=10)
        offset = request.args.get('offset', type=int, default=0)

        # Extract all tag-related query parameters dynamically
        tags = {key[4:]: value for key, value in request.args.items() if key.startswith("tag_")}
        print(f"Tags: {tags}")  # Debugging purposes

        # Call function with extracted parameters
        logs = get_all_logs(service=service, limit=limit, offset=offset, tags=tags)

        return logs
    except Exception as e:
        return Response(f"An error occurred: {str(e)}\n", status=500)
