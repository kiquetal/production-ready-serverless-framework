import  os
import datetime
from jinja2 import FileSystemLoader, Environment
from lib.response import success_response, error_response, html_response
from lib.sig4 import aws_signed_request
from aws_lambda_powertools.utilities.parameters import get_parameter
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def return_page():
    try:
        template_dir = os.path.join(os.path.dirname(__file__), '..','static')
        env = Environment(loader=FileSystemLoader(template_dir), autoescape=True)
        template = env.get_template('index-cognito.html')
        return template
    except Exception as e:
        print("Error loading template: ", str(e))
        return error_response("Failed to return template", str(e))

def get_restaurants_via_api(count=8):
    """Fetch restaurants through the API Gateway instead of directly from DynamoDB"""
    api_url = os.environ.get('API_GATEWAY')
    api_prod_domain = os.environ.get('API_PROD_DOMAIN')
    if api_prod_domain:
        api_url = api_prod_domain + "/apis"
    if not api_url:
        raise ValueError("API_GATEWAY environment variable not set")

    print(f"The API URL is {api_url}")
    response = aws_signed_request(
        f"{api_url}/restaurants",
        params={"limit": count}
    )

    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching restaurants from API: ", response.status_code, response.text)
        raise Exception(f"API request failed: {response.status_code}, {response.text}")


def load_restaurants(event, context):

    """
    Just for the sake of learning, this will now request another path in the apigateway
    should parse the JSON response and render it in the template
    """
    try:
        default_results = int(os.environ.get('default_results', 8))
        template = return_page()
        default_results = os.environ.get('DEFAULT_RESULTS')
        default_results = int(get_parameter(name=default_results))
        restaurants = get_restaurants_via_api(default_results)
        search_url = os.environ.get('API_GATEWAY') + '/restaurants/search'
        search_url_prod = os.environ.get('API_PROD_DOMAIN') + '/apis' + '/restaurants/search'
        if os.environ.get('API_PROD_DOMAIN'):

            search_url = search_url_prod
        print(f"search_url is {search_url}")
        print("Weekday is", datetime.datetime.now().weekday())
        dayOfWeek = days[datetime.datetime.now().weekday()]

        variables_templates = {
            'dayOfWeek': dayOfWeek,
            'restaurants': restaurants,
            'awsRegion': os.environ.get('AWS_REGION'),
            'cognitoUserPoolId': os.environ.get('COGNITO_USER_POOL_ID'),
            'cognitoClientId': os.environ.get('COGNITO_WEB_CLIENT_ID'),
            'searchUrl': search_url
            }

        rendered_page = template.render(**variables_templates)
        return html_response(rendered_page)
    except Exception as e:
        return error_response("Failed to load restaurants", str(e))
