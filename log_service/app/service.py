from datetime import datetime
from multiprocessing import Lock
import re

lock = Lock()

def format_message(json: dict) -> str:
    service = json.pop('service', '')

    if not service:
        raise ValueError("Service name is required")

    message = json.pop('message', '')

    if not message:
        raise ValueError("Message is required")


    tags = [f"{tag.replace('tag_','')}: {value}" for tag, value in json.items() if tag.startswith('tag_')]

    formatted_tags = f"[{', '.join(tags)}]" if tags else ''

    insert_timestamp = datetime.utcnow()
 
    return f"[{insert_timestamp}] [service: {service}] [message: {message}] {formatted_tags}"

def log_message(json: dict) -> None:
    """
    Logs a given message to a file named 'log.txt'.
    Args:
        message (str): The message to be logged.

    """

    formatted_message = format_message(json)
    with lock:
        with open('log.txt', 'a',encoding='UTF-8') as file:
            file.write(f"{formatted_message}\n")


def get_all_logs(service: str = None, limit: int = 100, offset: int = 0, tags: dict = None) -> list[str]:
    """
    Retrieves logs from the log file, applying optional filters.

    Args:
        service (str, optional): Filter logs by service name. If None, returns all logs.
        limit (int, optional): Max number of logs to return. Defaults to 100.
        offset (int, optional): Number of logs to skip. Defaults to 0.
        tags (dict, optional): Dictionary of tag filters (e.g., {"tag_env": "prod"}).

    Returns:
        list[str]: A list of log messages.
    """

    logs = []
    log_pattern = re.compile(r"\[(.*?)\] \[service: (.*?)\] \[message: (.*?)\](?: \[(.*?)\])?")

    with open('log.txt', 'r', encoding='UTF-8') as file:
        for line in file:
            log_entry = line.strip()
            match = log_pattern.match(log_entry)

            if not match:
                continue  # Skip malformed logs

            timestamp, log_service, message, extra_tags = match.groups()

            # Convert extra tags into a dictionary
            tag_dict = {}
            if extra_tags:
                tag_pairs = extra_tags.split("] [")  # Split tags like `[type: tag_example]`
                for pair in tag_pairs:
                    key, value = pair.split(": ", 1)
                    tag_dict[key] = value

            # Apply service filter **only if service is provided**
            if service and service != log_service:
                continue

            # Apply tag filters if provided
            if tags and not all(tag_dict.get(tag) == value for tag, value in tags.items()):
                continue

            logs.append(log_entry)

    # Apply offset and limit AFTER filtering
    return logs[offset:offset + limit]
