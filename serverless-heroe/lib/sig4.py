import boto3
import requests
from requests_aws4auth import AWS4Auth

def aws_signed_request(url, region=None, service='execute-api', method='GET', params=None, json_body=None):
    """
    Make a signed request to AWS services using SigV4 authentication

    Args:
        url (str): The endpoint URL to call
        region (str): AWS region (defaults to session region)
        service (str): AWS service name (e.g., 'execute-api', 'dynamodb')
        method (str): HTTP method
        params (dict): Query parameters
        json_body (dict): JSON request body

    Returns:
        requests.Response: Response object
    """
    # Get credentials from boto3 session
    session = boto3.Session()
    credentials = session.get_credentials()
    region = region or session.region_name or 'us-east-1'

    # Create AWS4Auth instance for request signing
    auth = AWS4Auth(
        credentials.access_key,
        credentials.secret_key,
        region,
        service,
        session_token=credentials.token
    )

    # Make the signed request
    return requests.request(
        method,
        url,
        auth=auth,
        params=params,
        json=json_body
    )
