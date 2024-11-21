import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta
from src.settings import settings
from src.logger import Logger

JIRA_USER = settings.get_jira_user
JIRA_API_TOKEN = settings.get_jira_api_token
JIRA_URL = settings.get_jira_url

logger = Logger().get_logger(__name__)


def verify_date_format(start_date: str, end_date: str) -> bool:
    try:
        datetime.strptime(start_date, '%Y/%m/%d')
        datetime.strptime(end_date, '%Y/%m/%d')
        return True
    except ValueError:
        logger.error('Invalid date format. Please provide the date in YYYY/MM/DD format.')
        return False


def get_jira_data(username: str, start_date: str, end_date: str) -> dict:
    
    if not verify_date_format(start_date, end_date):
        start_date = start_date.replace('-', '/')
        end_date = end_date.replace('-', '/')
    
    auth = HTTPBasicAuth(JIRA_USER, JIRA_API_TOKEN)
    headers = {"Accept": "application/json"}
    jql = (
        f'assignee = "{username}" '
        + (f'AND updated >= startOfDay("-7d") ' if not start_date else f'AND updated >= "{start_date}" ')
        + (f'AND updated <= endOfDay() ' if not end_date else f'AND updated <= "{end_date}" ')
        + 'ORDER BY updated DESC'
    )
    logger.debug(f'Querying Jira with JQL: {jql}')
    url = f'{JIRA_URL}/rest/api/3/search?jql={jql}'
    response = requests.get(url, headers=headers, auth=auth)
    logger.debug(f'Jira response: {response.json()}')
    if settings.debug:
        print(response.json())
    return response.json()


def get_statuses():
    auth = HTTPBasicAuth(JIRA_USER, JIRA_API_TOKEN)
    headers = {"Accept": "application/json"}
    url = f'{JIRA_URL}/rest/api/3/status'
    response = requests.get(url, headers=headers, auth=auth)
    print(response.json())
    return response.json()

if __name__ == '__main__':
    end_date = datetime.today().strftime('%Y/%m/%d')
    start_date = (datetime.today() - timedelta(days=7)).strftime('%Y/%m/%d')
    username = 'Matias Zulberti'
    print(f'Fetching Jira data for {username} on {start_date}\n')
    data = get_jira_data(
        username=username,
        start_date=start_date,
        end_date=end_date
    )
    print(data)
    issues = data['issues']
    for issue in issues:
        summary = issue['fields']['summary']
        status = issue['fields']['status']['name']
        updated = issue['fields']['updated']
        key = issue['key']
        print(f'Summary: {summary}')
        print(f'Status: {status}')
        print(f'Updated at: {updated}')
        print(f'Key: {key}\n')


