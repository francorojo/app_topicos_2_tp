from datetime import datetime
from multiprocessing import Lock
import re

lock = Lock()

def format_message(json: dict) -> str:
    """
    Formats a log message from a JSON dictionary.

    Args:
        json (dict): The dictionary containing log details. It must include:
            - "service" (str): The service name.
            - "message" (str): The log message.
            - Additional keys with "tag_" prefix for tagging.

    Returns:
        str: A formatted log string.

    Raises:
        ValueError: If "service" or "message" is missing.
    """
    service = json.pop('service', '')

    if not service:
        raise ValueError("Service name is required")

    message = json.pop('message', '')

    if not message:
        raise ValueError("Message is required")

    # Extract tags
    tags = [f"{tag.replace('tag_', '')}: {value}" for tag, value in json.items() if tag.startswith('tag_')]
    formatted_tags = f"[{', '.join(tags)}]" if tags else ''

    # Insert timestamp
    insert_timestamp = datetime.utcnow()

    return f"[{insert_timestamp}] [service: {service}] [message: {message}] {formatted_tags}"

def log_message(json: dict) -> None:
    """
    Logs a formatted message to the log file.

    Args:
        json (dict): The dictionary containing log details.
    """
    formatted_message = format_message(json)
    with lock:
        with open('log.txt', 'a', encoding='UTF-8') as file:
            file.write(f"{formatted_message}\n")

def get_all_logs(service: str = None, limit: int = 100, offset: int = 0, tags: dict = None, reversed_order: bool = False, from_time: datetime = None, to_time: datetime = None) -> list[str]:
    """
    Retrieves logs from the log file, applying optional filters.

    Args:
        service (str, optional): Filters logs by service name.
        limit (int, optional): Maximum number of logs to return.
        offset (int, optional): Number of logs to skip.
        tags (dict, optional): Dictionary of tag filters (e.g., {"env": "prod"}).
        reversed_order (bool, optional): If True, returns logs in reverse order.
        from_time (datetime, optional): Start timestamp filter.
        to_time (datetime, optional): End timestamp filter.

    Returns:
        list[str]: A list of log messages that match the filters.
    """
    logs = []
    log_pattern = re.compile(r"\[(.*?)\] \[service: (.*?)\] \[message: (.*?)\](?: \[(.*?)\])?")

    with open('log.txt', 'r', encoding='UTF-8') as file:
        log_lines = file.readlines()
        if reversed_order:
            log_lines.reverse()  # Reverse log order if needed

        for line in log_lines:
            log_entry = line.strip()
            match = log_pattern.match(log_entry)

            if not match:
                continue  # Skip malformed logs

            timestamp_str, log_service, message, extra_tags = match.groups()

            # Convert timestamp string to datetime object
            try:
                log_timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
            except ValueError:
                continue  # Skip if timestamp is incorrectly formatted

            # Convert extra tags into a dictionary
            tag_dict = {}
            if extra_tags:
                tag_pairs = extra_tags.split("] [")  # Split tags like `[type: tag_example]`
                for pair in tag_pairs:
                    key, value = pair.split(": ", 1)
                    tag_dict[key] = value

            # Apply service filter if provided
            if service and service != log_service:
                continue

            # Apply tag filters if provided
            if tags and not all(tag_dict.get(tag) == value for tag, value in tags.items()):
                continue

            # Apply timestamp range filters
            if from_time and log_timestamp < from_time:
                continue
            if to_time and log_timestamp > to_time:
                continue

            logs.append(log_entry)

    # Apply offset and limit AFTER filtering
    return logs[offset:offset + limit]
