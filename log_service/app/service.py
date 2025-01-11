from datetime import datetime

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
    
    Log Format:
    [timestamp] [message]
    """

    formatted_message = format_message(json)

    with open('log.txt', 'a',encoding='UTF-8') as file:
        file.write(f"{formatted_message}\n")
