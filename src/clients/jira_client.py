import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta
from src.settings import settings
from src.logger import Logger

JIRA_USER = settings.get_jira_user
JIRA_API_TOKEN = settings.get_jira_api_token
JIRA_URL = settings.get_jira_url

logger = Logger().get_logger(__name__)


def get_jira_data(
    username: str,
    start_date: datetime,
    end_date: datetime
) -> dict:
    auth = HTTPBasicAuth(JIRA_USER, JIRA_API_TOKEN)
    headers = {"Accept": "application/json"}
    jira_ed = (
        (end_date+timedelta(days=1)).strftime('%Y/%m/%d')
        if end_date
        else start_date.strftime('%Y/%m/%d')
    )
    jira_sd = start_date.strftime('%Y/%m/%d')
    jql = (
        f'assignee = "{username}" '
        + (f'AND updated >= startOfDay("-7d") ' if not jira_sd else f'AND updated >= "{jira_sd}" ')
        + (f'AND updated <= endOfDay() ' if not jira_ed else f'AND updated <= "{jira_ed}" ')
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


