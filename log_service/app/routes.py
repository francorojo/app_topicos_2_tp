from app.service import log_message, get_all_logs
from app import app
from flask import request, Response
from datetime import datetime

@app.route('/log', methods=['POST'])
def log():
    log_message(request.json)
    return Response(status=200)

@app.route('/logs', methods=['GET'])
def get_logs():
    """
    Retrieves logs based on query parameters such as service, timestamp range, limit, offset, and tags.
    """
    try:
        # Extract standard filters
        service = request.args.get('service')
        limit = request.args.get('limit', type=int, default=10)
        offset = request.args.get('offset', type=int, default=0)
        reversed_order = request.args.get('reversed', type=bool, default=False)

        # Extract time range filters
        from_timestamp = request.args.get('from')
        to_timestamp = request.args.get('to')

        # Extract tag-related filters dynamically
        tags = {key[4:]: value for key, value in request.args.items() if key.startswith("tag_")}

        # Convert timestamps to datetime objects
        from_time = datetime.strptime(from_timestamp, "%Y-%m-%d %H:%M:%S") if from_timestamp else None
        to_time = datetime.strptime(to_timestamp, "%Y-%m-%d %H:%M:%S") if to_timestamp else None

        # Debugging logs (optional)
        print(f"Filters - Service: {service}, From: {from_time}, To: {to_time}, Tags: {tags}, Limit: {limit}, Offset: {offset}")

        # Call function with extracted parameters
        logs = get_all_logs(
            service=service, 
            limit=limit, 
            offset=offset, 
            tags=tags, 
            reversed_order=reversed_order,
            from_time=from_time,
            to_time=to_time
        )

        return logs

    except ValueError as e:
        return Response(f"Invalid timestamp format. Use 'YYYY-MM-DD HH:MM:SS'. Error: {str(e)}\n", status=400)

@app.errorhandler(Exception)
def handle_exception(error):
    return Response(f"An error occurred: {str(error)}\n", status=500)
