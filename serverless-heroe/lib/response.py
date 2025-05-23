import json

def success_response(body, status_code=200):
    """
    Create a standardized success response

    Args:
        body (dict): The response body
        status_code (int, optional): HTTP status code. Defaults to 200.

    Returns:
        dict: Formatted response with statusCode and body
    """
    return {
        "statusCode": status_code,
        "body": json.dumps(body),
        "headers": {
            "Content-Type": "application/json"
        }
    }

def error_response(message, error=None, status_code=500):
    """
    Create a standardized error response

    Args:
        message (str): Error message
        error (str, optional): Detailed error information. Defaults to None.
        status_code (int, optional): HTTP status code. Defaults to 500.

    Returns:
        dict: Formatted error response with statusCode and body
    """
    body = {
        "message": message
    }

    if error:
        body["error"] = str(error)

    return {
        "statusCode": status_code,
        "body": json.dumps(body),
        "headers": {
            "Content-Type": "application/json"
        }
    }

def html_response(html_content, status_code=200):
    """
    Creates a standardized HTML response

    Parameters:
    - html_content: String containing HTML to return
    - status_code: HTTP status code (default: 200)

    Returns:
    - Dictionary with statusCode, headers, and body
    """
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'text/html; charset=UTF-8'
        },
        'body': html_content
    }
